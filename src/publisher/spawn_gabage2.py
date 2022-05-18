#!/usr/bin/env python

import rospy, tf, random
import tf_conversions
from gazebo_msgs.srv import DeleteModel, SpawnModel
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import *
from data_collector.msg import BasicInfo

import numpy as np

def type2_pub():
    pub = rospy.Publisher('garbage2', String, queue_size=10)
    pub1= rospy.Publisher('gar2_info',BasicInfo,  queue_size=10)
    rospy.init_node('spawn_gabage2',anonymous=True)
    rate = rospy.Rate(100)
    rospy.loginfo('node started, now publishing')

    rospy.wait_for_service("gazebo/delete_model")
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    print("Got it.")
    delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
    spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)


    rubber = rospy.get_param('~rubber')
    with open(rubber, "r") as f:
        obstacle_product_xml = f.read()

    # barrier_poses = [[25, 2],
    #                  [5, -0.5]
    #                  [10, 6],
    #                  [15, -5],
    #                  [-5, 0.9],
    #                  [-2,1],
    #                  [60, -6],
    #                  ]

    pos = [random.randint(8,10),random.randint(2,6)]

    # barrier_poses = []
    # for i, pos in enumerate(barrier_poses):
    orient = Quaternion(*tf_conversions.transformations.quaternion_from_euler(0.0, 0.0, np.random.uniform(-np.pi/2., np.pi/2)))
    pos_noise = np.random.uniform(-0.2, 0.2,size=2)
    item_pose = Pose(Point(x=pos[0]+pos_noise[0],
                            y=pos[1]+pos_noise[0],
                            z=0),
                            orient)

    spawn_model("rubber_{}".format(2), obstacle_product_xml, "", item_pose, "world")
    
    p_r = 0.95 #density for rubber
    size = random.randint(7,10)
    weight = p_r*size  ##relate with type&size

    while not rospy.is_shutdown():
        msg2=BasicInfo()
        msg2.x=pos[0]
        msg2.y=pos[1]
        msg2.type = 'rubber'
        msg2.weight = weight
        msg2.size = size
        msg1='type2'
        rospy.loginfo(msg1)
        rospy.loginfo(msg2)
        pub.publish(msg1)
        pub1.publish(msg2)
        rate.sleep



if __name__ == '__main__':

    try:
        type2_pub()

    except rospy.ROSInterruptException:
        pass