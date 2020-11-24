# L2_drive.py

# Import Internal Programs
#import L2_inverse_kinematics as inv #calculates wheel parameters from chassis
import L3_storing as store
import L2_kinematics as kin    # calculates chassis parameters from wheels
import L2_speed_control as sc
import L2_obstacle as obs
import L2_ColorTarget as target
import L2_log as log
import L1_camera as cam
import L1_motors as m
import L1_EM as magnet 
import L1_LoadCellUART as cell
import L1_gamepad as pad

# Import External programs
import numpy as np
import time
import threading # only used for threading functions
import math
import csv
import random
#import rcpy
#import rcpy.motor as motor


def main():

  # INITIALIZE VARIABLES FOR CONTROL SYSTEM
  status = "Preping for pickup"
  log.stringTmpFile(status, "Final_status.txt")
  t0 = 0  # time sample
  t1 = 1  # time sample
  e00 = 0 # error sample
  e0 = 0  # error sample
  e1 = 0  # error sample
  dt = 0  # delta in time
  de_dt = np.zeros(2) # initialize the de_dt
  
  stored_items = 0
  
  r = 0.041 # radius of wheel
  l = 0.201 # distance to wheel
  
  target_pixel = np.array([None, None, 0, None, None])
  
  
  
  x = 0
  #y = 0
  
  
  #rcpy.set_state(rcpy.RUNNING)
  
  while stored_items < 3:
    # GET NEAREST OBJECT

    nearest = obs.nearest_point() # L2_obstacle nearest obstacle
    obstacleX = nearest[0]  # obstacle distance x
    obstacleY = nearest[1] - 0.089  # obstacle distance y with lidar offset
    # print("Dx: ", obstacleX)
    # print("Dy: ", obstacleY)
    
    status = "Searching"
    log.stringTmpFile(status, "Final_status.txt")
    if obstacleX > 0 and obstacleX < 0.30: # If approaching object
        status = "Obstacle Detected...Avoiding"
        log.stringTmpFile(status, "Final_status.txt")
      # PDTARGET FROM RANDOM ANGLE
        randDeg = random.randrange(5, 26, 1)  # random degree turn from 5 to 25
        print("Deg: ", randDeg)
        randRad = randDeg * (math.pi / 180) # convert to radians
        rotateTime = (1 * randRad) / 1.57 # rotation time based on turn amount
      
      # WILL ROTATE LEFT UNLESS OBJECT IS TO LEFT
        if(obstacleY > 0): # object to the left
            randRad = randRad * -1  # turn right
        
      # SOLVE FOR PHIDOTS FROM THETADOT AND XDOT
        A = np.array([[r / 2, r / 2], [-r / (2 * l), r / (2 * l)]]) 
        B = np.array([0, randRad/rotateTime])
        pdTargets = np.linalg.solve(A, B) # turning phidots (radians/s)
      
        startTime = time.time() # set starting time
        currentTime = 0 # initialize current time
      
        while currentTime < rotateTime: # turn for a certain amount of time

            kin.getPdCurrent() # capture latest phi dots & update global var
            pdCurrents = kin.pdCurrents # assign the global variable value to a local var
        
        # THIS BLOCK UPDATES VARIABLES FOR THE DERIVATIVE CONTROL
            t0 = t1  # assign t0
            t1 = time.time() # generate current time
            dt = t1 - t0 # calculate dt
            e00 = e0 # assign previous previous error
            e0 = e1  # assign previous error
            e1 = pdCurrents - pdTargets # calculate the latest error
            de_dt = (e1 - e0) / dt # calculate derivative of error

            currentTime = time.time() - startTime # track time elapsed
    
        # CALLS THE CONTROL SYSTEM TO ACTION
            sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)
            time.sleep(0.05) # this time controls the frequency of the controller
    
    else:
      image = cam.newImage()
      height, width, channels = image.shape
      target_pixel = target.colorTarget()
      radius = target_pixel[2]
      x = target_pixel[0]
      
      if radius > 0 and x != -1:
        status = "Item Detected"
        log.stringTmpFile(status, "Final_status.txt")
        #time.sleep(0.5)
        print("Radius: \t", radius)
        magnet.em_on()
        status = "Picking Up item(s)"
        log.stringTmpFile(status, "Final_status.txt")
        time.sleep(0.5)
        status = "Item has been picked up"
        log.stringTmpFile(status, "Final_status.txt")
        print("Resuming search")
        m.MotorL(0)
        m.MotorR(0)
        store.storing()
        time.sleep(0.55)
        store.checking()
        cell.setup()
        status = "storing items...checking tray"
        log.stringTmpFile(status, "Final_status.txt")
        
        print("checking tray")
        buff1 = cell.loadRead()
        time.sleep(1)
        print("dropping now")
    
        # turn magnet off
        magnet.em_off()
        time.sleep(5)
        cell.setup()
        buff2 = cell.loadRead()
        
        print("checking tray")
        print("buff2 \t", buff2, "buff1 \t", buff1, "difference \t", buff2 - buff1)

        if  (buff2 - buff1) > 5000:
          print("buff2 \t", buff2, "buff1 \t", buff1, "difference \t", buff2 - buff1)
          stored_items = stored_items + 1
          store.complete()
          status = "retract tray...Storage Complete"
          time.sleep(0.55)
          store.checking()
          log.stringTmpFile(status, "Final_status.txt")
          #time.sleep(2)
        else: 
          # keep magnet on
          #magnet.em_on
          store.complete()
          time.sleep(0.55)
          #status = "retract tray...Failed Storage"
          #log.stringTmpFile(status, "Final_status.txt")
          store.checking()
          status = "Retract Tray...Failed to store"
          log.stringTmpFile(status, "Final_status.txt")
        time.sleep(2)
        # halt servos to check tray 
        store.checking()
        status = "Resuming Search"
        log.stringTmpFile(status, "Final_status.txt")
        time.sleep(2)
        
      pdTargets = np.array([5, 5]) # Input requested PhiDots (radians/s)
      kin.getPdCurrent() # capture latest phi dots & update global var
      pdCurrents = kin.pdCurrents # assign the global variable value to a local var
              
      t0 = t1  # assign t0
      t1 = time.time() # generate current time
      dt = t1 - t0 # calculate dt
      e00 = e0 # assign previous previous error
      e0 = e1  # assign previous error
      e1 = pdCurrents - pdTargets # calculate the latest error
      de_dt = (e1 - e0) / dt # calculate derivative of error
                             
      sc.driveClosedLoop(pdTargets, pdCurrents, de_dt)
      time.sleep(0.05) # this time controls the frequency of the controller
    
    log.tmpFile(pdCurrents[0], "Final_PDLEFT.txt")
    log.tmpFile(pdCurrents[1], "Final_PDRIGHT.txt")
    log.tmpFile(stored_items, "Final_Stored.txt")
  
  m.MotorR(0)
  m.MotorL(0)
  status = "Mission Complete"
  log.stringTmpFile(status, "Final_status.txt")
  time.sleep(5)
  status = "Please Give Us A Good Grade"
  log.stringTmpFile(status, "Final_status.txt")
  time.sleep(2)
    
if __name__ == '__main__':
  main()