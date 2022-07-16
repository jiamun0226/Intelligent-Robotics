#!/bin/bash
rosrun sound_play soundplay_node.py &
rosrun task1_2 ask_name_synthesis.py &
rosrun task1_2 ask_name_sr.py 
roslaunch rchomeedu_vision multi_astra.launch &
roslaunch robot_vision_openvino interactive_face_ros.launch & 
rosrun task1_2 say_gender_synthesis.py

rosnode kill -a