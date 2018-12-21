
import socket
import sys
import pycom
import time
import ssl
import firebase
from network import LTE

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


pycom.heartbeat(False)
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0xffff00

def connect():
    print("Attaching to LTE network ", end='')
    lte.attach(band=20)
    while not lte.isattached():
        lte.attach()
        time.sleep(1)
    print(' OK')
    if not lte.isconnected():
        print('Connecting to LTE network', end='')
        lte.connect()
        time.sleep(0.5)
    print(" OK")

def disconnect():
    lte.disconnect();
    lte.dettach();

def at(s):
    print(lte.send_at_cmd(s))

def google():
    s = socket.socket()
    ss = ssl.wrap_socket(s)
    i = socket.getaddrinfo('www.google.com', 443)[0][-1]
    print('Connecting to socket...')
    ss.connect(i)
    print('Send...')
    ss.send(b"GET / HTTP/1.0\r\n\r\n")
    print(ss.recv(4096))
    print('Close...')
    ss.close()


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

NTP_SERVER = "au.pool.ntp.org"

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
def setRTC():

 # Ensures LTE session is connected before attempting NTP sync.
 lte = getLTE()

 print("Updating RTC from {} ".format(NTP_SERVER), end='')
 rtc.ntp_sync(NTP_SERVER)
 while not rtc.synced():
     print('.', end='')
     time.sleep(1)
 print(' OK')

# Only returns an RTC object that has already been synchronised with an NTP server.
def getRTC():

 if not rtc.synced():
     setRTC()

 return rtc

HOST = 'omega.dss.cloud'
PORT = 12345

# Program starts here.
try:
    print("Program starts")
    lte = getLTE()
        #setChilKatConf()
    ss = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
    ss.bind((HOST, PORT))
    for i in range(1):
        ts = time.time()
        request = "GET /Pins.json HTTP/1.1\r\n" \
          "Host: " + HOST + "\r\n"                    \
          "Connection: keep-alive\r\n"                \
          "\r\n"
        ss.send(request.encode())
        result = ss.recv(4096)
        #print (result)
        while (len(result)>0):
            print (result)
            result = ss.recv(4096)
        print ('Time '+ str(time.time()-ts))

 #print("Initially, the RTC is {}".format("set" if rtc.synced() else "unset"))
 #rtc = getRTC()
    '''while(True):
         data = getDataSticks()
         lte = getLTE()
         #print("RTC is {}".format(rtc.now() if rtc.synced() else "unset"))
         time.sleep(5)'''
except Exception as e:
    print("ERROR" + str(e))
endLTE()
