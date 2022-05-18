#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import random
#import numpy as np
import time

def voice_pub():
    pub = rospy.Publisher('talking', String, queue_size=10)
    rospy.init_node('voice_pub', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")

    words=['drive','car','help','danger','police','good','shout','safe','oil','run out','time']

    #t=int(time.strftime('%H',time.localtime()))
    while not rospy.is_shutdown():
        talking=random.choice(words)
        msg = talking 
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        voice_pub()
    except rospy.ROSInterruptException:
        pass
