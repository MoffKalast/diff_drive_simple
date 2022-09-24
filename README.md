# Simple Diff Drive

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simpler alternative to the diff_drive_controller, for diff drive robots where wheel/propeller slip makes it it pointless to bother with that.

## Params

Note that min speed should be less or equal to max speed.

	<node name="diff_drive_node" pkg="diff_drive_simple" type="diff_drive.py" output="screen">
		<param name="min_speed" value="0.15" />
		<param name="max_speed" value="0.45" />
	<node>

## Subscribed Topics

 - `/cmd_vel` type of Twist, the velocity that needs to be muxed from linear.x and angular.z

## Published Topics

- `/diff_drive` type of JointState, publishes velocity for both wheels/propellers