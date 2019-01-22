{\rtf1\ansi\ansicpg1252\cocoartf1671\cocoasubrtf200
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #This is the newest version of main.py on the Pycom GPY. It makes use of threads in order to \
#get data from more Sticks. Not using Threads for this will make the socket listener crash.\
#Right now the problem with using threads is that it crashes when pushing it to Firebase \
#(this probably occurs because multiple threads are trying to push new data to Firebase at the\
#same time)\
\
import socket\
import sys\
import pycom\
import time\
from utime import sleep\
import ssl\
import ufirebase as firebase\
import ws2812\
from network import LTE\
import json\
import ledConf\
from machine import CAN\
import _thread;\
\
#from ws2812rmt import WS2812RMT\
#from machine import SPI, disable_irq, enable_irq\
\
#https://github.com/JF002/lopy-snippets/tree/master/WS2812\
\
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\
\
global healthStickOne\
global healthStickTwo\
healthStickOne = 0\
healthStickTwo = 0\
\
\
pycom.heartbeat(False)\
\
# Need to use global variables.\
# If in each function you delare a new reference, functionality is broken\
lte = LTE()\
\
# Returns a network.LTE object with an active Internet connection.\
def getLTE():\
\
 # If already used, the lte device will have an active connection.\
 # If not, need to set up a new connection.\
 if lte.isconnected():\
     return lte\
\
 # Modem does not connect successfully without first being reset.\
 print("Resetting LTE modem ... ", end='')\
 lte.send_at_cmd('AT^RESET')\
 print("OK")\
 time.sleep(1)\
\
 # While the configuration of the CGDCONT register survives resets,\
 # the other configurations don't. So just set them all up every time.\
 print("Configuring LTE ", end='')\
 lte.send_at_cmd('AT+CGDCONT=1,"IP","vodafone.internet"')\
 print(".", end='')\
 lte.send_at_cmd('AT!="RRC::addscanfreq band=20 dl-earfcn=6300"')\
 print(".", end='')\
 lte.send_at_cmd('AT+CFUN=1')\
 print(" OK")\
\
 # If correctly configured for carrier network, attach() should succeed.\
 if not lte.isattached():\
     print("Attaching to LTE network ", end='')\
     lte.attach()\
     while True:\
         if lte.isattached():\
             print(" OK")\
             break\
             print('.', end='')\
         time.sleep(1)\
\
 # Once attached, connect() should succeed.\
 if not lte.isconnected():\
     print("Connecting on LTE network ", end='')\
     lte.connect()\
     while(True):\
         if lte.isconnected():\
             print(" OK")\
             break\
             print('.', end='')\
         time.sleep(1)\
\
 # Once connect() succeeds, any call requiring Internet access will\
 # use the active LTE connection.\
 return lte\
\
# Clean disconnection of the LTE network is required for future\
# successful connections without a complete power cycle between.\
def endLTE():\
\
 print("Disonnecting LTE ... ", end='')\
 lte.disconnect()\
 print("OK")\
 time.sleep(1)\
 print("Detaching LTE ... ", end='')\
 lte.dettach()\
 print("OK")\
\
# Sets the internal real-time clock.\
# Needs LTE for Internet access.\
\
def pushtoDatabase(stickNumber, moistureValue, lightValue, temperatureValue):\
    stringStickNumber = str(stickNumber)\
    firebase.patch('https://growkit-020.firebaseio.com/Pins/4444/Plants/Stick'+stringStickNumber+'', \{'Water': moistureValue, 'Light': lightValue, 'Temperature': temperatureValue\})\
\
    '''if(stickNumber == 1):\
        firebase.patch('https://growkit-020.firebaseio.com/Pins/4444/Plants/Stick', \{'Water': moistureValue, 'Light': lightValue, 'Temperature': temperatureValue\})\
\
    if(stickNumber == 2):\
        firebase.put('https://growkit-020.firebaseio.com/Pins/4444/Plants/Stick2', \{'Water': moistureValue, 'Light': lightValue, 'Temperature': temperatureValue\})'''\
\
def setLED(moistureValue, lightValue, temperatureValue):\
    ledAmountMoisture = (moistureValue * 14) / 100 # 14 is the amount of leds for light\
    ledAmountLight = (lightValue * 11) / 100 # 11 is the amount of leds for light\
    ledAmountTemperature = (temperatureValue * 9) / 100 # 9 is the amount of leds for light\
\
    intLedAmountMoisture = int(ledAmountMoisture)\
    intLedAmountLight = int(ledAmountLight)\
    intLedAmountTemperature = int(ledAmountTemperature)\
\
    #print(intLedAmountMoisture)\
    #print(intLedAmountLight)\
    #print(intLedAmountTemperature)\
\
    #ws2812.show(ledConf.configLedYellow(intLedAmount))\
    #ws2812.show(34 * [(0,0,0)])\
    ws2812.show(ledConf.confSetLight(intLedAmountMoisture, intLedAmountLight, intLedAmountTemperature))\
    #sleep(1)\
\
\
\
def thread_stick(c):\
    #print ('Got connection from', addr)\
    global healthStickOne\
    global healthStickTwo\
\
    dataTest = c.readall()\
    value = dataTest.decode()\
    strValue = str(value)\
\
    stickNumber, moistureValue, lightValue, temperatureValue = strValue.split(':' , 3)\
\
    print('Stick = ' + stickNumber)\
    print('Water = ' + moistureValue)\
    print('Light = ' + lightValue)\
    print('Temperature = ' + temperatureValue)\
    #time.sleep(delay)\
    #print('Running thread %d' % addr)\
\
    #print('INT VALUES:')\
    intStickNumber = int(stickNumber)\
    intMoistureValue = int(moistureValue)\
    intLightValue = int(lightValue)\
    intTemperatureValue = int(temperatureValue)\
\
    c.close()\
\
    '''print(intStickNumber)\
    print(intMoistureValue)\
    print(intLightValue)\
    print(intTemperatureValue)'''\
\
    if(intStickNumber == 1):\
        print("TEST STICK 1")\
        healthStickOne = (intMoistureValue + intLightValue + intTemperatureValue) / 3\
\
        intHealthStickOne = int(healthStickOne)\
        intHealthStickTwo = int(healthStickTwo)\
\
        print(intHealthStickOne)\
        print(intHealthStickTwo)\
\
        if(healthStickOne <= healthStickTwo):\
            print("SETLED STICK 1")\
            setLED(intMoistureValue, intLightValue, intTemperatureValue)\
\
        pushtoDatabase(intStickNumber, intMoistureValue, intLightValue, intTemperatureValue)\
\
\
        #stringHealthStickOne = string(healthStickOne)\
    if(intStickNumber == 2):\
        print("TEST STICK 2")\
        #healthStickTwo = (intMoistureValue + intLightValue + intTemperatureValue) / 3\
        healthStickTwo = (intMoistureValue + intLightValue + intTemperatureValue) / 3\
\
        intHealthStickOne = int(healthStickOne)\
        intHealthStickTwo = int(healthStickTwo)\
\
        print(intHealthStickOne)\
        print(intHealthStickTwo)\
\
        if(healthStickTwo < healthStickOne):\
            print("SETLED STICK 2")\
            setLED(intMoistureValue, intLightValue, intTemperatureValue)\
\
        pushtoDatabase(intStickNumber, intMoistureValue, intLightValue, intTemperatureValue)\
\
\
\
    '''if(intHealthStickOne <= intHealthStickTwo):\
        print("IF")\
    if(intHealthStickTwo < intHealthStickOne):\
        print("IF 2")\
        print(intMoistureValue, intLightValue, intTemperatureValue)\
        setLED(intMoistureValue, intLightValue, intTemperatureValue)'''\
\
    #setLED(intMoistureValue, intLightValue, intTemperatureValue)\
    #print('Set LED light')\
    print()\
\
\
URL = 'https://growkit-020.firebaseio.com/'\
\
s.bind(('0.0.0.0', 10000))\
print ('Socket bind complete')\
s.listen(5)                          # Now wait for client connection.\
print ('Socket now listening...')\
\
blank = 34 * [(0,0,0)]\
#rmt = RMT(channel=3, gpio="P11", tx_idle_level=0)\
ws2812 = ws2812.WS2812("P12") #P12 = GPIO28 on pycom\
\
\
#https://github.com/vishal-android-freak/firebase-micropython-esp32\
i = 0\
\
# Program starts here.\
while True:\
    try:\
        print("Program Restarts")\
        #getLTE()\
        c = ''\
        c, addr = s.accept()\
        #print(c)\
        _thread.start_new_thread(thread_stick, (c,))\
        i = i + 1\
        if(i == 200):\
            ws2812.show(blank)\
            sleep(1)\
            break;\
        print(i)\
\
    except (Exception) as e:\
        print("ERROR" + str(e))\
        break;\
}