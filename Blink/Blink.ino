int sensorPin = A0; // select the input pin for LDR
int ledPin = A3;

int sensorValue = 0; // variable to store the value coming from the sensor
int power1 = 0;
void setup() {
Serial.begin(9600); //sets serial port for communication
}
void loop() {
sensorValue = analogRead(sensorPin); // read the value from the sensor
Serial.println(sensorValue); //prints the values coming from the sensor on the screen

if (sensorValue <= 20) {
    power1 = 0;
  } else if (sensorValue >= 69 && sensorValue <= 230) {
    power1 = 130;
  } else if (sensorValue >= 231 && sensorValue <= 407) {
    power1 = sensorValue;
  } else if (sensorValue >= 408 && sensorValue <= 630) {
    power1 = 1000;
  } else if (sensorValue >= 631 && sensorValue <= 896) {
    power1 = 1500;
  }

analogWrite(ledPin, power1);
delay(1000);
}
