#! /usr/bin/env python
# -*- coding:utf-8 -*-
#http://wiki.ros.org/turtlesim/Tutorials/Rotating%20Left%20and%20Right

import rospy
from geometry_msgs.msg import Twist, Vector3
import math


PARTE = 0

relative_angle = math.radians(90)

angular_speed = math.pi/10

if __name__ == "__main__":
    rospy.init_node("roda_exemplo")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=3)

    try:
        while not rospy.is_shutdown():

        	if PARTE == 0: # reto 

	        	t0 = rospy.Time.now().to_sec()
	        	while (rospy.Time.now().to_sec() - t0) < 6:
		            vel = Twist(Vector3(0.1,0,0), Vector3(0,0,0))
		            pub.publish(vel)



	        	PARTE = 1

	        if PARTE == 1:

	        	current_angle = 0
	        	t0 = rospy.Time.now().to_sec()

	        	while (current_angle < relative_angle):
		        	vel = Twist(Vector3(0,0,0), Vector3(0,0,angular_speed))
			        pub.publish(vel)
		        	t1 = rospy.Time.now().to_sec()
  	         		current_angle = angular_speed*(t1-t0)



	        	PARTE = 0

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")