import socket
import sys
import pycom
import time
from utime import sleep
import ssl
import ufirebase as firebase
import ws2812
from network import LTE
import json
import ledConf
from machine import CAN

#Creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

pycom.heartbeat(False)

# Need to use global variables.
# If in each function you delare a new reference, functionality is broken
lte = LTE()

# Returns a network.LTE object with an active Internet connection.
def getLTE():

 # If already used, the lte device will have an active connection.
 # If not, need to set up a new connection.
 if lte.isconnected():
     return lte

 # Modem does not connect successfully without first being reset.
 print("Resetting LTE modem ... ", end='')
 lte.send_at_cmd('AT^RESET')
 print("OK")
 time.sleep(1)

 # While the configuration of the CGDCONT register survives resets,
 # the other configurations don't. So just set them all up every time.
 print("Configuring LTE ", end='')
 lte.send_at_cmd('AT+CGDCONT=1,"IP","vodafone.internet"')
 print(".", end='')
 lte.send_at_cmd('AT!="RRC::addscanfreq band=20 dl-earfcn=6300"')
 print(".", end='')
 lte.send_at_cmd('AT+CFUN=1')
 print(" OK")

 # If correctly configured for carrier network, attach() should succeed.
 if not lte.isattached():
     print("Attaching to LTE network ", end='')
     lte.attach()
     while True:
         if lte.isattached():
             print(" OK")
             break
             print('.', end='')
         time.sleep(1)

 # Once attached, connect() should succeed.
 if not lte.isconnected():
     print("Connecting on LTE network ", end='')
     lte.connect()
     while(True):
         if lte.isconnected():
             print(" OK")
             break
             print('.', end='')
         time.sleep(1)

 # Once connect() succeeds, any call requiring Internet access will
 # use the active LTE connection.
 return lte

# Clean disconnection of the LTE network is required for future
# successful connections without a complete power cycle between.
def endLTE():

 print("Disonnecting LTE ... ", end='')
 lte.disconnect()
 print("OK")
 time.sleep(1)
 print("Detaching LTE ... ", end='')
 lte.dettach()
 print("OK")

# Sets the internal real-time clock.
# Needs LTE for Internet access.

def pushtoDatabase(stickNumber, moistureValue, lightValue, temperatureValue):
    #Make string of stickNumber, this has to be done to put it in the URL.
    stringStickNumber = str(stickNumber)
    #URL that will update firebase
    firebase.patch('https://'+databaseReference+'+/Pins/'+pin+'/Plants/Stick'+stringStickNumber+'', {'Water': moistureValue, 'Light': lightValue, 'Temperature': temperatureValue})

def setLED(moistureValue, lightValue, temperatureValue):
    #The following calculations calculates the amount of leds that has te be turned on
    #based on the value that has been measured. Ex: If moistureValue is 67, then
    #multiply this by 14 (this is the amount of leds used for moisture) and devide this
    #by hundred. This way, a value of 67 will turn on 9,38 leds.

    ledAmountMoisture = (moistureValue * 14) / 100 # 14 is the amount of leds for light
    ledAmountLight = (lightValue * 11) / 100 # 11 is the amount of leds for light
    ledAmountTemperature = (temperatureValue * 9) / 100 # 9 is the amount of leds for light

    #9.38 leds cant be turned on. Following code rounds this value. This is not completely working
    #because a value of 9.8 will be rounded to 9.
    intLedAmountMoisture = int(ledAmountMoisture)
    intLedAmountLight = int(ledAmountLight)
    intLedAmountTemperature = int(ledAmountTemperature)

    #Call function show from file ws2812. Give data value from the function confSetLight in file ledConf.
    ws2812.show(ledConf.confSetLight(intLedAmountMoisture, intLedAmountLight, intLedAmountTemperature))

def getDataSticks():
    #Clear buffer before reading new data from socket
    c = ''
    #Accept any incomming connections
    c, addr = s.accept()

    #Real all data from incomming socket connection
    dataTest = c.readall()
    #Decode dataTest
    value = dataTest.decode()
    #Make string value of value
    strValue = str(value)

    #The Hessah chip sends the data in string format. The string looks like this ex:
    #1:23:55:72. This means that stick one is sending a moisturevalue of 23, lightvalue of 55
    # and a temperaturevalue of 72. At every ":" it splits the value into the variables.
    stickNumber, moistureValue, lightValue, temperatureValue = strValue.split(':' , 3)

    #Convert all values to integers
    intStickNumber = int(stickNumber)
    intMoistureValue = int(moistureValue)
    intLightValue = int(lightValue)
    intTemperatureValue = int(temperatureValue)

    #Close socket connection, this is necassery to make a new one
    c.close()

    #Prints used from debugging
    #print(intStickNumber)
    #print(intMoistureValue)
    #print(intLightValue)
    #print(intTemperatureValue)

    #Call function setLed and give all the values with it
    setLED(intMoistureValue, intLightValue, intTemperatureValue)

    #Call function pushtoDatabase and give all the values with it
    pushtoDatabase(intStickNumber, intMoistureValue, intLightValue, intTemperatureValue)

URL = '' #URL to database ex: https://project-020.firebaseio.com/
databaseReference = '' #ex: project-020.firebaseio.com
pin = '' #ex: 4444

s.bind(('0.0.0.0', 10000)) #Bind to this address and port to get the data from the Sticks using a socket connection
s.listen(5)  # Now wait for client connection.

blank = 34 * [(0,0,0)]
ws2812 = ws2812.WS2812("P12") #P12 = GPIO28 on pycom


# Program starts here.
while True:
    try:
        #Use getLte() in your final version. It is not used for the showcase, because it makes the respond time very slow.
        #getLTE()

        getDataSticks()

    except (Exception) as e:
        print("ERROR" + str(e))
        break;
