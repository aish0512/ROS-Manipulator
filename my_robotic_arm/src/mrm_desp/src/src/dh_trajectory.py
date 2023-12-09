#!/usr/bin/env python3
import numpy as np
from math import pi
import rospy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import roboticstoolbox as rtb
import sys
from spatialmath.base import *
from spatialmath import SE3
import spatialmath.base.symbolic as sym

def perform_trajectory():
    rospy.init_node('dh_trajectory_publisher')
    contoller_name='/manu_controller/command'
    trajectory_publihser = rospy.Publisher(contoller_name,JointTrajectory, queue_size=10)
    
    link_1 = rtb.DHLink(a=0, alpha=pi/2, d=0)
    link_2 = rtb.DHLink(a=0.8, alpha=0, d=0)
    link_3 = rtb.DHLink(a=0.8, alpha=0, d=0)
    link_4 = rtb.DHLink(a=0, alpha=pi/2, d=0)
    link_5 = rtb.DHLink(a=0, alpha=pi/2, d=0)
    robot= rtb.DHRobot([link_1,link_2,link_3,link_4,link_5]) 
    argv = sys.argv[1:]

    panda_joints = ['joint_1','joint_2','joint_3', 'joint_4', 'joint_5']
    point = SE3(float(argv[0]), float(argv[1]), float(argv[2]) )
    point_sol = str(robot.ikine_LM(point))
    print("angles\n:", point_sol)

    start_index = point_sol.find("q=[") + 3
    end_index = point_sol.find("]")

    # Extract and split the q values string
    q_values_str = point_sol[start_index:end_index]
    q_values = [float(val) for val in q_values_str.split(",")]

    # Print the extracted q values
    print("Extracted q values:", q_values)

 
    rospy.loginfo("Goal Position set lets go ! ")
    rospy.sleep(1)


    trajectory_msg = JointTrajectory()
    trajectory_msg.joint_names = panda_joints
    trajectory_msg.points.append(JointTrajectoryPoint())
    trajectory_msg.points[0].positions = q_values
    trajectory_msg.points[0].velocities = [0.0 for i in panda_joints]
    trajectory_msg.points[0].accelerations = [0.0 for i in panda_joints]
    trajectory_msg.points[0].time_from_start = rospy.Duration(3)
    rospy.sleep(1)
    trajectory_publihser.publish(trajectory_msg)


if __name__ == '__main__':
    perform_trajectory()