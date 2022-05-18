#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from data_collector.msg import BasicInfo
from data_collector.msg import JobInfo
from std_msgs.msg import String
import time

global x_o, y_o
x_o=30
y_o=0
value=0
dist=60
w=0


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

def G_info_callback(msg):
    global size
    global x
    global y
    global dist
    global value
    size=msg.size  
    x=msg.x
    y=msg.y
    type=msg.type
    dist=msg.dis
    if type == 'plastic':
        t_v=1
    elif type == 'rubber':
        t_v=2
    else:
        t_v=0
    value = size * t_v

def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)

def agent_callback(msg):
    global dist
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    dist = distance(x,y,x_o,y_o)

def weather_callback(msg):
    global w
    weather = msg.data
    if weather == 'heavy rain' or "heavy fog" or "heavy snow":
        w = 5
    elif weather == 'clear':
        w=0
    else:
        w=2


def main():
    global dist
    rospy.init_node("explore")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    rospy.Subscriber("/G_sensor_info", BasicInfo, G_info_callback)
    rospy.Subscriber("/weather_ind", String, weather_callback)
    pub=rospy.Publisher('explore', JobInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")   
    
    while not rospy.is_shutdown():
        if value == 0:
            dist1=convert_c(60,0,dist)
            p= 10*(0.167*dist1 + 0.25*w)
        else:
            p=0
        msg=JobInfo()
        msg.task="explore"
        msg.priority=p
        msg.x=x_o
        msg.y=y_o
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass