#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Float32
import random
import time
from std_msgs.msg import String
from data_collector.msg import weatherInfo

C_w = 0
humid_v=0
lumin_v=0
temp_v=0
visib_v=0
weather_ind='clear'

def w_sensor_callback(msg):
    global humid_v
    global lumin_v
    global temp_v
    global visib_v
    global weather_ind

    # msg=weatherInfo()
    humid_v = msg.humidity
    lumin_v = msg.luminance
    temp_v = msg.temperature
    visib_v = msg.visibility
    weather_ind='fog'


    # if humid_v<50 and temp_v<30 and temp_v>0 and visib_v>5:
    #     weather_ind='clear'
    # elif humid_v>80:
    #     weather_ind='heavy rain'
    # elif humid_v<80 and humid_v>50:
    #     weather_ind='rain'
    # elif humid_v<50 and temp_v<30 and temp_v>0 and visib_v<2.5:
    #     weather_ind='heavy fog'
    # elif visib_v<5:
    #     weather_ind='fog'
    # elif temp_v<0 and visib_v<3:
    #     weather_ind='heavy snow'
    # elif temp_v<0:
    #     weather_ind='snow'
    # else:
    #     weather_ind='clear'

def weather_ind():
    # weather_ind='clear'
    rospy.Subscriber("/w_sensor_info", weatherInfo, w_sensor_callback)
    pub = rospy.Publisher('weather_ind', String, queue_size=10)
    rospy.init_node('weather_ind', anonymous=True)
    rate = rospy.Rate(1) # 100hz
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        time.sleep(1)
        msg=weather_ind
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        weather_ind()
    except rospy.ROSInterruptException:
        pass
