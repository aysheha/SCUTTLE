# Lab4Template.py
# Team Number: 01
# Hardware TM: Aysheh Abushanab 
# Software TM: Nicholas B. Petta 
# Date: 09/24/20
# Code purpose: The purpose of this code is to capture the values & 
#               understanding of the SCUTTLE wheels and frame of the 
#               robot. This allows the user to produce a GUI that identifies 
#               the phi dot L, phi dot R, x dot and theta dot values when moving
#               the robot. 

# Import Internal Programs
import L2_kinematics as kin
import L2_log as log

# Import External programs
import numpy as np
import time

# DEFINE THE FUNCTIONS FOR THE PROGRAM
def task2():
  wheels = kin.getPdCurrent()       
  wheelL = wheels[0]                  # left phi dot value from getPdCurrent
  wheelR = wheels[1]                  # rigth phi dot value from getPDCurrent
  
  frames = kin.getMotion()
  speed = frames[0]                   # x dot value from getMotion
  angle = frames[1]                   # theta dot value from getMotion
  
  log.uniqueFile(wheelR, "phidotR.txt")
  log.uniqueFile(wheelL, "phidotL.txt")
  print("Left Wheel, Right Wheel: \t", wheelL, wheelR, "x dot, theta dot \t", speed, angle)
  log.uniqueFile(speed, "xdot.txt")
  log.uniqueFile(angle, "thetadot.txt")

# UNCOMMENT THE LOOP BELOW TO RUN THE PROGRAM CONTINUOUSLY
while 1:
    task2()
    time.sleep(0.2) # delay a short period
