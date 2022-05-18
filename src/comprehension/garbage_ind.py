#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32
import random
import time
from std_msgs.msg import String
from data_collector.msg import BasicInfo

x = 0
y = 0
type=''
weight=0
size=0
garbage_ind=''

def gar_callback(msg):
    global x
    global y
    global type
    global weight
    global size
    global garbage_ind

    #msg=BasicInfo()
    x = msg.x
    y = msg.y
    type = msg.type
    weight = msg.weight
    size = msg.size


    if type == 'plastic' and weight <=100:
        garbage_ind='Liftable plastic garbage detected'
    elif type == 'rubber' and weight <=100:
        garbage_ind='Liftable rubber garbage detected'
    else:
        garbage_ind='unknown garbage'

def garbage_ind():
    rospy.Subscriber("/G_sensor_info", BasicInfo, gar_callback)
    pub = rospy.Publisher('garbage_ind', String, queue_size=10)
    rospy.init_node('garbage_ind', anonymous=True)
    rate = rospy.Rate(100) # 100hz
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        time.sleep(1)
        msg=garbage_ind
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        garbage_ind()
    except rospy.ROSInterruptException:
        pass
