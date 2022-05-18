#!/usr/bin/env python

from cmath import log10
import imp
import math
from re import T, X
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from std_msgs.msg import Int32
from data_collector.msg import JobInfo
from data_collector.msg import tasksList
from itertools import permutations
import time
import sys

current_t=["GotoPS"]
current_t0=''
Location=[(0,0)]
#try0= "Power_status"
PS=0
x=0
y=0

def Current_tasks(msg):
    global current_t
    global current_t0
    current_t=msg.data
    current_t0=current_t[0]
    # print("list:%s" %(current_t))
    # print("list[0]:%s" %(current_t0))
    # print("len(current_t)=%f" %(len(current_t)))
    # if len(current_t)>1:
    #     for i in range(0,len(current_t)):
    #       def goal_location_callback(msg):
    #           task = current_t[i]
    #           ###maybe publish action with location



def Power_status(msg):
    global PS
    PS=msg.data


def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)


def goal_location_callback(msg):
    global x
    global y
    # time.sleep(2)
    x=msg.x
    y=msg.y
    #print("x:%s" %(x))
    ###maybe publish action with location

def find_shortest_route(Location):
    global dist
    global L0
    L0=(7,1)
    dist=0   
    dist_min=9999 ##initial minmum distance should be large enough
    Plan_all=[]
    for p in permutations(Location):  ###list all the sequence
        Plan_all.append(p)
    print("Plan_all:%s" %(Plan_all))
    for k in Plan_all:
        # rospy.loginfo(k)
        for i in k:
            # rospy.loginfo(i)
            dist += distance(L0[0],L0[1],i[0],i[1])   ##maybe the wrong setting of distance fomat
            L0=i
        print("dist:%s" %(dist))
        if  dist<dist_min:
            k_min=k
            dist_min=dist
        dist=0
        L0=(7,1)
    rospy.loginfo(k_min)
    print("d_min:%s" %(dist_min))


    
#     #list.append(p_CPA)

# def Check_leftS(msg):
#     global p_GPS
#     global t_GPS
#     p_GPS=msg.priority
#     t_GPS=msg.task
#     #list.append(p_GPS)



def main():
    global Location
    rospy.init_node("Route_planner")
    rospy.Subscriber("/top_tasks", tasksList, Current_tasks)
    rospy.Subscriber("/Power_status", Int32, Power_status)

    rospy.Subscriber(current_t[0], JobInfo, goal_location_callback)
    # print("list[0]:%s" %(current_t[0]))
    # Location.append((x,y))
    pub1=rospy.Publisher('location', String, queue_size=10)
    # rospy.Subscriber("/p_GotoPS", JobInfo, Check_leftS)
    # pub=rospy.Publisher('first_priority', String, queue_size=10)
    rospy.loginfo(Location)

    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        if len(current_t)<=1:
            msg1=current_t0
        else:
            for i in range(0,len(current_t)):
                rospy.Subscriber(current_t[i], JobInfo, goal_location_callback)
                print("list[0]:%s" %(current_t[i]))
                #time.sleep(2)
                Location.append((x,y))
                msg1=current_t0
            #print("location:%s" %(Location))
            Location=[(3,3),(7,3),(9,3)]
            print("len:%s" %(len(Location)))
            find_shortest_route(Location)
        #rospy.loginfo(Location[0])
        pub1.publish(msg1)
        rate.sleep()
        Location=[]


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass