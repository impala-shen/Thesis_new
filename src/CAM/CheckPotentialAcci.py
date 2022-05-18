#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
from data_collector.msg import JobInfo
from data_collector.msg import AcciInfo
import time

dist=38
voice=''
x=20
y=45
w=0
Ss=0


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

def info_callback(msg):
    global dist
    global voice
    global x,y
    dist=msg.dist
    voice=msg.voice
    x=msg.x
    y=msg.y

def weather_callback(msg):
    global w
    weather = msg.data
    # rospy.loginfo('shelter: %s', weather)
    w=2
    # if weather == 'heavy rain' or "heavy fog" or "heavy snow":
    #     w = 5
    # elif weather == 'clear':
    #     w=0
    # elif weather == "rain":
    #     w=1
    # else:
    #     w=2

def RC_callback(msg):
    global Ss
    RC = msg.data
    Ss=0
    # if RC == "soft soil":
    #     if (y>5 and y<10) or (y<-5 and y>-10):
    #         Ss=5
    # else:
    #     Ss=0

def main():
    global dist
    rospy.init_node("CheckPotentialAcci")
    rospy.Subscriber("/Acci_info", AcciInfo, info_callback)
    rospy.Subscriber("/weather_ind", String, weather_callback)
    rospy.Subscriber("/route_condition", String, RC_callback)
    pub=rospy.Publisher('CheckPotentialAccident', JobInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")   

    
##sensor gives the infomation of the cloest garbage
    while not rospy.is_shutdown():
        dist1=convert_c(60,0,dist)
        p= 10*(0.333*w + 0.2*dist1 + 0.420*Ss)
        # rospy.loginfo('PA: %s',w)
        # rospy.loginfo('PA: %s',Ss)
        if dist<10:
            if voice in {'good','safe','run out','time'}:
                p=0
            else:
                p=99  ##do call police task

        
        msg=JobInfo()
        msg.task="CheckPotentialAccident"
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