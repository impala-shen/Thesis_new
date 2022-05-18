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

def TOD_callback(msg):
    global t1
    t1=msg

def weather_callback(msg):
    global w_ind
    w_ind=msg.data
    ##think a way to calculate soil humidity

    #msg=BasicInfo()  
    # if w_ind == 'heavy rain' and t1>5:
    #     route_ind='soft soil'
    # elif w_ind == 'rain' and t1>10:
    #     route_ind='soft soil'
    # elif w_ind == 'snow' and t1>10:
    #     route_ind='icy soil'
    # elif w_ind == 'heavy snow' and t1>5:
    #     route_ind='icy soil'
    # else:
    #     route_ind='route is in good condition'

def route_ind():
    hum_ind=0
    icy_ind=0
    rospy.Subscriber('/time', String, TOD_callback)
    rospy.Subscriber("/weather_ind", String, weather_callback)
    pub = rospy.Publisher('route_condition', Int32, queue_size=10)
    rospy.init_node('route_condition', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        ##define a humidity indication for explain soft/dry soil
        if w_ind == 'heavy rain' and hum_ind<40:
            hum_ind=hum_ind+2
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'snow' and icy_ind<40:
            icy_ind=icy_ind+1
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'rain' and hum_ind<40:
            hum_ind=hum_ind+1
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'clear' and hum_ind>2:
            hum_ind=hum_ind-2
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'clear' and icy_ind>2:
            icy_ind=icy_ind-2
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'heavy snow' and icy_ind<40:
            icy_ind=icy_ind+2
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'fog' or w_ind == 'heavy fog' and hum_ind>1:
            hum_ind=hum_ind-0.5
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        elif w_ind == 'fog' or w_ind == 'heavy fog' and icy_ind>1:
            icy_ind=icy_ind-0.5
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))
        else:
            print('hum_ind = %s' %(hum_ind))
            print('icy_ind = %s' %(icy_ind))

    ##if humidity_ind is over 15, route condition is soft; is humidity is over 0, and 
    ##icy_ind is over 10, route is icy and slippery.
        if hum_ind > 20 and icy_ind<20:
            route_ind='soft soil'
        elif hum_ind>0 and icy_ind>15:
            route_ind='slippery road'
        elif icy_ind>20:
            route_ind='slippery road'
        else:
            route_ind='route is in good condition'
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
