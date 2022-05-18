#!/usr/bin/env python

import rospy, tf, random
import tf_conversions
from gazebo_msgs.srv import DeleteModel, SpawnModel
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import *
from nav_msgs.msg import Odometry
import  math

import numpy as np

heard=''

def safe_case_callback(msg):
    global heard
    words=msg.data
    #if dist <= 10:
    if words in {'good','safe','run out','time'}:
        heard=words
    
def safe_case_ind():
    rospy.Subscriber("/talking",String,safe_case_callback)
    pub = rospy.Publisher('safe_case', String, queue_size=10)
    pub1 = rospy.Publisher('people_odom', Odometry, queue_size=10)
    rospy.init_node('safe_case_ind',anonymous=True)
    rate = rospy.Rate(1)
    rospy.loginfo('node started, now publishing')

    rospy.wait_for_service("gazebo/delete_model")
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    print("Got it.")
    delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)


    people = rospy.get_param('~people')
    with open(people, "r") as f:
        obstacle_product_xml = f.read()

    # barrier_poses = [[25, 2],
    #                  [5, -0.5]
    #                  [10, 6],
    #                  [15, -5],
    #                  [-5, 0.9],
    #                  [-2,1],
    #                  [60, -6],
    #                  ]

    pos = [random.randint(25,28),random.randint(6,8)]

    # barrier_poses = []
    # for i, pos in enumerate(barrier_poses):
    orient = Quaternion(*tf_conversions.transformations.quaternion_from_euler(0.0, 0.0, np.random.uniform(-np.pi/2., np.pi/2)))
    pos_noise = np.random.uniform(-0.2, 0.2,size=2)
    item_pose = Pose(Point(x=pos[0]+pos_noise[0],
                            y=pos[1]+pos_noise[0],
                            z=0),
                            orient)

    spawn_model("people_{}".format(2), obstacle_product_xml, "", item_pose, "world")

    while not rospy.is_shutdown():
        msg2=Odometry()
        msg2.pose.pose.position.x=pos[0]
        msg2.pose.pose.position.y=pos[1]
        msg1=heard
        rospy.loginfo(msg1)
        rospy.loginfo(msg2)
        pub.publish(msg1)
        pub1.publish(msg2)
        rate.sleep
# def voice_callback(msg):
#     words=msg.data
#     #if dist <= 10:
#     if words in {'help','danger','police','shout'}:
#         heard=words



if __name__ == '__main__':

    try:
        safe_case_ind()

    except rospy.ROSInterruptException:
        pass