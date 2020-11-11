# this file will let you use your gamepad to drive the SCUTTLE robot


import L2_speed_control as sc		# produced duty cycle from pldr & pldr
import L2_inverse_kinematics as inv	# converts xdot & tdot to pldr & pldl

import time

def manual_nav():
	c = inv.getPdTargets()			# takes the phi dot targets defined in 
									# L2_inverse & assigns it as c converts the
									# xdot & tdot values into pldr & pldl

	sc.driveOpenLoop(c)				# takes the pldl and pldr converted values  
									# into L2_speed_control & produces the Duty 
									# cycle based on pldr and pldl outputs 
									# the motor commands
while 1:
	manual_nav()					# continously reads the motor commands 
									# for the controller
									
	time.sleep(0.15)