int sensor_pin = A0;

int value;
int output_value;
void setup() {

   Serial.begin(9600);

   Serial.println("Reading From the Sensor ...");

   delay(2000);

   }

void loop() {

   value= analogRead(sensor_pin);

   output_value = map(value,400,850,0,100);

   if(output_value < 0){
    output_value = 0;
   }
   
   if(output_value > 100) {
    output_value = 100;
   }

   Serial.print("Moisture : ");

   Serial.print(output_value);

   Serial.println("%");

   delay(1000);

   }
