#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from std_msgs.msg import String
import time
import sys

x1=0
y1=0
dist=0
dist_ps=0


def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)

def agent_callback(msg):
    global x
    global y
    global dist
    global dist_ps
    x_ps=0
    y_ps=20
    x_a=0
    y_a=0
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    dist=distance(x,y,x_a,y_a)
    dist_ps=distance(x,y,x_ps,y_ps)
    # print("x=%f,y=%f" %(x,y))
    # print("travelled distance=%f" %(dist))
    # rospy.loginfo("x=%f,y=%f" %(x,y))



def main():
    rospy.init_node("travelled_dis")
    rospy.Subscriber("/odom",Odometry,agent_callback)
    pub=rospy.Publisher('travelled_dis', Float64 , queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        msg=dist
        rospy.loginfo('travelled distance:%f' %(msg))
        rospy.loginfo("distance to PowerStation=%f" %(dist_ps))
        pub.publish(msg)
        rate.sleep()

    #rospy.Subscriber("/danger_case",String,d_voice_callback)
    #rospy.Subscriber("/2_front_car/odom",Odometry,car2_callback)
    ##rospy.Subscriber("/weather",String,weather_callback)
    # rospy.Subscriber("/internal_state", Int8 ,internal_state_callback)
    # rospy.Subscriber("/time", Int8 ,time_callback)


    # #pass arguments to node
    # args = rospy.myargv(argv=sys.argv)
    # if len(args) !=2:
    #     print('error: no case provided')
    #     sys.exit(1)

    # ind_case = args[1]
    # if ind_case == 'bad':
    #     rospy.Subscriber("/talking",String,badcase_callback)
    # if ind_case == 'good':
    #     rospy.Subscriber("/talking",String,goodcase_callback)
    

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass