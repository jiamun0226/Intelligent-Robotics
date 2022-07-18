# Intelligent-Robotics
### <ins>Find My Mates</ins>

### Instructions to run the code.
<I>P.S. Steps 1 and 2 are not needed if you are deploying the code on JUNO/IO/Jupiter Robot</I>
<ol>
<li>Install ROS Melodic according to http://wiki.ros.org/melodic/Installation/Ubuntu</li>
<li>Git clone github repo</li>

`git clone https://github.com/robocupathomeedu/rc-home-edu-learn-ros.git`

<li>Create a new ROS package, following steps in http://wiki.ros.org/ROS/Tutorials/CreatingPackage</li>

`cd ~/catkin_ws/src`

`catkin_create_pkg task1_2 rospy roscpp std_msgs sensor_msgs cv_bridge`

`cd ..`

`catkin_make`

<li>Create a folder named scripts in the package</li>

`mkdir scripts`

<li>Download and paste all the files from scripts into the scripts folder that you have created</li>

<li>Run the xx.sh code </li>
<I>P.S. Follow the steps in the Techniques section below</I>
</ol>

## Techniques 
<ol>
<li><b>For Person Detection</b></li>

- Run the detect_ppl.sh file 

`roscd task1_2/scripts`

`./detect_ppl.sh`

<li><b>For Gender and Age Detection</b></li>

- Run the run.sh file

`roscd task1_2/scripts`

`./run.sh`

<li><b>For Gender and Age Detection</b></li>

- Download the pretrained facial landmarks recognition from https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat

- Run the glasses_detection_robocup.py file

`rosrun glasses_detection_robocup.py`

<li><b>For Posture Detection</b></li>

- Modify the image path for posture detection

- Run the gesture2.py file

`rosrun gesture2.py`

<li><b>For Object Detection</b></li>

- Modify the image path for object detection (objects that can be detected: whiteboard, chairs, tables, clothes, person)

- Run the object2.py file

`rosrun object2.py`

<li><b>For Shirt Type and Colour Detection</b></li>

- Modify the image path for shirt detection

- Run the inference.py file

`rosrun inference.py`
</ol>





