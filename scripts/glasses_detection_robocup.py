#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

import numpy as np
import dlib
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import statistics


def detector():
    pub = rospy.Publisher('glasses_detector', String, queue_size=10)
    pub2 = rospy.Publisher('detection', String, queue_size=10)
    rospy.init_node('detector', anonymous = True)
    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    detected = glasses_detector()
    rospy.loginfo(detected)
    pub.publish(detected)
    pub2.publish(detected)
    image = Image.open('temp.jpeg')
    image.show()
    rate.sleep()



def glasses_detector():
    datFile = '/home/jiamun/catkin_ws/src/robocup_pkg/launch/shape_predictor_68_face_landmarks.dat'
    #'/home/jiamun/catkin_ws/src/beginner_tutorials/scripts/glasses_detection/shape_predictor_68_face_landmarks.dat'
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(datFile)
    imcap = cv2.VideoCapture(0) 
    imcap.set(3, 640) # set width as 640
    imcap.set(4, 480) # set height as 480

    success, img = imcap.read() # capture frame from video
    cv2.imwrite('temp.jpeg', img)
    img = dlib.load_rgb_image('temp.jpeg')

    if len(detector(img))==0:
        return('No face detected')
    rect = detector(img)[0]
    sp = predictor(img, rect)
    landmarks = np.array([[p.x, p.y] for p in sp.parts()])

    nose_bridge_x = []
    nose_bridge_y = []

    for i in [28,29,30,31,33,34,35]:
        nose_bridge_x.append(landmarks[i][0])
        nose_bridge_y.append(landmarks[i][1])

    ### x_min and x_max
    x_min = min(nose_bridge_x)
    x_max = max(nose_bridge_x)

    ### ymin (from top eyebrow coordinate),  ymax
    y_min = landmarks[20][1]
    y_max = landmarks[30][1]

    img2 = Image.open('temp.jpeg')
    img2 = img2.crop((x_min,y_min,x_max,y_max))
    plt.imshow(img2)
    

    img_blur = cv2.GaussianBlur(np.array(img2),(3,3), sigmaX=0, sigmaY=0)

    edges = cv2.Canny(image =img_blur, threshold1=100, threshold2=200)

    edges_center = edges.T[(int(len(edges.T)/2))]

    feature = "a"

    if 255 in edges_center:
        feature = "Glasses present"
        glass_label = " is wearing glasses."
    else:
        feature = "Glasses absent"
        glass_label = " is not wearing glasses."

    return feature

"""
    file1 = open('name.txt','r')
    name = file1.read()
    file = open('feature.txt', 'a')
    file.write('. ')
    file.write(name)
    file.write(glass_label)
    file.close()
"""


if __name__ == '__main__':
    try:
        detector()
    except rospy.ROSInterruptException:
        pass
