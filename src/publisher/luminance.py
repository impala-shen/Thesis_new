#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from std_msgs.msg import String
import random
import time
import math

#C_w = 10
C_w = 0
lum = 0 
pub = rospy.Publisher('luminance', Float32, queue_size=10)

#related with weather,consatnt will change with weather
def weather_callback(msg):
    global C_w
    w=str(msg.data)
    if w == 'clear' or w == 'snowy':
        C_w=10
    if w == 'rainy':
        C_w=7
    if w == 'foggy':
        C_w=6
    #print('weather:%s' %(w))
    #print('C_w1=:%s' %(C_w))
    
#related with time
def time_callback(msg):
    global t
    global lum
    #rospy.Subscriber("/weather", String, weather_callback)
    #rate = rospy.Rate(100) # 100hz
    t = int(msg.data)  
    #print('time: %s'%(t)) 
    #print('C_w2=:%s' %(C_w))
    lum=C_w*math.sin(math.pi/24*t)
    rospy.loginfo(lum)
    pub.publish(lum)



def lumin_ind():
    rospy.init_node('lumin_ind', anonymous=True)
    rospy.Subscriber("/weather", String, weather_callback)
    rospy.Subscriber("/time", Int32 , time_callback)
    #pub = rospy.Publisher('luminance', Int32, queue_size=10)
    #rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")
    pub.publish(lum)
    rospy.spin()


if __name__ == '__main__':
    try:
        lumin_ind()
    except rospy.ROSInterruptException:
        pass
