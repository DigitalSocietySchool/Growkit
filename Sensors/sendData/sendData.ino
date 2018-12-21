#include <ESP8266WiFi.h>

int sensor_pin = A0;

int value;
int output_value;

const char* ssid     = "DSS";
const char* password = "DSSwifi020!";
const char* message     = "Hi from the Wemos!";

String commandStop = "stop";

int i = 0;

const uint16_t port = 10000;
const char * host = "192.168.43.42";
String serial_data = "This is the Wemos";
WiFiClient client;

WiFiServer wifiServer(10000);

int moistureSensor(){
   value= analogRead(sensor_pin);

   output_value = map(value,100,1000,0,100);

   if(output_value < 0){
    output_value = 0;
   }
   
   if(output_value > 100) {
    output_value = 100;
   }
    
   Serial.print("Moisture : ");

   Serial.print(output_value);

   Serial.println("%");

   return output_value;
}

void senddata(int value){
WiFiClient client = wifiServer.available();
if(!client.connect(host, port)) 
  {
    Serial.println("connection failed");
  }
  else{
   //if(i == 5){
   //Serial.println("Sending Stop command");
   //client.print(commandStop);
   //Serial.println("Last disconnect...");
   //client.stop();
    // This will send data to client via TCP
    Serial.println("Sent..");
    //serial_data = String(Serial.read());
    client.print(value);
    Serial.println("Disconnecting...");
    client.stop();
    //i++;
    }
  }
  
void setup() {
  Serial.begin(9600);
  Serial.println();
  //Serial.setDebugOutput(true);

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

 delay(5000);
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
