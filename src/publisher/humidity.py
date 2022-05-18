#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32
import random
import time
from std_msgs.msg import String

C_w = 0
humid_v=0

#related with weather,consatnt will change with weather
def weather_callback(msg):
    global C_w
    global humid_v
    E = random.random()
    w=str(msg.data)
    if w == 'rainy':
        C_w=100
        humid_v=E*C_w/2+50   ##humidity is in (50,100) when its raining
    else:
        C_w=50
        humid_v=E*C_w

def humidity_ind():
    rospy.Subscriber("/weather", String, weather_callback)
    pub = rospy.Publisher('humidity', Float32, queue_size=10)
    rospy.init_node('humidity_ind', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        time.sleep(1)
        msg=humid_v 
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        humidity_ind()
    except rospy.ROSInterruptException:
        pass
