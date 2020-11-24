# L3_storing.py
# This program stores the collected metal item(s) into a tray. The tray is retracted
# both inward and outward using a servo motor. A load cell is also used to determine 
# whether the SCUTTLE successfully stored the metal item(s)
# Access nodered at 192.168.8.1:1880 (by default, it's running on the Blue)

# SENSORS used: Load Cell [raw adc] 
# ACTUATORS used: EM is activated & Servo motor
# Mission Status: "Storing", "Checking", "Complete"
# Error Status: "Failed to store"

# Import Internal Programs
import L1_EM as magnet          # turn off EM
import L1_LoadCell as cell      # determine if tray has stored items
import L1_servos as act         # retract tray via servos
import time  

import Adafruit_BBIO.UART as UART
import serial
print("FINISHED loading libraries")

# Run the main loop
def storing():
    act.move1(-0.6)

def checking():
    act.move1(0)

def complete():
    magnet.em_off()
    act.move1(0.6)


#magnet.em_on()

#while 1:
    #magnet.em_on()
    # retract tray outwards
    #storing()
    #time.sleep(0.55)
    #checking()
    #cell.setup()
    #print("storing items")

    #print("checking tray")
    #buff1 = cell.loadRead()
    #time.sleep(1)
    #print("drop now")
    
    # turn magnet off
    #magnet.em_off()
    #time.sleep(5)
    #cell.setup()
    #buff2 = cell.loadRead()
    
    # check load cell readings 
    #print("checking tray")
    #print("buff2 \t", buff2, "buff1 \t", buff1, "difference \t", buff2 - buff1)

    #if  (buff2 - buff1) > 5000:
        #print("buff2 \t", buff2, "buff1 \t", buff1, "difference \t", buff2 - buff1)
        #complete()
        #print("retract tray")
        #print("Storage complete")
        #time.sleep(0.55)
        #checking()
        #time.sleep(2)
    #else: 
        # keep magnet on
        #magnet.em_on
        #print("retract tray")
        #checking()
        #time.sleep(2)
        #print("ERROR: Failed to store")
    #time.sleep(5)
    # halt servos to check tray 
    #magnet.em_on
    #checking()
    #time.sleep(2)
    #print("Resume Search")