int temperaturePin = A1;

void setup() {

   Serial.begin(9600);

   Serial.println("Reading From the Sensor ...");

   delay(2000);

   }

void loop() {
   
  int value = analogRead(temperaturePin);

  int adjusted_value = value * 1.024;  
  int tempC = (adjusted_value * 0.2222) - 68.111;

   Serial.print("Temperature: ");

   Serial.print(tempC);

   Serial.println(" C");

   delay(1000);

}
