#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32
import random
import time
from std_msgs.msg import String
from data_collector.msg import weatherInfo

t1=0
w_ind=''
route_ind=''
hum_ind=0
icy_ind=0
x1=0
y1=0

def acci_callback(msg):
    global x1
    global y1
    global dist
    x1=msg.pose.pose.position.x
    y1=msg.pose.pose.position.y




def weather_callback(msg):
    global w_ind
    w_ind=msg.data
    rospy.loginfo(w_ind)


def route_ind():
    hum_ind=0
    icy_ind=0
    rospy.Subscriber("/weather_ind", String, weather_callback)
    pub = rospy.Publisher('route_condition', String, queue_size=10)
    rospy.init_node('route_condition', anonymous=True)
    rate = rospy.Rate(1) # 100hz
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        ##define a humidity indication for explain soft/dry soil
        if w_ind == 'heavy rain' and hum_ind<40:
            hum_ind=hum_ind+2
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'snow' and icy_ind<40:
            icy_ind=icy_ind+1
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'rain' and hum_ind<40:
            if icy_ind>0:
                icy_ind=icy_ind-1
            hum_ind=hum_ind+1
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'clear' and hum_ind>2:
            hum_ind=hum_ind-2
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'clear' and icy_ind>2:
            icy_ind=icy_ind-2
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'heavy snow' and icy_ind<40:
            icy_ind=icy_ind+2
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'fog' or w_ind == 'heavy fog':
            if hum_ind>0:
                hum_ind=hum_ind-0.5
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'fog' or w_ind == 'heavy fog':
            if icy_ind>1:
                icy_ind=icy_ind-0.5
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))
        else:
            hum_ind=hum_ind
            icy_ind=icy_ind
            # print('hum_ind = %s' %(hum_ind))
            # print('icy_ind = %s' %(icy_ind))

    #if humidity_ind is over 15, and robot is on soil, the 
    # route condition is soft; if humidity is over 0, and 
    #icy_ind is over 10, route is icy and slippery.
        if hum_ind > 20 and icy_ind<20:
            route_ind='soft soil'
        elif hum_ind>0 and icy_ind>15:
            route_ind='slippery road'
        elif icy_ind>20:
            route_ind='slippery road'
        else:
            route_ind='route is in good condition'
        # route_ind='soft soil'

        time.sleep(1)
        msg=route_ind
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        route_ind()
    except rospy.ROSInterruptException:
        pass
