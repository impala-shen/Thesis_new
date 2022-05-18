#!/usr/bin/env python

import math
# from tkinter import W
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from data_collector.msg import JobInfo
from data_collector.msg import AcciInfo
import time

dist=1
voice=''
x=0
y=0
risk_p = 0
Ss=0
w=2

def agent_callback(msg):
    global x, y
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y


def weather_callback(msg):
    global w
    weather = msg.data
    # W=1
    if weather == 'heavy rain' or "heavy fog" or "heavy snow":
        w = 5
    elif weather == 'clear':
        w=0
    elif weather == "rain":
        w=1
    else:
        w=2


def RC_callback(msg):
    global Ss
    RC = msg.data
    if RC == "soft soil":
        if (y>5 and y<10) or (y<-5 and y>-10):
            Ss=5
    else:
        Ss=0


def main():
    dist=1
    voice=''
    x=0
    y=0
    risk_p = 0
    Ss=0
    w=1
    rospy.init_node("Wait")
    rospy.Subscriber("/odom", Odometry, agent_callback)
    rospy.Subscriber("/route_condition", String, RC_callback)
    rospy.Subscriber("/weather_ind", String, weather_callback)
    pub=rospy.Publisher('Wait', JobInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")   
    
##sensor gives the infomation of the cloest garbage
    while not rospy.is_shutdown():
        # if risk_p > 0.6:
        #     p = 50
        # elif risk_p > 0.4:
        #     p = 30
        # elif risk_p > 0.2:
        #     p = 10
        # else:
        #     p=0
        # p= 10*(0.333*w + 0.42*Ss)
        p=0

        msg=JobInfo()
        msg.task="Wait"
        msg.priority=p
        msg.x=x
        msg.y=y
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass