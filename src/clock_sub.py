#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int8
from rosgraph_msgs.msg import Clock
import time

def time_callback(msg):
    print("clock:%s" %(msg))
    # rospy.loginfo(msg)


def main():
    rospy.init_node("clock_sub")
    rospy.Subscriber("/clock", Clock ,time_callback)
    rospy.spin()

if __name__=='__main__':
    main()