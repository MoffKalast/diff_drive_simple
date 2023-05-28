cmake_minimum_required(VERSION 2.8.3)
project(diff_drive_simple)

find_package(catkin REQUIRED COMPONENTS
    dynamic_reconfigure
    rospy
	sensor_msgs
	std_msgs
	geometry_msgs
    message_generation
)

generate_dynamic_reconfigure_options(
    config/DiffDriveSimple.cfg
)

generate_messages(
    DEPENDENCIES geometry_msgs std_msgs sensor_msgs
)

catkin_package(
    CATKIN_DEPENDS dynamic_reconfigure rospy geometry_msgs sensor_msgs std_msgs geometry_msgs
)

include_directories(
    ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
    src/diff_drive.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)