# Lab6.py
# Team Number: 01
# Hardware TM: Aysheh Abushanab 
# Software TM: Nicholas B. Petta 
# Date: 10/22/20
# Code purpose:  

# Import Internal Programs
import L2_vector as veclab
import L2_log as log

# Import External programs
import numpy as np
import time

# DEFINE THE FUNCTIONS FOR THE PROGRAM
def task2():
    vect = veclab.getNearest()   
    scan = veclab.lidar.polarScan()                        # get a reading in meters and degrees
    valids = veclab.getValid(scan)                         # remove the bad readings
    vec = veclab.nearest(valids)
    dist = vec[0]                  # left phi dot value from getPdCurrent
    ang = vec[1]                  # rigth phi dot value from getPDCurrent
  
    dy = (dist*np.sin(ang))
    
    dx = (dist*np.cos(ang))
    log.uniqueFile(dist, "distance.txt")
    log.uniqueFile(ang, "angle.txt")
    log.uniqueFile(dx, "dx.txt")
    log.uniqueFile(dy, "dy.txt")
    print("Distance [m]\t", dist,"\t", "Angle [deg]\t", ang, "\t","dx [m]\t",  dx, "\t","dy [m]\t", dy)

# UNCOMMENT THE LOOP BELOW TO RUN THE PROGRAM CONTINUOUSLY
while 1:
    task2()
    time.sleep(0.2) # delay a short period
