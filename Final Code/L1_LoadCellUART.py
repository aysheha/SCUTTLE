#This code reads Loadcell ADC data over UART
#The two firmwares for the loadcell use 9600 baud
#this code will return a variable containing the 24bit ADC value
#if the code returns "ns" the loadcell is not hooked up
#run on its own, the code will simply print the value to terminal

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#you MUST run setup somewhere before running other functions
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import Adafruit_BBIO.UART as UART
import serial

 

buff = "3"
ser = serial.Serial(port = "/dev/ttyO5", baudrate=9600) 
def setup():

		ser.close()
		ser.open()
		print ("Serial is open!")
		
def loadRead():
	buff = ser.readline()
	buff = int(buff)
	return buff
		
if __name__ == "__main__":
	UART.setup("UART5")
	setup()
	print("beginning Loadcell loop")
	while True:
		buff = loadRead()
		print(buff)
