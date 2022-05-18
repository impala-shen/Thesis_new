#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Float32
#import numpy as np
import random
import time
from std_msgs.msg import String

C_w = 0
visib_v = 0

#related with weather,consatnt will change with weather
def weather_callback(msg):
    global C_w
    global visib_v
    E = random.random()
    w=str(msg.data)
    if w == 'foggy':
        C_w=5
        visib_v=C_w*E  #visibility is between (0,5) when its foggy
    elif w == 'clear':
        C_w=10
        visib_v=C_w*E/2+5  #visibility is between (5,10) when its clean
    else:
        C_w=6
        visib_v=C_w*E/2+4  #visibility is between (4,7) in other weathers
    #print('C_w:%s' %(C_w))


def visibility_ind():
    rospy.Subscriber("/weather", String, weather_callback)
    pub = rospy.Publisher('visibility', Float32, queue_size=10)
    rospy.init_node('visibility_ind', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")

    
    while not rospy.is_shutdown():
        time.sleep(1)
        msg=visib_v
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        visibility_ind()
    except rospy.ROSInterruptException:
        pass
