#!/usr/bin/env python

import math
import rospy
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
from data_collector.msg import JobInfo
import time

LS=74
global x_dp,y_dp
global x,y

x_dp=7
y_dp=18
x=0
y=0
##########test DM#########
# x_dp=7
# y_dp=3
# x=7
# y=1


def convert_r(x_max,x_min,x_r):
    x_max=float(x_max)
    x_min=float(x_min)
    x_r=float(x_r)
    g=1.8*(1-(x_max-x_r)/(x_max-x_min))
    return math.exp(g)-1

def convert_c(x_max,x_min,x_c):
    x_max=float(x_max)
    x_min=float(x_min)
    x_c=float(x_c)
    g=1.8*(1-(x_c-x_min)/(x_max-x_min))
    # rospy.loginfo("g=%f" %(g))
    return math.exp(g)-1


def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)

def agent_callback(msg):
    global x,y
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    # print("x=%f,y=%f" %(x,y))
    # print("distance to PowerStation=%f" %(dist))
    # rospy.loginfo("x=%f,y=%f" %(x,y))


def PS_callback(msg):
    global PS
    PS=msg.data



def main():
    global LS
    global dist
    rospy.init_node("GotoDumping")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    rospy.Subscriber("/Power_status", Int32, PS_callback)
    pub=rospy.Publisher('GoDumping', JobInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")   
    
##sensor gives the infomation of the cloest garbage
    while not rospy.is_shutdown():
        # p=50/dist+(100-PS)   ###could be changed for debugging
        dist=distance(x,y,x_dp,y_dp)
        dist1=convert_c(60,0,dist)
        LS1=convert_c(100,0,LS)
        p= 10*(0.2*dist1 + 0.714*LS1)
        msg=JobInfo()
        msg.task="GoDumping"
        msg.priority=p
        msg.x=x_dp
        msg.y=y_dp
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass