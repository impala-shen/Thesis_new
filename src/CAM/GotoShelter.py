#!/usr/bin/env python

import math
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
from data_collector.msg import JobInfo
from data_collector.msg import weatherInfo
import time


humid_v = 0
temp_v = 1
visib_v = 0
dist1 = 18
dist2 = 21
w=0
LS=74
PS=50

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

def weather_s_callback(msg):
    global humid_v
    global temp_v
    global visib_v
    humid_v = msg.humidity
    temp_v = msg.temperature
    visib_v = msg.visibility
    # rospy.loginfo(humid_v)

def weather_callback(msg):
    global w
    weather = msg.data
    # rospy.loginfo('shelter: %s', weather)
    w=1
    # if weather == 'heavy rain' or "heavy snow":
    #     w = 4
    # elif weather == 'clear':
    #     w=0
    # elif weather == "rain":
    #     w=1
    # else:
    #     w=0
    # rospy.loginfo('shelter: %s', w)

def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)

def agent_callback(msg):
    global dist1
    global dist2
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    x_ps = 0
    y_ps = 20
    x_d = 7
    y_d = 18
    dist1 = distance(x,y,x_ps,y_ps)
    dist2 = distance(x, y, x_d, y_d)
    # print("x=%f,y=%f" %(x,y))
    # print("distance to PowerStation=%f" %(dist))
    # rospy.loginfo("x=%f,y=%f" %(x,y))

def PS_callback(msg):
    global PS
    PS=msg.data



def main():
    global PS
    global LS,dist1,dist2
    rospy.init_node("GotoShelter")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    rospy.Subscriber("/weather_ind", String, weather_callback)
    rospy.Subscriber("/w_sensor_info", weatherInfo, weather_s_callback)
    rospy.Subscriber("/Power_status", Int32, PS_callback)
    pub=rospy.Publisher('GotoShelter', JobInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")   


##sensor gives the infomation of the cloest garbage
    while not rospy.is_shutdown():
        msg=JobInfo()
        if humid_v < 100 and temp_v>-20:
            p_ps = p_d = 0
        else:
            PS1=convert_c(100,0,94)
            LS1=convert_c(100,0,80)
            # rospy.loginfo("PS=%f,LS=%f" %(PS1,LS1))
            dist1_s=convert_c(60,0,dist1)
            dist2_s=convert_c(60,0,dist2)
            p_ps= 10*(0.333*w + 0.2*dist1_s + 0.286*PS1)
            p_d= 10*(0.333*w + 0.2*dist2_s + 0.286*LS1)
        if p_ps > p_d:
            msg.task="GotoShelter(PS)"
            msg.priority=p_ps
            msg.x = 0
            msg.y = 20
        else:
            msg.task="GotoShelter(dp)"
            msg.priority=p_d
            msg.x = 7
            msg.y = 18
        
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass