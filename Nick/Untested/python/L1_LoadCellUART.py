#This code reads Loadcell ADC data over UART
#The two firmwares for the loadcell use 9600 baud
#this code will return a variable containing the 24bit ADC value
#if the code returns "ns" the loadcell is not hooked up
#run on its own, the code will simply print the value to terminal

import Adafruit_BBIO.UART as UART
import serial
import rcpy
 
UART.setup("UART1")
 
def setup():
	ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600)
	ser.close()
	ser.open()
def loadRead():
	if ser.isOpen():
		print "Serial is open!"
   	 	buff = ser.read()
    		return buff

if __name__ == "__main__":
	setup()
	while True:
		print("beginning Loadcell loop")
		buff = loadRead(buff)
        	print(buff)
