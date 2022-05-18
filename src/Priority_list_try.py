#!/usr/bin/env python

import math
from os import ctermid
from re import T
import rospy
from data_collector.msg import JobInfo
from data_collector.msg import tasksList
from data_collector.msg import PoseList
from itertools import permutations
from data_collector.msg import Projection

p_CPA=7
p_GPS=1
p_PG1=0
p_D=0
x_PA=0
y_PA=0
x_PS=0
y_PS=20
x_D=0
y_D=0
x_G=0
y_G=0
x_o=0
y_o=0
p_W = 0
x_W = 0
y_W = 20
p_ST=0
x_ST=0
y_ST=0
tasks=[]
tasks_v=[]
tasks_l=[]
task_list=[]
t_CPA='wait0'
t_GPS='GotoPS'
t_PG1='wait2'
t_W='Wait'
t_ST = 'wait3'
t_D='wait4'
reward = 0
topTask = 'GotoPS'
p_o=0
t_o='wait5'
x_G2 = 0
y_G2=0

# class CTM:
#     def __init__(self, content, location, priority):
#         self.c = content
#         self.l = location
#         self.p = priority


def CheckPA_callback(msg):
    global p_CPA
    global t_CPA
    global x_PA,y_PA
    global dic
    p_CPA=msg.priority
    t_CPA=msg.task
    x_PA=msg.x
    y_PA=msg.y
    #list1=[]
    #list.append(p_CPA)

def GotoPS_callback(msg):
    global p_GPS
    global t_GPS
    global x_PS,y_PS
    p_GPS=msg.priority
    t_GPS=msg.task
    #list.append(p_GPS)

def PickG1_callback(msg):
    global p_PG1
    global t_PG1
    global x_G,y_G
    p_PG1=msg.priority
    t_PG1=msg.task
    x_G=msg.x
    y_G=msg.y
    # list.append(p_PG1)
    # print("list:%s" %(list))
def PickG2_callback(msg):
    global p_PG2
    global t_PG2
    global x_G2,y_G2
    p_PG2=msg.priority
    t_PG2=msg.task
    x_G2=msg.x
    y_G2=msg.y
    
def Wait_callback(msg):
    global p_W
    global t_W
    global x_W,y_W
    p_W=msg.priority
    t_W=msg.task
    x_W=msg.x
    y_W=msg.y

def GotoShelter_callback(msg):
    global p_ST
    global t_ST
    global x_ST,y_ST
    p_ST=msg.priority
    t_ST=msg.task
    x_ST=msg.x
    y_ST=msg.y

def GoDumping_callback(msg):
    global p_D
    global t_D
    global x_D,y_D
    p_D=msg.priority
    t_D=msg.task
    x_D=msg.x
    y_D=msg.y
    #list.append(p_GPS)

def explore_callback(msg):
    global p_o
    global t_o
    global x_o,y_o
    p_o=msg.priority
    t_o=msg.task
    x_o=msg.x
    y_o=msg.y

def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)

def find_shortest_route(Location):
    global dist, dist_min, k_min
    global L0
    L0=(0,0)
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
            dist += distance(L0[0],L0[1],i[0],i[1])  
            L0=i
        print("dist:%s" %(dist))
        if  dist<dist_min:
            k_min=k
            dist_min=dist
        dist=0
        L0=(0,0)

def reward_callback(msg):
    global reward, topTask
    reward = msg.reward
    topTask = msg.topTask



def main():
    rospy.init_node("Priority_list")
    rospy.Subscriber("/CheckPotentialAccident", JobInfo,CheckPA_callback)
    rospy.Subscriber("/GotoPS", JobInfo, GotoPS_callback)
    rospy.Subscriber("/PickupG", JobInfo, PickG1_callback)
    rospy.Subscriber("/PickupG1", JobInfo, PickG2_callback)
    rospy.Subscriber("/Wait", JobInfo, Wait_callback)
    rospy.Subscriber("/GoDumping", JobInfo, GoDumping_callback)
    rospy.Subscriber("/explore", JobInfo, explore_callback)
    rospy.Subscriber("/execute_task", Projection, reward_callback)
    rospy.Subscriber("/GotoShelter", JobInfo, GotoShelter_callback)
    pub = rospy.Publisher('tasks_list', tasksList, queue_size=10)
    # pub1=rospy.Publisher('locations', PoseList, queue_size=10)
    
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        global tasks
        global tasks_l
        global task_list
        new_dic={}
        p_value_list=[]
        p_values = []
        p_keys = []
        ########Expande new tasks here##########
        dic = {
            t_CPA: ((x_PA, y_PA), p_CPA),
            t_GPS: ((x_PS, y_PS), p_GPS),
            t_PG1: ((x_G, y_G), p_PG1),
            t_W: ((x_W, y_W), p_W),
            t_ST: ((x_ST, y_ST), p_ST),
            t_D: ((x_D, y_D), p_D),
            t_o: ((x_o, y_o), p_o),
        }
############ make feedback between Priority list with Projection #############        
        exe_T = {topTask: (dic[topTask][0], (dic[topTask])[1]+ reward)}  ###recieve reward from Projection
        dic.update(exe_T)
############ Priority list ##################        
        p_list = sorted(dic.items(), key=lambda r: r[1][1], reverse=True)
        print("priority list:%s" %(p_list)) 
        p_1=((p_list[0])[1])[1]
        for v in p_list:
            p_values.append(v[1])   ###list of locations and priority
            p_keys.append(v[0])   ###list of task content in order
            if (v[1])[1]>p_1-5:
                task_cv=v[1]
                task_c=v[0]
                new_dic[task_c] = task_cv[0]
            tasks_l = list(new_dic.values())
            tasks = list(new_dic.keys())
        print("list1:%s" %(new_dic))  
#############Route Planner###########
        if len(tasks)>1:   ###check whether there are similar priority tasks
            find_shortest_route(tasks_l)
            for l in k_min:
                t = list(new_dic.keys())[list(new_dic.values()).index(l)]
                task_list.append(t)
            msg = tasksList()
            msg = task_list
            rospy.loginfo("list2:%s", msg)
            pub.publish(msg)
#########################################            
        else:      ###if there is only one top task
            msg = p_keys
            rospy.loginfo("list:%s",msg)
            pub.publish(msg)
            
        rate.sleep()
        task_list=[]
    

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass