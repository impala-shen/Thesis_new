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


global check_flag, reward
PS=100
LS=100
size = 0
p_GPS=0
p_PG1=0
list=[]
PS_check=""
t_GPS='wait'
t_PG1='wait'
top_task = "GotoPS"
x = 0
y = 0 
x_a = 0
y_a = 0
reward = 0
check_PS_flag = 0
tasks_list = ["Wait", "Wait"]  ###initial settings

def Top_T(msg):
    global top_task
    global tasks_list
    tasks_list = msg.data
    top_task = tasks_list[0]

def Top_task_info(msg):
    global x, y
    x = msg.x
    y = msg.y

def agent_callback(msg):
    global x_a, y_a
    x_a=msg.pose.pose.position.x
    y_a=msg.pose.pose.position.y


def distance(x1,y1,x2,y2):
    xd=x1-x2
    yd=y1-y2
    return math.sqrt(xd*xd + yd*yd)


def Check_PS(msg):
    global PS
    global PS_check
    global check_PS_flag
    PS = msg

def check_PS_flag(x, y):
    x_p = 0
    y_p = 20
    d1 = distance(x_a, y_a, x, y)
    d2 = distance(x, y, x_p, y_p)
    d = d1+d2
    # if PS  < d:  ## PS=100-dist_T
    #     return False
    # else:
    #     return True
    return True
        
def gar_info_callback(msg):
    global size
    size = msg.size

def Check_leftS(msg):
    global LS
    LS = msg

def check_LS_flag(size):    
    # if top_task == "PickupG":
    #     if LS - size < 0:
    #         return False
    # else:
    #     return True
    return True


def main():
    rospy.init_node("Projection")
    rospy.Subscriber("/tasks_list", tasksList, Top_T)
    # rospy.Subscriber(top_task, JobInfo, Top_task_info)
    rospy.Subscriber("/odom", Odometry, agent_callback)
    rospy.Subscriber("/Power_status", Int32, Check_PS)
    rospy.Subscriber("/gar1_info", BasicInfo, gar_info_callback)
    rospy.Subscriber("/space_status", Int32, Check_leftS)
    pub=rospy.Publisher('execute_task', Projection, queue_size=10)
    # pub1=rospy.Publisher('reward', Int32, queue_size=10)
    # pub2=rospy.Publisher('pulishment', Int32, queue_size=10)
    rate= rospy.Rate(1)
    rospy.loginfo("node started, now publishing")
    
    while not rospy.is_shutdown():
        # if check_PS_flag == 0:  ###check if all pre-condition meet
        #     msg = top_task
        #     msg1 = 5
        #     pub1.publish(msg1)
        # else:
        #     tasks_list.pop(0)  ###remove first priority task due to pre-condition don't meet
        #     top_task = tasks_list[0]
        #     msg = top_task

        for top_task in tasks_list:
            rospy.Subscriber(top_task, JobInfo, Top_task_info)
            if check_PS_flag(x, y) and check_LS_flag(size):    ##make check return true, expandable
                # msg = top_task
                reward = 10
                break
            # else:
            #     tasks_list.pop[0]

        msg = Projection()
        msg.topTask = top_task
        msg.reward = reward
        rospy.loginfo(msg.topTask)
        print("Executable alternative:%s" %(top_task))
        print("Feedback reward:%s" %(reward))
        print("Execute alternative:%s" %(top_task)) 
        pub.publish(msg)
        rate.sleep()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass