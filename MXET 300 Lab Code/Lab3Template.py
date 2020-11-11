# L3_drivingPatterns.py
# Team Number: 4
# Hardware TM: Aysheh Abushanab	
# Software TM: Nicholas B. Petta
# Date: 09/17/20
# Code purpose: 
#				Inputting the xd, td, and duration values determined by 
#				calculation were placed into this code. The 6 motions 
#				are identified that allow the robot to move forward for 
#				distance of d1, and turn at an arc, and make 2 sharp turn
#				This code allows the robot to complete a set of motions 
#				in which the robot returns to its original position.
# indicate d1 and d2 distances: 
#								d1 = 2 meters 
#								d2 = 3 meters 

# Import Internal Programs
import L2_speed_control as sc
import L2_inverse_kinematics as inv

# Import External programs
import numpy as np
import time

def task2():
	myVelocities = np.array([0.2, 0]) # go forward for a distance of d1
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(10) # input your duration (s)
	
	myVelocities = np.array([0.4, 0.133]) # ARC TURN of a length (L) = d2
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(11.78) # input your duration (s)
	
	myVelocities = np.array([0.3, 0]) # go forward for a distance of d1
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(6.6) # input your duration (s)
	
	myVelocities = np.array([0, 0.131]) # SHARP 90 degree turn 1
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(6) # input your duration (s)
	
	myVelocities = np.array([0.4, 0]) # go forward for a distance of d2
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(7.5) # input your duration (s)
	
	myVelocities = np.array([0, 0.196]) # SHARP 90 degree turn 2
	myPhiDots = inv.convert(myVelocities)
	sc.driveOpenLoop(myPhiDots)
	time.sleep(4) # input your duration (s)
	
while 1:
    task2()
    time.sleep(0.2)
