# Tries to center the robot by using the 

#
import L1_motors as m
import L1_EM as magnet

target_pixel = np.array([-1, -1, 0, -1, -1])
band = 50

tc = 90
tf = 6
tp = 65

duty_l = 0
duty_r = 0
scale_t = 1.2
scale_d = 0.8
item_up = False

def center_robot(x, width,first_time):
	if first_time:
        m.MotorL(0)
        m.MotorR(0)
        first_time = False
        time.sleep(5)
        
	print("Radius: \t", radius)
    x = int(x)
    if x > ((width/2) - (band/2)) and x < ((width/2) + (band/2)):
        time.sleep(1)
        magnet.em_on()
        print("Item Centered")
        #duty = -1 *((radius-tp)/(tc-tp))
        # go to centered item
            if radius >= tp:
                duty = ((radius-tp)/(tc-tp)) # back up
                print("Picking up item")
                item_up = True
            elif radius < tp:
                duty = 1 - ((radius - tf)/(tp-tf))
                duty = scale_d * duty
                print("approaching item")
                    
            duty_r = duty
            duty_l = duty
            print("duty:\t", duty)
            #print("Picking Up item(s)")

            #print("Item has been picked up")

            #print("Resuming search")
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
    
    if item_up:
        time.sleep(2)
        m.MotorL(0)
        m.MotorR(0)
        #put function for tray thing
        item_up = False
    
if __name__== "__main__":
    while True:
    print("I don't think we can test this on it's own")