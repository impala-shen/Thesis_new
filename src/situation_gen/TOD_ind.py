#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
import random
#import numpy as np
import time
import sys

time_v=0
TOD=''

def time_callback(msg):
    global time_v
    global TOD
    time_v=msg.data
    ##print('time = %s' %(time_v))
    if time_v<=19 and time_v>6:
        TOD = 'Daytime'
    else:
        TOD = 'Night'
    

def TOD_ind():
    rospy.Subscriber('/time', Int32, time_callback)
    pub = rospy.Publisher('TOD_ind', String, queue_size=10)
    rospy.init_node('TOD_ind', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")

    # #pass arguments to node
    # args = rospy.myargv(argv=sys.argv)
    # if len(args) !=2:
    #     print('error: no time provided')
    #     sys.exit(1)

    while not rospy.is_shutdown():
        time.sleep(1)
        msg=TOD
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        TOD_ind()
    except rospy.ROSInterruptException:
        pass
