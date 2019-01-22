#include <ESP8266WiFi.h>
#include <Wire.h>

int light;
int moisture;
int temperature;

int mapped_light;
int mapped_moisture;
int mapped_temperature;

char string_mapped_light[4];
char string_mapped_moisture[4];
char string_mapped_temperature[4];

int value;
//Stick should be changed when using another stick. This code is used for stick number 1. When using stick number 2, change it to "2:"
//Same works for stick 3, 4, 5 etc..
String Stick = "1:";


const char* ssid     = "DSS";
const char* password = "DSSwifi020!";

int i = 0;

//port 10000 is the port where the Pycom GPY is bound to. To send the data, it has to connect with the same port.
//host is the IP address of the Pycom GPY
const uint16_t port = 10000;
const char * host = "192.168.0.105";
WiFiClient client;
WiFiServer wifiServer(10000);

//WriteI2cRegsiter8bit and readI2CRegister16bit reads and writes the value of the moisture sensore, light sensor and temperature sensor
void writeI2CRegister8bit(int addr, int value) {
  Wire.beginTransmission(addr);
  Wire.write(value);
  Wire.endTransmission();
}

unsigned int readI2CRegister16bit(int addr, int reg) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.endTransmission();
  delay(20);
  Wire.requestFrom(addr, 2);
  unsigned int t = Wire.read() << 8;
  t = t | Wire.read();
  return t;
}


String moistureSensor(){
  //Get and print value of moisture sensor, light sensor and temperature sensor
  Serial.print(readI2CRegister16bit(0x20, 0)); //read capacitance register
  Serial.print(", ");
  writeI2CRegister8bit(0x20, 3); //request light measurement 
  Serial.print(readI2CRegister16bit(0x20, 4)); //read light register
  Serial.print(", ");
  Serial.println(readI2CRegister16bit(0x20, 5)); //temperature register
  delay(500);

  moisture = readI2CRegister16bit(0x20, 0);
  temperature = readI2CRegister16bit(0x20, 5);
  light = readI2CRegister16bit(0x20, 4);

  //Map the values all values from 0 to 100 (percentages). Ex: if moisture value is 555, the mapped value of this will be around 50.
  //Thats because 200 equals 0 and 722 equals 100. 555 is in the middle.
  mapped_moisture = map(moisture, 200, 722, 0, 100);
  mapped_light = map(light, 5000, 0, 0, 100);
  mapped_temperature = map(temperature, 255, 305, 0, 100);

  //These if statements are used if the value will reach under 0 or above some value.
  if(mapped_moisture < 0){
    mapped_moisture = 0;
  }
  
  if(mapped_light > 5000){
    mapped_light = 5000;
  }

  if(mapped_light < 0){
    mapped_light = 0;
  }

  if(mapped_temperature > 100){
    mapped_temperature = 100; 
  }
  

  //Makes Strings of the integer values to.
  sprintf(string_mapped_moisture, "%d", mapped_moisture);
  sprintf(string_mapped_light, "%d", mapped_light);
  sprintf(string_mapped_temperature, "%d", mapped_temperature);
  
  Serial.println(Stick+string_mapped_moisture+":"+string_mapped_light+":"+string_mapped_temperature);
  //Return this string
  return (Stick+string_mapped_moisture+":"+string_mapped_light+":"+string_mapped_temperature);
}

void senddata(String value){
WiFiClient client = wifiServer.available();
//If Pycom is not online
if(!client.connect(host, port)) 
  {
    Serial.println("connection failed");
  }
  //Else, send the data with client.print
  else{
    delay(500);
    Serial.println("Connected! Sending data..");
    client.print(value);
    Serial.println("Disconnecting...");
    client.stop();
       }
    }
  
  
void setup() {
  Wire.begin();
  Wire.setClockStretchLimit(2500);
  Serial.begin(9600);
  writeI2CRegister8bit(0x20, 6); //reset
  Serial.println();

  //Wifi connection settins for DSS wifi
  WiFi.begin("DSS_2", "DSSwifi020!");

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("connecting to ");
  Serial.println(host);

  const int port = 10000;
  while (!client.connect(host, port)) 
  {
    Serial.println("connection failed");
    delay(5000);
  }
}

void loop(){
senddata(moistureSensor());
 delay(100);
}
