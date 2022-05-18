#!/usr/bin/env python

import math
import rospy
from data_collector.msg import BasicInfo
from data_collector.msg import JobInfo
from std_msgs.msg import String
import time

# size=7.5
# x=7
# y=3
# dist=8
# PS=50
# w=2
# type=''
# Ss=0
value=7.5
x=9
y=3
dist=2.8
Ss=0

dist2=5
value2=11
x2=9
y2=-8

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
    #print("distance_garbage=%f" %(dist))

def info_callback2(msg):
    global size2
    global x2
    global y2
    global dist2
    global value2
    size2=msg.size  
    x2=msg.x
    y2=msg.y
    type2=msg.type
    dist2=msg.dis
    value2 = size2
    #print("distance_garbage=%f" %(dist))

def RC_callback(msg):
    global Ss
    RC = msg.data
    if RC == "soft soil":
        if (y>5 and y<10) or (y<-5 and y>-10):
            Ss=3
    else:
        Ss=0



def main():
    global dist
    rospy.init_node("PickupGarbage")
    rospy.Subscriber("/G_sensor_info", BasicInfo, info_callback)
    rospy.Subscriber("/G_sensor_info1", BasicInfo, info_callback2)
    rospy.Subscriber("/route_condition", String, RC_callback)
    pub=rospy.Publisher('PickupG', JobInfo, queue_size=10)
    # pub1=rospy.Publisher('PickupG1', JobInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")   
    
##sensor gives the infomation of the cloest garbage
    while not rospy.is_shutdown():
        # p=float(98/dist+size/5)   ####remember to change
        dist1=convert_c(60,0,dist)
        value1=convert_r(30,0,value)
        p=0
        # p= 10*(0.2*dist1 + value1 + 0.16*Ss)
        msg=JobInfo()
        msg.task="PickupG1"
        msg.priority=p
        msg.x=x
        msg.y=y
        rospy.loginfo(msg)
        pub.publish(msg)

        # dist3=convert_c(60,0,dist2)
        # value3=convert_r(40,0,value2)
        # p1= 10*(0.2*dist3 + value3 + 0.16*Ss)
        # msg1=JobInfo()
        # msg1.task="PickupG2"
        # msg1.priority=p1
        # msg1.x=x2
        # msg1.y=y2
        # rospy.loginfo(msg1)
        # pub1.publish(msg1)

        # dist1=convert_c(60,0,dist)
        # value1=convert_r(40,0,value)
        # p= 10*(0.333*dist1 + value1 + 0.16*Ss)
        # msg=JobInfo()
        # msg.task="PickupG1"
        # msg.priority=p
        # msg.x=30
        # msg.y=0
        # rospy.loginfo(msg)
        # pub.publish(msg)

        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass