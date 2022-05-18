#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import random
import time

def internal_state_ind():
    pub = rospy.Publisher('internal_state', String, queue_size=10)
    rospy.init_node('internal_state_ind', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")

    INT_S = 'garbage pick up'
    while not rospy.is_shutdown():
        msg = INT_S 
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        internal_state_ind()
    except rospy.ROSInterruptException:
        pass
