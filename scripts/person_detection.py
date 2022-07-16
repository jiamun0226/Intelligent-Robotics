#!/usr/bin/env python
from unittest import result
import rospy
from std_msgs.msg import String
from robot_vision_msgs.msg import BoundingBoxes
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
import subprocess
import os
from gtts import gTTS


class People:
    def __init__(self):
        rospy.Subscriber('/yolo_ros/bounding_boxes', BoundingBoxes, self.callback)
        rospy.spin()

    
    def tts_func(self,data):
        tts = gTTS(data)
        tts.save("speech.mp3")
        os.system("mpg321 speech.mp3")
        os.remove("speech.mp3")
        

    def callback(self,data):
        rospy.loginfo("Run successfully")
        pred = data.bounding_boxes[0].Class
        rospy.sleep(5)
        if pred == "person":
            reply = "Hello, welcome home!"
            self.tts_func(reply)
            rospy.loginfo(pred)
        rospy.sleep(3)


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    r = People()
    
        
    


