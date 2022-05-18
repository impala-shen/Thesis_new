#!/usr/bin/env python

import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float32
import time
import sys


def lumin_callback(msg):
    #global opt_v
    opt_v=int(msg.data)
    if opt_v==0 or opt_v==10:
            print('luminance sensor:%s' %(opt_v))

def visib_callback(msg):
    #global visib_v
    visib_v=float(msg.data)
    if visib_v==0:
        print('camera visibility:%s' %(visib_v))

def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)

# def agent_callback(msg):
#     global x
#     global y
#     global dist
#     x=msg.pose.pose.position.x
#     y=msg.pose.pose.position.y
#     dist=distance(x,y,x_a,y_a)
#     print("x=%f,y=%f" %(x,y))


# def power_callback(msg):
#    power_0 = 100
#    power_c=power_0 - 0.5*dist
#    if power_c <= 20:
#        print("Low battery! Left battery =%f" %(power_c))


def main():
    rospy.init_node("misfunction_ind")

    #pass arguments to node
    args = rospy.myargv(argv=sys.argv)
    if len(args) !=2:
        print('error: no case provided')
        sys.exit(1)

    in_case = args[1]
    if in_case == 'defect_camera':
        rospy.Subscriber("/luminance", Int32 ,lumin_callback)
        rospy.Subscriber("/visibility", Float32 ,visib_callback)
    # if in_case == 'low battery':
    #     rospy.Subscriber("/talking",String,goodcase_callback)
    

    rospy.spin()

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass