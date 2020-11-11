#this script toggles the state of the electro-magnet, with a delay to ensure the induced current
#reaches zero beofre continuing the code, to ensure the bolt drops
#this code toggles a gpio on GPIO connector 1

import L1_gpio as gpio
import time

emState = 0

def em_on():
	gpio.write(0, 0, 1) #chANGE PORT/PIN to match real ones
	emState = 1

def em_off():
	gpio.write(0,0,0)
	time.sleep(2)
	emState = 0

def toggle():
	if emState == 1:
		em_off()
	elif emState == 0:
		em_on()

if __name__ == "__main__":
	while (1):
		toggle()
		time.sleep(5)