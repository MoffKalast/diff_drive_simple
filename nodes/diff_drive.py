#!/usr/bin/env python3
import rospy
import time
import math
import sys

from std_msgs.msg import Header, Float32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

from dynamic_reconfigure.server import Server
from diff_drive_simple.cfg import DiffDriveDynConf

def clamp(val, minval, maxval):
	if val < minval:
		return minval
	if val > maxval:
		return maxval
	return val

def map(v, in_min, in_max, out_min, out_max):
	v = clamp(v, in_min, in_max)
	return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

class DiffDrive:
	def __init__(self):
		rospy.init_node('diff_drive_node')

		self.SPEED_MIN = rospy.get_param('~min_speed', 0.0)
		self.SPEED_MAX = rospy.get_param('~max_speed', 1.0)

		# won't ever go faster than this
		self.max_sub = rospy.Subscriber("diff_drive/max_speed", Float32, self.max_callback)

		# non-zero messages won't go slower than this (to prevent motor stall)
		self.min_sub = rospy.Subscriber("diff_drive/min_speed", Float32, self.min_callback)

		self.cmdsub = rospy.Subscriber("cmd_vel", Twist, self.velocity)
		self.wheel_pub = rospy.Publisher("diff_drive", JointState, queue_size=1)

		self.reconfigure_srv = Server(DiffDriveDynConf, dynamic_reconfigure_callback)

		rospy.loginfo("Diff Drive Ready")

	def dynamic_reconfigure_callback(self, config, level):
		print(config)
		print(level)

		return config

	def min_callback(self, msg):
		if msg.data > 0.0 and msg.data <= self.SPEED_MAX:
			self.SPEED_MIN = msg.data

	def max_callback(self, msg):
		if msg.data >= self.SPEED_MIN:
			self.SPEED_MAX = msg.data

	def velocity(self, msg):

		left_vel = 0.0
		right_vel = 0.0

		if msg.angular.z != 0 or msg.linear.x != 0:
			left, right = self.diffdrive(msg.angular.z, msg.linear.x)

			left_spd = clamp(abs(left), self.SPEED_MIN, self.SPEED_MAX)
			right_spd = clamp(abs(right), self.SPEED_MIN, self.SPEED_MAX)

			left_vel = math.copysign(left_spd, left)
			right_vel = math.copysign(right_spd, right)

		state = JointState()
		state.name = ["left_wheel", "right_wheel"]
		state.velocity = [left_vel, right_vel]
		self.wheel_pub.publish(state)


	def diffdrive(self, x,  y):

			# First Compute the angle in deg
			# First hypotenuse
			z = math.sqrt(x * x + y * y)

			# angle in radians
			rad = math.acos(math.fabs(x) / z)

			# and in degrees
			angle = rad * 180 / math.pi

			# Now angle indicates the measure of turn
			# Along a straight line, with an angle o, the turn co-efficient is same
			# this applies for angles between 0-90, with angle 0 the coeff is -1
			# with angle 45, the co-efficient is 0 and with angle 90, it is 1
			tcoeff = -1 + (angle / 90) * 2
			turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
			turn = round(turn * 100, 0) / 100

			# And max of y or x is the movement
			mov = max(math.fabs(y), math.fabs(x))

			# First and third quadrant
			if (x >= 0 and y >= 0) or (x < 0 and y < 0):
				rawLeft = mov
				rawRight = turn
			else:
				rawRight = mov
				rawLeft = turn

			if y < 0:
				return [-rawLeft, -rawRight]

			return [rawRight, rawLeft]

try:
	drive = DiffDrive()
	rospy.spin()
except Exception as e:
	print(e)
