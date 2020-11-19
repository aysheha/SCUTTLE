#This code reads Loadcell ADC data over UART
#The two firmwares for the loadcell use 9600 baud
#this code will return a variable containing the 24bit ADC value
#if the code returns "ns" the loadcell is not hooked up
#run on its own, the code will simply print the value to terminal

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#you MUST run setup somewhere before running other functions
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# this code also calibrates the raw ADC readings 
# basic linear equation of y = mx+b 
# calibration portion covers m = (y-b)/x | multipler = (actual - offset)/raw
# offset value is the average reading with no load applied to load cell
# actual values are the raw adc loadRead() readings 

import Adafruit_BBIO.UART as UART
import serial
import time

buff = "3"
ser = serial.Serial(port = "/dev/ttyO5", baudrate=9600) 
def setup():
		ser.close()
		ser.open()
		print ("Serial is open!")

def loadRead():
	if ser.isOpen():
		buff = ser.readline()
		return int(buff)
		
if __name__ == "__main__":
	UART.setup("UART5")
	setup()
	print("Ready for CALIBRATION")
	print("CALIBRATE: Ensure nothing is placed on load cell")
	time.sleep(2)
	print("CALIBRATE: Calculating Average")
	time.sleep(2)
	
	offset = 0 
	for i in range(0, 20): 
		buff = loadRead()
		offset = float(buff + offset)
		print("buff: \t", float(buff), "\t", "Sum: \t", offset)
		i = i + 1
	
	totalSum = round((offset / 20), 2)
	print("CALIBRATE: offset value:", float(totalSum))
	time.sleep(5)
	
	print("CALIBRATE: place 1 kg item")
	# calibrate w/ actual 1 kg item
	actual = 1000 # 1 kg
	raw = loadRead()
	time.sleep(5)
	print("Waiting...")

	multiplier = abs(round(((actual - float(offset))/float(raw)), 3))
	time.sleep(5)
	print("Calibration complete")
	print("remove items")
	
	time.sleep(4)
	print("beginning Loadcell loop")
	while True:
		raw = loadRead()
		# calculate weight y = mx + b (y = actual; m = multiplier; x = raw, b = buff)
		weight = round((multiplier*float(raw) - float(offset)), 3)
		time.sleep(4)
		print("Multipler: \t", multiplier, "\t", "Raw value: \t", float(raw), "\t", "offset: \t", float(offset), "\t", "actual: \t", weight, "\t")
