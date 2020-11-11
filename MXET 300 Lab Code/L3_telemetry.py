# L3_telemetry.py
# This program grabs data from the onboard sensors and log data in files
# for NodeRed access and integrate into a custom "flow".
# Access nodered at 192.168.8.1:1880 (by default, it's running on the Blue)

# Import Internal Programs
import L1_mpu as mpu
import L1_bmp as bmp
import L1_adc as adc
import L2_log as log

# Import External programs
import numpy as np
import time

# Run the main loop
while True:
    accel = mpu.getAccel()                          # call the function from within L1_mpu.py
    (xAccel) = accel[0]                             # x axis is stored in the first element
    (yAccel) = accel[1]                             # y axis is stored in the second element
    (zAccel) = accel[2]                             # z axis is stored in the third element
    print("x axis:", xAccel, "y axis:", yAccel, "z axis:", zAccel)     # print the two values
    axes = np.array([xAccel, yAccel, zAccel])               # store just 2 axes in an array
    log.NodeRed3(axes)                              # send the data to txt files for NodeRed to access.
    log.uniqueFile(xAccel,"xAccel.txt")           # another way to log data for NodeRed access
    log.uniqueFile(yAccel,"yAccel.txt")
    log.uniqueFile(zAccel,"zAccel.txt")
    # log.tmpFile(xAccel,"xAccel.txt")              # another way to lof data for NodeRed access
    # log.tmpFile(yAccel,"yAccel.txt")
    
    temperature = bmp.temp()
    #(temperature) = tempC[0]
    print("Temperature:", temperature)
    log.uniqueFile(temperature, "temperature.txt")
    
    pressure = bmp.pressure()
    # (pressure) = presskpa[0]
    print("Pressure:", pressure)
    log.uniqueFile(pressure, "pressure.txt")
    
    altitude = bmp.altitude()
    # (altitude) = altm[0]
    print("Altitude:", altitude)
    log.uniqueFile(altitude, "altitude.txt")
    
    barrelvoltage = adc.getDcJack()
    #(barrelVoltage) = voltage[1]
    print("Barrel Voltage:", barrelvoltage)
    log.uniqueFile(barrelvoltage, "barrelvoltage.txt")
    

    time.sleep(0.2)
#################