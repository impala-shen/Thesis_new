#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
from data_collector.msg import BasicInfo
import time

weight=0
size=0
x1=99
y1=99
dist1=99
weight2=0
size2=0
x2=0
y2=0
dist2=0
x=0
y=0
type1=''
type2=''


def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)


def agent_callback(msg):
    global x
    global y
    # x_a=60
    # y_a=7
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y

def gar1_callback(msg):
    global weight
    global size
    global x1
    global y1
    global dist1
    global type1
    weight=msg.weight
    #print("weight sensor:%s" %(weight))
    size=msg.size
    #print("camera:%s" %(size))   
    x1=msg.x
    y1=msg.y
    orient=msg.orient
    type1=msg.type
    dist1=distance(x,y,x1,y1)
    # print("x=%s,y=%s" %(x1,y1))  #relate with distance,calculate orientation
    # print("distance_garbage=%f" %(dist1))
    # rospy.loginfo(msg)

def gar2_callback(msg):
    global weight2
    global size2
    global x2
    global y2
    global dist2
    global type2
    weight2=msg.weight
    #print("weight sensor2:%s" %(weight))
    size2=msg.size
    #print("camera2:%s" %(size))  
    type2=msg.type 
    x2=msg.x
    y2=msg.y
    orient=msg.orient
    dist2=distance(x,y,x2,y2)
    # print("x2=%s,y2=%s" %(x2,y2))  #relate with distance,calculate orientation
    # print("distance_garbage2=%f" %(dist2))
    # rospy.loginfo(msg)


def main():
    rospy.init_node("garbage_sub")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    rospy.Subscriber("/gar1_info", BasicInfo ,gar1_callback)
    rospy.Subscriber("/gar2_info", BasicInfo ,gar2_callback)
    pub=rospy.Publisher('G_sensor_info', BasicInfo, queue_size=10)
    pub1=rospy.Publisher('G_sensor_info1', BasicInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
##sensor gives the infomation of the cloest garbage
    while not rospy.is_shutdown():
        msg=BasicInfo()
        # msg.weight=weight
        # msg.size=size
        # msg.x=x1
        # msg.y=y1
        # msg.orient=0
        # msg.type=type2
        # msg.type=type
        if dist2>dist1:
            msg.weight=weight
            msg.size=size
            msg.x=x1
            msg.y=y1
            msg.type=type1
            msg.dis=dist1
        else:
            msg.weight=weight2
            msg.size=size2
            msg.x=x2
            msg.y=y2
            msg.type=type2
            msg.dis=dist2

        # msg1=BasicInfo()
        # msg1.weight=weight
        # msg1.size=size
        # msg1.x=x1
        # msg1.y=y1
        # msg1.type=type1
        # msg1.dis=dist1
        # rospy.loginfo(msg1)
        # pub1.publish(msg1)

        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass