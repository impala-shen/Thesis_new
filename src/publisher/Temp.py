#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from std_msgs.msg import String
import math
import random
import time

# C_w = 0
t = 0
w = 'none'

#related with weather,consatnt will change with weather
def weather_callback(msg):
    global w
    # global C_w
    w=str(msg.data)
    # if w == 'snowy':
    #     C_w=10

    # elif w == 'clear':
    #     C_w=30
    # else:
    #     C_w=20

#related with time
def time_callback(msg):
    global t
    t = int(msg.data) 


def Temp_ind():
    rospy.Subscriber("/weather", String, weather_callback)
    rospy.Subscriber("/time", Int32 , time_callback)
    pub = rospy.Publisher('temperature', Float32, queue_size=10)
    rospy.init_node('Temp_ind', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")

    
    while not rospy.is_shutdown():
        if w == 'snowy':         ##temperature is between (-20,0) when its snowy
            C_w=20
            msg=C_w*(-math.sin(math.pi/24*t))
        elif w == 'clear':
            C_w=30
            msg=C_w*math.sin(math.pi/24*t)
        else:
            C_w=20
            msg=C_w*math.sin(math.pi/24*t)

        # msg=C_w*math.sin(math.pi/24*t) 
        time.sleep(1)
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        Temp_ind()
    except rospy.ROSInterruptException:
        pass
