# L3_pickup.py
# This program activates the EM, once metal item(s) have been identified, and 
# centers the SCUTTLE allow the SCUTTLE to move forward and pick up the metal items
# Access nodered at 192.168.8.1:1880 (by default, it's running on the Blue)

# SENSORS used: Load Cell [raw adc] & computer vision (center metal items)
# ACTUATORS used: EM is activated & motor wheels
# Mission Status: "Prepping for Pickup", "Picking Up", "Item has been Picked Up"
# Error Status: "Failed to Pickup"

#print("LOADING libraries")
# Import Internal Programs
import L1_EM as magnet
import L1_gpio as gpio
# import L2_speed_control as sc
# import L2_drive as drive

#print("LOADING external programs")
# Import External programs
import cv2              # For image capture and processing
import argparse         # For fetching user arguments
import numpy as np      # kernel
import time             # 
#print("FINISHED loading libraries")

#print("LOADING rcpy.")
import rcpy             # import rcpy library
import rcpy.motor as motor  # import rcpy motor module
#print("FINISHED loading libraries")

# camera 
camera_input = 0  # Define camera input. Default=0. 0=/dev/video0
size_w  = 330   # Resized image width. This is the image width in pixels.
size_h = 220	# Resized image height. This is the image height in pixels.

# Color Range, described in HSV
v1_min = 165    # min H value day(145) night (130)
v2_min = 100    # min S value day(100) night (95)
v3_min = 85     # min V value day(85) night (85)

v1_max = 220    # max H value day(220) night (180)
v2_max = 220    # max S value day(220) night (185)
v3_max = 255    # max V value day(255) night (185)

# RGB or HSV
filter = 'HSV'  # Use HSV to describe pixel color values
gpio.write(0, 0, 1)

# Run the main loop
def main():
    print("PREPPING for Pickup")
    camera = cv2.VideoCapture(camera_input)     # Define camera variable
    camera.set(3, size_w)                       # Set width of images that will be retrived from camera
    camera.set(4, size_h)                       # Set height of images that will be retrived from camera

    # reduced tc value to 0, allows robot to move over 
    tc = 70     # Too Close     - Maximum pixel size of object to track
    tf = 6      # Too Far       - Minimum pixel size of object to track
    tp = 65     # Target Pixels - Target size of object to track

    band = 30   # range of x considered to be centered

    x = 0  # will describe target location left to right
    y = 0  # will describe target location bottom to top
    radius = 0  # estimates the radius of the detected target
    duty_l = 0 # initialize motor with zero duty cycle
    duty_r = 0 # initialize motor with zero duty cycle

    #print("initializing RCPY...")
    rcpy.set_state(rcpy.RUNNING)        # initialize the rcpy library
    #print("finished initializing rcpy.")
    
    # obtain color tracking phi dot values 

    print("Magnet On")
    try:
        print("Initial Prep")
        while rcpy.get_state() != rcpy.EXITING:
            if rcpy.get_state() == rcpy.RUNNING:
                scale_t = 0.9	# a scaling factor for speeds
                scale_d = 0.9	# a scaling factor for speeds
                motor_r = 2 	# Right Motor assigned to #2
                motor_l = 1 	# Left Motor assigned to #1

                ret, image = camera.read()  # Get image from camera
                height, width, channels = image.shape   # Get size of image
                if not ret:
                    break
                if filter == 'RGB':                     # If image mode is RGB switch to RGB mode
                    frame_to_thresh = image.copy()
                else:
                    frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # Otherwise continue reading in HSV

                thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))   # Find all pixels in color range
                kernel = np.ones((5,5),np.uint8)                            # Set gaussian blur strength.
                mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)     # Apply gaussian blur
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]     # Find closed shapes in image
                center = None   # Create variable to store point
                # locate item center point "prepping for pickup"
                
                if len(cnts) > 0:   # If more than 0 closed shapes exist
                    c = max(cnts, key=cv2.contourArea)              # Get the properties of the largest circle
                    ((x, y), radius) = cv2.minEnclosingCircle(c)    # Get properties of circle around shape
                    radius = round(radius, 2)   # Round radius value to 2 decimals
                    x = int(x)          # Cast x value to an integer
                    M = cv2.moments(c)  # Gets area of circle contour
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   # Get center x,y value of circle
                    print("x: ", x, "\ty: ", y, "\tR: ", radius, "\tCenter: ", center)
                    # handle centered condition
                    # magnet.em_on()
                    if x > ((width/2)-(band/2)) and x < ((width/2)+(band/2)):       # If center point is centered
                        #item centered to SCUTTLE center of usb camera "centered"
                        print("Item Centered")
                        # once SCUTTLE is center; drive towards metal items. "picking up"
                        dir = "driving"
                        if radius >= tp: # Too close
                            case = "too close"
                            duty = -1 * ((radius-tp)/(tc-tp))
                            print("slowly approach")
                        elif radius < tp: # Too far
                            case = "too far"
                            duty = 1 - ((radius - tf)/(tp - tf))
                            duty = scale_d * duty
                            print("approach item(s)")
                        duty_r = duty
                        duty_l = duty
                        print("Picking Up Item(s)")
                        # drive function to drive forward for a few seconds
                        # time.sleep(0.2) # call out encoders 
                        # resume random path
                        print("Item has been picked up")
                        rcpy.set_state(rcpy.EXITING)
                        print("Resuming Search")
                    # addition of recentering scuttle if lost for future
                    elif x < ((width/2)-(band/2)): # recenter scuttle if still in view field
                        print("Turning Right")
                        case = "turning right"
                        duty_l = round((x-0.5*width)/(0.5*width),2)     # Duty Left
                        duty_l = duty_l*scale_t
                        duty_r = round((0.5*width-x)/(0.5*width),2)     # Duty Right
                        duty_r = duty_r*scale_t
                    elif x > ((width/2)+(band/2)):
                        print("Turning left")
                        case = "turning left"
                        duty_r = round((x-0.5*width)/(0.5*width),2)     # Duty Left
                        duty_r = duty_l*scale_t
                        duty_l = round((0.5*width-x)/(0.5*width),2)     # Duty Right
                        duty_l = duty_r*scale_t
                        print("Resume Search")
                        # resume random path cleaning
                        # rcpy.set_state(rcpy.EXITING)   
                    # Keep duty cycle within range for right wheel
                    if duty_r > 1:
                        duty_r = 1
                    elif duty_r < -1:
                        duty_r = -1
                     # Keep duty cycle within range for left wheel                      
                    if duty_l > 1:
                        duty_l = 1
                    elif duty_l < -1:
                        duty_l = -1
                        
                    # Round duty cycles
                    duty_l = round(duty_l,2)
                    duty_r = round(duty_r,2)

                    # Set motor duty cycles
                    motor.set(motor_l, duty_l)
                    motor.set(motor_r, duty_r)
            elif rcpy.get_state() == rcpy.EXITING:
                pass
    except KeyboardInterrupt: # condition added to catch a "Ctrl-C" event and exit cleanly
        rcpy.set_state(rcpy.EXITING)
        pass
    finally:
    	rcpy.set_state(rcpy.EXITING)
    	print("Exiting Color Tracking.")
    
if __name__ == '__main__':
    main()
