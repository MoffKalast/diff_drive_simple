cmake_minimum_required(VERSION 2.8.3)
project(diff_drive_simple)

find_package(catkin REQUIRED COMPONENTS
	roscpp
	rospy
	sensor_msgs
	std_msgs
	geometry_msgs
)

catkin_python_setup()

catkin_package(
	CATKIN_DEPENDS std_msgs sensor_msgs message_runtime
)