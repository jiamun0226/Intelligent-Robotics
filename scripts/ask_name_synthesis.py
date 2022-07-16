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
    msg = msg.capitalize()
    rospy.loginfo('I received: %s' % (msg))
    pub = rospy.Publisher('guest_name', String, queue_size=10)
    pub2 = rospy.Publisher('reply_kill', String, queue_size=10)
    say = 'Hi, ' + msg + '. Nice to meet you.'
    rospy.loginfo(say)
    play_sound(say)
    pub.publish(msg)
    kill = "kill"
    pub2.publish(kill)
    
    file1 = open("name.txt","w")
    file1.write(msg)
    file1.close()
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
    question = 'What is your name?'
    play_sound(question)
    rospy.Subscriber('reply', String, callback=callback)
    # rospy.Subscriber('/interactive_face_ros/face_results', FaceResults, callback=get_gender_age)
    rospy.spin()
    