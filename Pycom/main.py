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

#from ws2812rmt import WS2812RMT
#from machine import SPI, disable_irq, enable_irq

#https://github.com/JF002/lopy-snippets/tree/master/WS2812

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def send_rmt(data, rmt):
    no_pixel = len(data)
    bits = bytearray(no_pixel * 24 * 2 + 2)
    duration =  bytearray(no_pixel * 24 * 2 + 2)
    bits[0] = 0
    duration[0] = 255
    bits[0] = 1
    duration[1] = 255 # reset 51 µs
    index = 2
    for pixel in data:
        for byte in pixel:
            mask = 0x80
            while mask:
                bits[index] = 1
                bits[index+1] = 0
                if byte & mask:
                    duration[index] = 8
                    duration[index+1] = 4
                else:
                    duration[index] = 5
                    duration[index+1] = 9
                index += 2
                mask >>= 1
    rmt.pulses_send(tuple(duration), tuple(bits))

'''
chain = WS2812( ledNumber=4, brightness=10, dataPin='P22' ) # dataPin is for LoPy board only
data = [
        (255, 102, 0)
        (255, 102, 0)
        (255, 102, 0)
        (255, 102, 0)
        ]
chain.show( data )'''
'''chain = WS2812(spi_bus=1, led_count=4, intensity=10)
data = [
    (255, 0, 0),    # red
    (0, 255, 0),    # green
    (0, 0, 255),    # blue
    (85, 85, 85),   # white
]
chain.show(data)'''


pycom.heartbeat(False)
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0xffff00

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
    stringStickNumber = str(stickNumber)
    firebase.patch('https://growkit-020.firebaseio.com/Pins/4444/Plants/Stick'+stringStickNumber+'', {'Water': moistureValue, 'Light': lightValue, 'Temperature': temperatureValue})

    '''if(stickNumber == 1):
        firebase.patch('https://growkit-020.firebaseio.com/Pins/4444/Plants/Stick', {'Water': moistureValue, 'Light': lightValue, 'Temperature': temperatureValue})

    if(stickNumber == 2):
        firebase.put('https://growkit-020.firebaseio.com/Pins/4444/Plants/Stick2', {'Water': moistureValue, 'Light': lightValue, 'Temperature': temperatureValue})'''

def setLED(moistureValue, lightValue, temperatureValue):
    ledAmountMoisture = (moistureValue * 14) / 100 # 14 is the amount of leds for light
    ledAmountLight = (lightValue * 11) / 100 # 11 is the amount of leds for light
    ledAmountTemperature = (temperatureValue * 9) / 100 # 9 is the amount of leds for light

    intLedAmountMoisture = int(ledAmountMoisture)
    intLedAmountLight = int(ledAmountLight)
    intLedAmountTemperature = int(ledAmountTemperature)

    #print(intLedAmountMoisture)
    #print(intLedAmountLight)
    #print(intLedAmountTemperature)

    #ws2812.show(ledConf.configLedYellow(intLedAmount))
    #ws2812.show(34 * [(0,0,0)])
    ws2812.show(ledConf.confSetLight(intLedAmountMoisture, intLedAmountLight, intLedAmountTemperature))
    #sleep(1)

def getDataSticks():
    c = ''
    c, addr = s.accept()

    try:
        print ('Got connection from', addr)
        dataTest = c.readall()
        value = dataTest.decode()
        strValue = str(value)

        stickNumber, moistureValue, lightValue, temperatureValue = strValue.split(':' , 3)

        print('Stick = ' + stickNumber)
        print('Water = ' + moistureValue)
        print('Light = ' + lightValue)
        print('Temperature = ' + temperatureValue)

    except (Exception) as e:
        print("ERROR1" + str(e))

    print('INT VALUES:')
    intStickNumber = int(stickNumber)
    intMoistureValue = int(moistureValue)
    intLightValue = int(lightValue)
    intTemperatureValue = int(temperatureValue)

    print('Socket connection closed!')
    c.close()

    print(intStickNumber)
    print(intMoistureValue)
    print(intLightValue)
    print(intTemperatureValue)

    '''
    if(intStickNumber == 1):
        healthStickOne = (intMoistureValue + intLightValue + intTemperatureValue) / 3
        stringHealthStickOne = string(healthStickOne)
        print('Health stick 1 = ' + stringHealthStickOne)

    else:
        healthStickTwo = (intMoistureValue + intLightValue + intTemperatureValue) / 3
        print('Health stick 2 = ' + healthStickTwo)

    intHealthStickOne = int(healthStickOne)
    intHealthStickTwo = int(healthStickTwo)

    if(intHealthStickOne <= intHealthStickTwo):
        setLED(intMoistureValue, intLightValue, intTemperatureValue)
    else:
        setLED(intMoistureValue, intLightValue, intTemperatureValue)
    '''

    setLED(intMoistureValue, intLightValue, intTemperatureValue)
    print('Set LED light')
    print()

    pushtoDatabase(intStickNumber, intMoistureValue, intLightValue, intTemperatureValue)

URL = 'https://growkit-020.firebaseio.com/'

s.bind(('0.0.0.0', 10000))
print ('Socket bind complete')
s.listen(5)                          # Now wait for client connection.
print ('Socket now listening...')

blank = 34 * [(0,0,0)]
#rmt = RMT(channel=3, gpio="P11", tx_idle_level=0)
ws2812 = ws2812.WS2812("P12") #P12 = GPIO28 on pycom


#https://github.com/vishal-android-freak/firebase-micropython-esp32
i = 0


# Program starts here.
while True:
    try:
        print("Program Restarts")
        #getLTE()
        getDataSticks()

        i = i + 1
        if(i == 60):
            ws2812.show(blank)
            sleep(1)
            break;
        print(i)

    except (Exception) as e:
        print("ERROR" + str(e))
        break;
