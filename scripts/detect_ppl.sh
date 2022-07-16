#!/bin/bash
roslaunch rchomeedu_vision multi_astra.launch &
sleep 5
rosrun final_robocup person_detection.py &
sleep 5
roslaunch robot_vision_openvino yolo_ros.launch 

