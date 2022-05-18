#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from data_collector.msg import AcciInfo
import time
import sys

x1=0
y1=0
dist_T=0

def travelD_callback(msg):
    global dist_T
    dist_T=msg.data


def main():
    rospy.init_node("Power_status")
    rospy.Subscriber("/travelled_dis", Float64 , travelD_callback)
    pub=rospy.Publisher('Power_status', Int32, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        PS=100-dist_T
        # PS=23
        msg=int(PS)
        rospy.loginfo('Power status:%f' %(msg))
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