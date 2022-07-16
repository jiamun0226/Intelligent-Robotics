#!/usr/bin/env python2
  

from tokenize import String

from paramiko import Agent
import rospy, os, sys
from sound_play.msg import SoundRequest
from std_msgs.msg import String
from robot_vision_msgs.msg import FaceResults
from sound_play.libsoundplay import SoundClient

import subprocess


def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass


def callback(data):
    msg = data.data
    msg = msg.lower()
    rospy.loginfo('I received: %s' % (msg))
    pub = rospy.Publisher('guest_name', String, queue_size=10)
    pub2 = rospy.Publisher('reply_kill', String, queue_size=10)
    say = 'Hi, ' + msg + '. Nice to meet you.'
    rospy.loginfo(say)
    play_sound(say)
    pub.publish(msg)
    kill = "kill"
    pub2.publish(kill)
    # file1 = file1.write("name.txt","W")
    # file1.write(msg)
    # file1.close()
    

def get_gender_age(data):
    #data = FaceResults()
    #details = []
    
    file2 = open("/home/mustar/catkin_ws/src/task1_2/scripts/name.txt", "r")
    name = file2.read()
    file2.close()
    rospy.loginfo("I received person details")
    say2 = name
    age = data.results[0].age
    gender = data.results[0].gender
    if gender == "Female":
        say2 += " is a female. She is " + str(age) + " years old."
    else:
        say2 += " is a male. He is " + str(age) + " years old."
    play_sound(say2)

    stop = True
    rospy.signal_shutdown(stop)


def play_sound(msg):
    soundhandle = SoundClient()
    sleep(1)
    soundhandle.stopAll()
    soundhandle.say(msg)
    sleep(3)

if __name__ == '__main__':
    rospy.init_node('soundplay_test', anonymous = True)
    # question = 'What is your name?'
    # play_sound(question)
    # rospy.Subscriber('reply', String, callback=callback)
    rospy.Subscriber('/interactive_face_ros/face_results', FaceResults, callback=get_gender_age)
    rospy.spin()
    