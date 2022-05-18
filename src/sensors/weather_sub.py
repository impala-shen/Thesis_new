#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from data_collector.msg import weatherInfo
import time

import csv



time=0
luminance=0
humidity=0
temperature=0
visibility=0
weather=''

def weather_callback(msg):
    global weather
    weather=msg.data
    #print("current_weather:%s" %(msg.data))
    # rospy.loginfo(msg)

def time_callback(msg):
    global time
    time=msg.data
    print("current_time:%s" %(msg.data))
    # rospy.loginfo(msg)

def lumin_callback(msg):
    # lum=[] ##store sensor value
    global luminance
    luminance=msg.data
    print("luminance sensor:%s" %(msg.data))
    # rospy.loginfo(msg)

def humidity_callback(msg):
    #humid_v=int(msg.data)
    global humidity
    humidity=msg.data
    print('humidity sensor:%s' %(msg.data))


def Temp_callback(msg):
    #temp_v=int(msg.data)
    global temperature
    temperature=msg.data
    print('temperature sensor:%s' %(msg.data))

def visib_callback(msg):
    #visib_v=float(msg.data)
    global visibility
    visibility=msg.data
    print('camera visibility:%s' %(msg.data))       


def main():
    rospy.init_node("weather_sub")
    rospy.Subscriber("/weather", String, weather_callback)
    rospy.Subscriber("/time", Int32 ,time_callback)
    rospy.Subscriber("/luminance", Float32 , lumin_callback)
    rospy.Subscriber("/humidity", Float32, humidity_callback)
    rospy.Subscriber("/temperature", Float32 ,Temp_callback)
    rospy.Subscriber("/visibility", Float32 ,visib_callback)
    pub=rospy.Publisher('w_sensor_info', weatherInfo, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    

    while not rospy.is_shutdown():
        msg=weatherInfo()
        msg.time=time
        msg.weather=weather
        msg.humidity=humidity
        msg.luminance=luminance
        msg.temperature=temperature
        msg.visibility=visibility
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass