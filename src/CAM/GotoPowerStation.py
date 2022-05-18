#!/usr/bin/env python

import math
import rospy
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
from data_collector.msg import JobInfo
import time

# PS=50
# dist=18
# global x_ps,y_ps
# x_ps=0
# y_ps=20
# # x_ps=3
# # y_ps=3
# w=2
global x_ps,y_ps
global x,y
PS=50

x_ps=0
y_ps=20
x=0
y=0
##########test DM#########
# x_ps=3
# y_ps=3
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
    global PS
    global dist
    # x_ps=3
    # y_ps=3   
    rospy.init_node("GotoPowerStation")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    rospy.Subscriber("/Power_status", Int32, PS_callback)
    pub=rospy.Publisher('GotoPS', JobInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")   
    
##sensor gives the infomation of the cloest garbage
    while not rospy.is_shutdown():
        # p=50/dist+(100-PS)   ###could be changed for debugging
        dist=distance(x,y,x_ps,y_ps)
        dist1=convert_c(60,0,dist)
        PS1=convert_c(100,0,PS)
        # PS1=convert_c(100,0,12)
        p= 10*(0.2*dist1 + 0.714*PS1)
        msg=JobInfo()
        msg.task="GotoPS"
        msg.priority=p
        msg.x=x_ps
        msg.y=y_ps
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass