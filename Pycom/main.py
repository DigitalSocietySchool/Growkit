
import socket
import sys
import pycom
import time
import ssl
import urequests
from ws2812 import WS2812
from network import LTE

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
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

def setLED(value):
    if value >= 60:
        pycom.rgbled(0xff00) #Green

    elif value < 60 and value >= 20:
        pycom.rgbled(0xffff00) #Yellow

    elif value < 20:
        pycom.rgbled(0xFF0000) #Red

def getDataSticks():
    s.bind(('0.0.0.0', 10000))

    print ('Socket bind complete')

    s.listen(5)                          # Now wait for client connection.
    print ('Socket now listening')

    print("Listening...")
    c, addr = s.accept()        # Establish connection with client.
    print ('Got connection from', addr)
    data = c.recv(1024)
    value = data.decode()
    print (value)
    valueint = int(value)
    #if value == "stop":
    #   break;
    c.send('Thank you for connecting')
    c.close()                # Close the connection
    print('Socket connection closed!')
    #if value != "stop":
    #
    setLED(valueint)
    return value


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

host = "omega.dss.cloud"
port = 23

# Program starts here.
try:
    print("Program starts")

    #response = urequests.post("http://jsonplaceholder.typicode.com/posts", data = "some dummy content")
    #print(response.text)
    #response.close()

    sensorData = {"w1": "78", "l1": "56", "t1": "23"}
    res = urequests.post("http://omega.dss.cloud/joel/send", data = "hey")
    res.close()

    addr_info = socket.getaddrinfo(host, port)
    print (addr_info)
    addr = addr_info[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send("Pycom here!")
    data = s.recv(500)
    print(str(data, 'utf8'), end='')
    '''
    addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
    addr = addr_info[0][-1]
    s = socket.socket()
    s.connect(addr)
    data = s.recv(500)
    print(str(data, 'utf8'), end='')
    '''

    #lte = getLTE()
    #s.bind(HOST, PORT)
    #s.connect('0.0.0.0', PORT)
    #addr = socket.getaddrinfo(host, port)[0][-1]
    #s.connect(addr)
    #s.bind(host,port)
    #s.send('Here is the Pycom!')


 #print("Initially, the RTC is {}".format("set" if rtc.synced() else "unset"))
 #rtc = getRTC()
    '''while(True):
         data = getDataSticks()
         lte = getLTE()
         #print("RTC is {}".format(rtc.now() if rtc.synced() else "unset"))
         time.sleep(5)'''
except (socket.error, socket.timeout) as e:
    print("ERROR" + str(e))
endLTE()
