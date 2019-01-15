#include <ESP8266WiFi.h>
#include <Wire.h>

int sensor_pin = A0;

int light;
int moisture;
int temperature;

int mapped_light;
int mapped_moisture;
int mapped_temperature;

/*char string_mapped_light[4] = {'8','8'};
char string_mapped_moisture[4] = {'1'};
char string_mapped_temperature[4] = {'1','0','0'};*/

char string_mapped_light[4];
char string_mapped_moisture[4];
char string_mapped_temperature[4];

int value;
int output_value;
//char string_output_value[13] = string_mapped_light+':'+string_mapped_moisture+':'+string_mapped_temperature;
String Stick = "1:";

const char* ssid     = "DSS";
const char* password = "DSSwifi020!";
const char* message     = "Hi from the Wemos!";

String commandStop = "stop";

int i = 0;

const uint16_t port = 10000;
const char * host = "192.168.43.28";
String serial_data = "This is the Wemos";
WiFiClient client;

WiFiServer wifiServer(10000);

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

  //moisture 200 / 722
  //light 65535 / 0
  //room temperature = 250

  mapped_moisture = map(moisture, 200, 722, 0, 100);
  mapped_light = map(light, 5000, 0, 0, 100);
  mapped_temperature = map(temperature, 199, 256, 0, 100); //temperature - 223;

  if(mapped_light > 5000){
    mapped_light = 5000;
  }

  if(mapped_light < 0){
    mapped_light = 0;
  }

  if(mapped_temperature > 100){
    mapped_temperature = 100; 
  }
  
  Serial.print(mapped_moisture);
  Serial.print(", ");
  Serial.print(mapped_light);
  Serial.print(", ");
  Serial.println(mapped_temperature);

  sprintf(string_mapped_moisture, "%d", mapped_moisture);
  sprintf(string_mapped_light, "%d", mapped_light);
  sprintf(string_mapped_temperature, "%d", mapped_temperature);
  
  Serial.println(Stick+string_mapped_moisture+":"+string_mapped_light+":"+string_mapped_temperature);
  return (Stick+string_mapped_moisture+":"+string_mapped_light+":"+string_mapped_temperature);
}

void senddata(String value){
WiFiClient client = wifiServer.available();
if(!client.connect(host, port)) 
  {
    Serial.println("connection failed");
  }
  else{
    delay(500);
    Serial.println("Connected! Sending data..");
    client.print(value);
    Serial.println("Disconnecting...");
    client.stop();
       }
    //i++;
    }
  
  
void setup() {
  Wire.begin();
  Wire.setClockStretchLimit(2500);
  Serial.begin(9600);
  writeI2CRegister8bit(0x20, 6); //reset
  Serial.println();

  WiFi.begin("MobielJoel", "dbkq2327");

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

  // Use WiFiClient class to create TCP connections

  const int port = 10000;
  while (!client.connect(host, port)) 
  {
    Serial.println("connection failed");
    delay(5000);
  }
  
    //Serial.println("connected to Host");
    //Serial.println("Sent..");
    //client.print(serial_data);
 
}

void loop(){

senddata(moistureSensor());
 //delay(5000);
 delay(100);
}

  /*if (client) {
    while (client.connected()) {
      while (client.available()>0) {
        client.print(message);
        //Serial.write(c);
      }
      
         delay(1000);
    }
    client.stop();]
    Serial.println("Client disconnected");
  }
  else{
    Serial.println("Could not send data");
    delay(1000);
  }*/
