# L2_drive.py

# Import Internal Programs
#import L2_inverse_kinematics as inv #calculates wheel parameters from chassis
import L2_kinematics as kin    # calculates chassis parameters from wheels
import L2_speed_control as sc
import L2_obstacle as obs
import L2_ColorTarget as target
import L1_camera as cam
import L1_motors as m
import L1_EM as magnet 

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
  print("Preping for pickup")
  t0 = 0  # time sample
  t1 = 1  # time sample
  e00 = 0 # error sample
  e0 = 0  # error sample
  e1 = 0  # error sample
  dt = 0  # delta in time
  de_dt = np.zeros(2) # initialize the de_dt
  
  r = 0.041 # radius of wheel
  l = 0.201 # distance to wheel
  
  target_pixel = np.array([None, None, 0, None, None])
  band = 50
  
  tc = 90
  tf = 6
  tp = 65
  
  x = 0
  y = 0
  
  duty_l = 0
  duty_r = 0
  scale_t = 1.2
  scale_d = 0.8
  motor_r = 2
  motor_l = 1
  found_obj = False
  first_time = True
  #rcpy.set_state(rcpy.RUNNING)
  
  while 1:
    # GET NEAREST OBJECT
    first_time = True
    nearest = obs.nearest_point() # L2_obstacle nearest obstacle
    obstacleX = nearest[0]  # obstacle distance x
    obstacleY = nearest[1] - 0.089  # obstacle distance y with lidar offset
    # print("Dx: ", obstacleX)
    # print("Dy: ", obstacleY)
    
    print("Searching")
    if obstacleX > 0 and obstacleX < 0.30: # If approaching object
    
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
    
    else: # continue straight unless 
      
            
        image = cam.newImage()
        height, width, channels = image.shape
        target_pixel = target.colorTarget()
        radius = target_pixel[2]
        x = target_pixel[0]
        print("Radius: \t", radius)
        
        if radius > 0 and x != -1:
            #and target_pixel[0] is not None
            if first_time:
                m.MotorL(0)
                m.MotorR(0)
                first_time = False
                time.sleep(0.5)
            print("Radius: \t", radius)
            found_obj = True
            x = int(x)
            if x > ((width/2) - (band/2)) and x < ((width/2) + (band/2)):
                time.sleep(1)
                magnet.em_on()
                print("Item Centered")
                duty = -1 *((radius-tp)/(tc-tp))
                print("slowly approach")
                # go to centered item
                if radius >= tp:
                    duty = ((radius-tp)/(tc-tp)) # back up
                    print("slowly approach")
                elif radius < tp:
                    duty = 1 - ((radius - tf)/(tp-tf))
                    duty = scale_d * duty
                    print("approaching item")
                    
                duty_r = duty
                duty_l = duty
                print("duty:\t", duty)
                print("Picking Up item(s)")

                print("Item has been picked up")

                print("Resuming search")
            elif x < ((width/2)-(band/2)): #turning right
                print("Turning Right")
                duty_r = round((x-0.5*width)/(0.5*width),2)
                duty_r = duty_r * scale_t
                duty_l = round((0.5*width-x)/(0.5*width),2)
                print("DutyL:", duty_l, "DutyR: ", duty_r)
                duty_l = duty_l * scale_t
            elif x > ((width/2)-(band/2)): # turning left
                print("Turning Left")
                duty_l = round((x-0.5*width)/(0.5*width),2)
                duty_l = duty_l * scale_t
                duty_r = round((0.5*width-x)/(0.5*width),2)
                duty_r = duty_r * scale_t
                print("DutyL:", duty_l, "DutyR: ", duty_r)
        
            if duty_r > 1:
                duty_r = 1
            elif duty_r < -1:
                duty_r = -1
            
            if duty_l > 1:
                duty_l = 1
            elif duty_l < -1:
                duty_l = -1
            
            duty_l = round(duty_l,2)
            duty_r = round(duty_r,2)
        
            m.MotorL(duty_l)
            m.MotorR(duty_r)
                
        else:
            found_obj = False
                
        if found_obj == False:
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
            
if __name__ == '__main__':
    main()