#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from data_collector.msg import AcciInfo
import time
import sys



def main():
    rospy.init_node("LS_status")
    pub=rospy.Publisher('space_status', Int32, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        LS=87
        msg=LS
        rospy.loginfo('storage status:%f' %(msg))
        pub.publish(msg)
        rate.sleep()

    

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass