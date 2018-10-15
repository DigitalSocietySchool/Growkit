/*#include <dht.h>

dht DHT;

#define DHT11_PIN 7

void setup(){
  Serial.begin(9600);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  delay(1000);
}
*/
int humidityPin = A2;
int value;

void setup() {

   Serial.begin(9600);

   Serial.println("Reading From the Sensor ...");

   delay(2000);

   }

void loop() {

   value = analogRead(humidityPin);

   int adjusted_value = value * 1.024; 

   if(adjusted_value > 1000){
    adjusted_value = 1000;
   }
   
   int output_value = map(adjusted_value,0,1000,0,100);
 

   Serial.print("Humidity : ");

   Serial.print(output_value);

   Serial.println("%");

   delay(1000);

}
