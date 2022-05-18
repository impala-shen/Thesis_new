#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int32
import random
#import numpy as np
import time

def time_pub():
    pub = rospy.Publisher('time', Int32, queue_size=10)
    rospy.init_node('time_pub', anonymous=True)
    rate = rospy.Rate(10) # 100hz
    rospy.loginfo("node started, now publishing")

    #t=int(time.strftime('%H',time.localtime()))
    while not rospy.is_shutdown():
        for t in range(0,24):
            msg = t 
            rospy.loginfo(msg)
            pub.publish(msg)
            time.sleep(1)
            rate.sleep()

if __name__ == '__main__':
    try:
        time_pub()
    except rospy.ROSInterruptException:
        pass