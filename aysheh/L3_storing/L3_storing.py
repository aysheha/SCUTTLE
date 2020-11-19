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
    act.move1(-0.8)

def checking():
    act.move1(0)

def complete():
    # magent.em_off()
    act.move1(0.8)
    
def cellreading():
    raw = loadRead()
	# calculate weight y = mx + b (y = actual; m = multiplier; x = raw, b = buff)
	
while 1:
    # retract tray outwards
    storing()
    print("storing items")
    time.sleep(1)
    
    # turn magnet off
    # magnet.em_off()
    
    # check load cell readings 
    print("checking tray")
    cellreading()
    weight = round((cell.multiplier*float(raw) - float(offset)), 3)
	print("Multipler: \t", multiplier, "\t", "Raw value: \t", float(raw), "\t", "offset: \t", float(offset), "\t", "actual: \t", weight, "\t")
        if weight < 0:
            complete()
            print("Storage complete")
        else: 
            # keep magnet on
            # magnet.em_on
            print("retract tray")
            complete()
            print("ERROR: Failed to store")
    time.sleep(10)
    # halt servos to check tray 
    checking()
    print("Multipler: \t", multiplier, "\t", "Raw value: \t", float(raw), "\t", "offset: \t", float(offset), "\t", "actual: \t", weight, "\t")
    time.sleep(5)

    print("Resume Search")
   
