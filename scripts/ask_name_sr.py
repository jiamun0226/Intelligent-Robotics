#!/usr/bin/env python2

import rospy
from std_msgs.msg import String
import speech_recognition as sr


def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

def callback(data):
    if data.data =="kill":
        stop = True
        rospy.signal_shutdown(stop)


def googlesr():
    rospy.init_node('googlesr', anonymous=True)
    pub = rospy.Publisher('reply', String, queue_size=10)

    while not rospy.is_shutdown():
        # obtain audio from the microphone
        sleep(5)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(">>> Say something!")
            #audio = r.listen(source)
            audio = r.record(source, duration=3)
            
        # recognize speech using Google Speech Recognition
        
        try:
            result = r.recognize_google(audio)
            print("SR result: " + result)
            result = result.lower()
            name_list = ["william", "jack", "angel", "charlotte"]
            for x in name_list:
                if x in result:     
                    pub.publish(result)
                    print(result)
                else:
                    pass                     
        except sr.UnknownValueError:
            print("SR could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
        rospy.Subscriber('reply_kill', String, callback=callback)
        


if __name__ == '__main__':
    try:
        googlesr()
    except rospy.ROSInterruptException:
        pass