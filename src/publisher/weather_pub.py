#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import random
#import numpy as np
import time



def weather_pub():
    pub = rospy.Publisher('weather', String, queue_size=10)
    rospy.init_node('weather_pub', anonymous=True)
    rate = rospy.Rate(10) # 100hz
    rospy.loginfo("node started, now publishing")

    #t=int(time.strftime('%H',time.localtime()))
    while not rospy.is_shutdown():
        time.sleep(3)
        w=random.choice(['clear','rainy','foggy','snowy'])
        msg=w
        rospy.loginfo(msg)
        pub.publish(msg)
        time.sleep(21)
        rate.sleep


if __name__ == '__main__':
    try:
        weather_pub()
    except rospy.ROSInterruptException:
        pass