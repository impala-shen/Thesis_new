#!/usr/bin/env python

import math
from re import T
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
from data_collector.msg import JobInfo
from data_collector.msg import tasksList
from data_collector.msg import Projection
from data_collector.msg import BasicInfo

top_task = "Wait"
x = 100
y = 100
x_a = 0
y_a = 0
dist = 100


def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)


def Exe_T(msg):
    global top_task
    top_task = msg.topTask

def Exe_task_info(msg):
    global x, y
    x = msg.x
    y = msg.y

def agent_callback(msg):
    global x_a, y_a, dist
    x_a=msg.pose.pose.position.x
    y_a=msg.pose.pose.position.y
    dist = distance(x, y, x_a, y_a)



def main():
    rospy.init_node("Execution")
    rospy.Subscriber("/execute_task", Projection, Exe_T)
    rospy.Subscriber(top_task, JobInfo, Exe_task_info)
    rospy.Subscriber("/odom", Odometry, agent_callback)
    pub=rospy.Publisher('execution_dist', Int32, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        msg = dist
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass