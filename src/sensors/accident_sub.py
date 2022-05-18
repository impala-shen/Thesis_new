#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from data_collector.msg import AcciInfo
import time
import sys

x1=26
y1=7.6
dist=0
words_s=''


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
    #dist_a=distance(x,y,x_a,y_a)
    #print("x=%f,y=%f" %(x,y))
    #print("distance_accident=%f" %(dist_a))
    # rospy.loginfo("x=%f,y=%f" %(x,y))

def acci_callback(msg):
    global x1
    global y1
    global dist
    x1=msg.pose.pose.position.x
    y1=msg.pose.pose.position.y
    dist=distance(x,y,x1,y1)
    # print("x1=%f,y1=%f" %(x1,y1))
    # print("distance_accident=%f" %(dist))

def d_voice_callback(msg):
    global words
    words=msg
    #print('acoustics sensor:%s' %(words))

def s_voice_callback(msg):
    global words_s
    words_s=msg.data
    #print('acoustics sensor:%s' %(words_s))
    # if dist <= 10:
    #     print('acoustics sensor:%s' %(words))



def main():
    rospy.init_node("accident_sub")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    #rospy.Subscriber("/talking",String,acous_callback)
    rospy.Subscriber("/people_odom",Odometry,acci_callback)
    rospy.Subscriber("/danger_case",String,d_voice_callback)
    rospy.Subscriber("/safe_case",String,s_voice_callback)
    pub=rospy.Publisher('Acci_info', AcciInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        msg=AcciInfo()
        msg.x=x1
        msg.y=y1
        msg.dist= dist
        msg.voice=words_s
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

    #rospy.Subscriber("/danger_case",String,d_voice_callback)
    #rospy.Subscriber("/2_front_car/odom",Odometry,car2_callback)
    ##rospy.Subscriber("/weather",String,weather_callback)
    # rospy.Subscriber("/internal_state", Int8 ,internal_state_callback)
    # rospy.Subscriber("/time", Int8 ,time_callback)


    # #pass arguments to node
    # args = rospy.myargv(argv=sys.argv)
    # if len(args) !=2:
    #     print('error: no case provided')
    #     sys.exit(1)

    # ind_case = args[1]
    # if ind_case == 'bad':
    #     rospy.Subscriber("/talking",String,badcase_callback)
    # if ind_case == 'good':
    #     rospy.Subscriber("/talking",String,goodcase_callback)
    

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass