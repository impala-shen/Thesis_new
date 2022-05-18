#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32
import random
import time
from std_msgs.msg import String
from data_collector.msg import weatherInfo


cost=0
cost0=0
cost1=0
cost2=0


def TOD_callback(msg):
    global cost0
    TOD=msg.data
    if TOD == 'Night':
        cost0=2
    else:
        cost0=0
    print('cost0 = %s' %(cost0))
    

def weather_callback(msg):
    global cost1
    w_ind=msg.data
    ##think a way to calculate cost
    if w_ind == 'heavy rain':
        cost1=2
    elif w_ind == 'rain':
        cost1=1
    elif w_ind == 'snow':
        cost1=1
    elif w_ind == 'heavy snow':
        cost1=2
    elif w_ind == 'fog':
        cost1=1
    elif w_ind == 'heavy fog':
        cost1=2
    else:
        cost1=0
    print('cost1 = %s' %(cost1))

def route_c_callback(msg):
    global cost2
    r_c=msg.data
    ##think a way to calculate cost
    if r_c == 'soft soil':
        cost2=1
    elif r_c == 'slippery road':
        cost2=3
    else:
        cost2=0
    print('cost2 = %s' %(cost2))

def possible_acci():
    #cost_l=random.randint(0,3)  ##lucky constant
    rospy.Subscriber('/TOD_ind', String, TOD_callback)
    rospy.Subscriber("/weather_ind", String, weather_callback)
    rospy.Subscriber("/route_condition", String, route_c_callback)
    pub = rospy.Publisher('risk_p', Float32, queue_size=10)
    rospy.init_node('future_acci_pred', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        cost=cost0+cost1+cost2  ##total cost
        
        p=0.1*cost  ##possibility of accident happen

        # if p > 0.6:
        #     acci_pred='Danger! there is a big chance of accident.'
        # elif p > 0.4:
        #     acci_pred='Warning! accident might happen'
        # elif p > 0.2:
        #     acci_pred='Careful for accident'
        # else:
        #     acci_pred='Safe to drive'
        # time.sleep(1)
        msg = p
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        possible_acci()
    except rospy.ROSInterruptException:
        pass
