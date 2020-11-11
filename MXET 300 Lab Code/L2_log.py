# This program contains functions for logging robot parameters
# to local files.  The files can be accessed by NodeRed or other programs.
# Nodered can be found on the beagle at port 1880. ie, 192.168.8.1:1880

# Import external libraries
import csv      # for handling comma-separated-values file type


# A function for populating 2 text files with updated phi-dots
def writeFiles(current_phis):
    txt = open("/home/debian/basics/PDL.txt", 'w+')         # file for phi dot left
    txt2 = open("/home/debian/basics/PDR.txt", 'w+')        # file for phi dot right
    phi_dotL = round(current_phis[0], 1)
    phi_dotR = round(current_phis[1], 1)
    txt.write(str(round(phi_dotL, 1)))
    txt2.write(str(round(phi_dotR, 1)))
    txt.close()
    txt2.close()


# A function for populating 2 text files with updating variables
def NodeRed3(values):                                       # this function takes a 2-element array called val
    txt = open("/home/debian/basics/xAccel.txt", 'w+')           # file for generic variable a
    txt2 = open("/home/debian/basics/yAccel.txt", 'w+')          # file for generic variable b
    txt3 = open("/home/debian/basics/zAccel.txt", 'w+')          # file for generic variable b
    xAccel = round(values[0], 2)
    yAccel = round(values[1], 2)
    zAccel = round(values[2], 2)
    txt.write(str(xAccel))
    txt2.write(str(yAccel))
    txt3.write(str(zAccel))
    txt.close()
    txt2.close()
    txt3.close()
    
# A function for populating 2 text files with updating variables
def NodeRed2(values):                                       # this function takes a 2-element array called val
    txt = open("/home/debian/basics/pdl.txt", 'w+')          
    txt2 = open("/home/debian/basics/pdr.txt", 'w+')          
    phidotL = round(values[0], 2)
    phidotR = round(values[1], 2)
    txt.write(str(phidotL))
    txt2.write(str(phidotR))
    txt.close()
    txt2.close()
    
def uniqueFile(value):
    txt = open("/home/debian/basics/distance.txt", 'w+')     # file for phi dot R
    txt.write(str(dist))
    txt.close()

def uniqueFile(value):
    txt = open("/home/debian/basics/angle.txt", 'w+')     # file for phi dot R
    txt.write(str(ang))
    txt.close()

def uniqueFile(value):
    txt = open("/home/debian/basics/dx.txt", 'w+')     # file for phi dot R
    txt.write(str(dx))
    txt.close()

def uniqueFile(value):
    txt = open("/home/debian/basics/dy.txt", 'w+')     # file for phi dot R
    txt.write(str(dy))
    txt.close()
    
def uniqueFile(value):
    txt = open("/home/debian/basics/phidotR.txt", 'w+')     # file for phi dot R
    txt.write(str(phidotR))
    txt.close()
    
def uniqueFile(value):
    txt = open("/home/debian/basics/phidotL.txt", 'w+')     # file for phi dot L
    txt.write(str(phidotL))
    txt.close()

def uniqueFile(value):
    txt = open("/home/debian/basics/xdot.txt", 'w+')        # file for x dot
    txt.write(str(xdot))
    txt.close()

def uniqueFile(value):
    txt = open("/home/debian/basics/thetadot.txt", 'w+')    # file for theta dot
    txt.write(str(thetadot))
    txt.close()
    
def uniqueFile(value):
    txt = open("/home/debian/basics/heading.txt", 'w+')    # file for theta dot
    txt.write(str(headingDegrees))
    txt.close()

# A function for populating 2 text files with updating variables
def uniqueFile(value):
    txt = open("/home/debian/basics/temperature.txt", 'w+')           # file for generic variable a
    #temperature = round(values[0], 2)
    txt.write(str(temperature))
    txt.close()

def uniqueFile(value):   
    txt = open("/home/debian/basics/pressure.txt", 'w+')          # file for generic variable b
#     pressname = round(values[0], 2)
#     pressure = round(values[1], 2)
    txt.write(str(pressure))
    txt.close()

def uniqueFile(value):    
    txt = open("/home/debian/basics/altitude.txt", 'w+')          # file for generic variable b
#     altitude = round(values[0], 2)
    txt.write(str(altitude))
    txt.close()

# A function for sending 1 value to a log file of specified name
def uniqueFile(value):                            # this function takes a 2-element array called val
    txt = open("/home/debian/basics/barrelvoltage.txt", 'w+')     # file with specified name
#     barrelvoltage = round(values[1], 2)
    txt.write(str(barrelvoltage))
    txt.close()
    
    
# A function for sending 1 value to a log file of specified name
def uniqueFile(value, fileName):                            # this function takes a 2-element array called val
    txt = open("/home/debian/basics/" + fileName, 'w+')     # file with specified name
    myValue = round(value, 2)
    txt.write(str(myValue))
    txt.close()

# A function for sending 1 value to a log file in a temporary folder
#def tmpFile(value, fileName):                               # this function takes a 2-element array called val
#    txt = open("/tmp/" + fileName, 'w+')                    # file with specified name
#    myValue = round(value, 2)
#    txt.write(str(myValue))
#    txt.close()

# A function for creating a CSV file from a list of values.
def csv_write(list):
    list = [str(i) for i in list]
    with open('excel_data.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(list)
    csvFile.close()


# A function to clear an existing CSV file
def clear_file():
    open('excel_data.csv', 'w').close()