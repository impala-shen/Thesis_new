#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import random
#import numpy as np
#import time
import sys

def extent_pub():
    pub = rospy.Publisher('extent', String, queue_size=10)
    rospy.init_node('extent_pub', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")

    #pass arguments to node
    args = rospy.myargv(argv=sys.argv)
    if len(args) !=2:
        print('error: no extent provided')
        sys.exit(1)

    extent = args[1]


    while not rospy.is_shutdown():
        msg=extent

        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        extent_pub()
    except rospy.ROSInterruptException:
        pass
