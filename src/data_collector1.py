#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int8
import time

def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)

def agent_callback(msg):
    global x
    global y
    x_a=60
    y_a=7
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    dist_a=distance(x,y,x_a,y_a)
    print("x=%f,y=%f" %(x,y))
    print("distance_accident=%f" %(dist_a))
    # rospy.loginfo("x=%f,y=%f" %(x,y))

def car1_callback(msg):
    global x1
    global y1
    global dist
    x1=msg.pose.pose.position.x
    y1=msg.pose.pose.position.y
    dist=distance(x,y,x1,y1)
    if y1<=9 and y1>=5:
        print("accident happen!")
    print("x1=%f,y1=%f" %(x1,y1))
    print("distance_1=%f" %(dist))
    # rospy.loginfo("x1=%f,y1=%f" %(x1,y1))
    # rospy.loginfo("distance=%f" %(dist))

def car2_callback(msg):
    x2=msg.pose.pose.position.x
    y2=msg.pose.pose.position.y
    dist=distance(x,y,x2,y2)
    if y2<=9 and y2>=5:
        print("accident happen!")
    print("x2=%f,y2=%f" %(x2,y2))
    print("distance_2=%f" %(dist))


def weather_callback(msg):
    print("weather:%s" %(msg))
    # rospy.loginfo(msg)


def internal_state_callback(msg):
    print("internal_state:%s" %(msg))
    # rospy.loginfo(msg)


def time_callback(msg):
    print("current_time:%s" %(msg))
    # rospy.loginfo(msg)


def main():
    rospy.init_node("data_collector")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    rospy.Subscriber("/1_front_car/odom",Odometry,car1_callback)
    rospy.Subscriber("/2_front_car/odom",Odometry,car2_callback)
    ##rospy.Subscriber("/weather",String,weather_callback)
    rospy.Subscriber("/internal_state", Int8 ,internal_state_callback)
    rospy.Subscriber("/time", Int8 ,time_callback)
    rospy.spin()

if __name__=='__main__':
    main()