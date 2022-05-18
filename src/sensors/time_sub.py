#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
import time


def time_callback(msg):
    print("current_time:%s" %(msg.data))
    # rospy.loginfo(msg)


def main():
    rospy.init_node("time_sub")
    rospy.Subscriber("/time", Int32 ,time_callback)
    rospy.spin()

if __name__=='__main__':
    main()