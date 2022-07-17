#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from PIL import Image

import numpy as np
import torch
import cv2
import joblib
import torchvision.transforms as transforms
import torch.nn as nn

from models import MultiHeadResNet50

def detector():
    pub = rospy.Publisher('shirt_detector', String, queue_size=10)
    pub2 = rospy.Publisher('detection', String, queue_size=10)
    #pub2 = rospy.Publisher('glass_speech', String, queue_size=10)
    rospy.init_node('shirt_detector', anonymous = True)
    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    detected = shirt_detector()
    rospy.loginfo(detected)
    pub.publish(detected)
    pub2.publish(detected)
    #image = Image.open('temp.jpeg')
    #image.show()
    rate.sleep()



def loss_fn(outputs, targets):
  o1, o2, o3, o4 = outputs
  t1, t2, t3, t4 = targets
  l1 = nn.CrossEntropyLoss()(o1, t1)
  l2 = nn.CrossEntropyLoss()(o2, t2)
  l3 = nn.CrossEntropyLoss()(o3, t3)
  l4 = nn.CrossEntropyLoss()(o4, t4)

  return (l1 + l2 + l3 + l4) / 4

def shirt_detector():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MultiHeadResNet50(pretrained=False, requires_grad=False)

    checkpoint = torch.load('/home/jiamun/catkin_ws/src/robocup_pkg/launch/model3_adamW_master_sub.pth', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225])
    ])


    image = cv2.imread('/home/jiamun/catkin_ws/src/robocup_pkg/launch/test_images/image_3.jpeg')
    original_image = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = transform(image)
    # add batch dimension
    image = image.unsqueeze(0).to(device)

    # forward pass the image through the model
    outputs = model(image)
    # extract the four outputs
    output1, output2, output3, output4 = outputs
    # get the index positions of the highest label score
    out_label_1 = np.argmax(output1.detach().cpu())
    out_label_2 = np.argmax(output2.detach().cpu())
    out_label_3 = np.argmax(output3.detach().cpu())
    out_label_4 = np.argmax(output4.detach().cpu())

    # load the label dictionaries
    num_list_master = joblib.load('/home/jiamun/catkin_ws/src/robocup_pkg/launch/input/num_list_master.pkl')
    num_list_sub = joblib.load('/home/jiamun/catkin_ws/src/robocup_pkg/launch/input/num_list_sub.pkl')
    num_list_article = joblib.load('/home/jiamun/catkin_ws/src/robocup_pkg/launch/input/num_list_article.pkl')
    num_list_colour = joblib.load('/home/jiamun/catkin_ws/src/robocup_pkg/launch/input/num_list_colour.pkl')

    # get the keys and values of each label dictionary
    master_keys = list(num_list_master.keys())
    master_values = list(num_list_master.values())

    sub_keys = list(num_list_sub.keys())
    sub_values = list(num_list_sub.values())

    article_keys = list(num_list_article.keys())
    article_values = list(num_list_article.values())

    colour_keys = list(num_list_colour.keys())
    colour_values = list(num_list_colour.values())

    final_labels = []

    # append the labels by mapping the index position to the values 
    final_labels.append(master_keys[master_values.index(out_label_1)])
    final_labels.append(sub_keys[sub_values.index(out_label_2)])
    final_labels.append(article_keys[article_values.index(out_label_3)])
    final_labels.append(colour_keys[colour_values.index(out_label_4)])

    # write the label texts on the image
    cv2.putText(
        original_image, final_labels[0], (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 
        0.8, (255, 0, 0), 2, cv2.LINE_AA 
    )
    cv2.putText(
        original_image, final_labels[1], (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
        0.8, (255, 0, 0), 2, cv2.LINE_AA 
    )
    cv2.putText(
        original_image, final_labels[2], (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 
        0.8, (255, 0, 0), 2, cv2.LINE_AA 
    )
    cv2.putText(
        original_image, final_labels[3], (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 
        0.8, (255, 0, 0), 2, cv2.LINE_AA 
    )
    """
    # visualize and save the image
    cv2.imshow('output', original_image)
    print(f'masterCategory: {final_labels[0]}')
    print(f'subCategory: {final_labels[1]}')
    print(f'articleType: {final_labels[2]}')
    print(f'baseColour: {final_labels[3]}')
    # cv2.imwrite('/content/outputs/test_image_1.jpg', original_image)
    """
    label_shirt = final_labels[3] +" "+ final_labels[1]
    return label_shirt



if __name__ == '__main__':
    try:
        detector()
    except rospy.ROSInterruptException:
        pass