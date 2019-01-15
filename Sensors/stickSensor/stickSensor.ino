/*#include <Wire.h>
 int state = 0;
void writeI2CRegister8bit(int addr, int reg, int value) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.write(value);
  Wire.endTransmission();
}
 
void writeI2CRegister8bit(int addr, int value) {
  Wire.beginTransmission(addr);
  Wire.write(value);
  Wire.endTransmission();
}
 
void setup() {
  Wire.begin();
  Serial.begin(9600);
                                       //talking to the default address 0x20
  writeI2CRegister8bit(0x20, 1, 0x21); //change address to 0x21
  writeI2CRegister8bit(0x20, 6);       //reset
  delay(1000);                         //give it some time to boot
}

void loop()
{
  byte error, address;
  int nDevices;
  
 while(state == 0){
  Serial.println("Scanning...");
 
  nDevices = 0;
  for(address = 1; address < 127; address++ )
  {
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
 
    if (error == 0)
    {
      Serial.print("I2C device found at address 0x");
      if (address<16)
        Serial.print("0");
      Serial.print(address,HEX);
      Serial.println("  !");
      state = 1;
      nDevices++;
    }
    else if (error==4)
    {
      Serial.print("Unknow error at address 0x");
      if (address<16)
        Serial.print("0");
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("done\n");
 
  delay(5000);           // wait 5 seconds for next scan
 }
}

*/


int light;
int moisture;
int temperature;

int mapped_light;
int mapped_moisture;
int mapped_temperature;

#include <Wire.h>

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

void setup() {
  Wire.begin();
  Wire.setClockStretchLimit(2500);
  Serial.begin(9600);
  writeI2CRegister8bit(0x20, 6); //reset
}

void loop() {
  Serial.print(readI2CRegister16bit(0x20, 0)); //read capacitance register
  Serial.print(", ");
  Serial.print(readI2CRegister16bit(0x20, 5)); //temperature register
  Serial.print(", ");
  writeI2CRegister8bit(0x20, 3); //request light measurement 
  Serial.println(readI2CRegister16bit(0x20, 4)); //read light register
  delay(500);

  moisture = readI2CRegister16bit(0x20, 0);
  temperature = readI2CRegister16bit(0x20, 5);
  light = readI2CRegister16bit(0x20, 4);

  //moisture 200 / 722
  //light 65535 / 0
  //room temperature = 250

  mapped_moisture = map(moisture, 200, 722, 0, 100);
  mapped_light = map(light, 5000, 0, 0, 100);
  mapped_temperature = temperature - 215;

  if(mapped_light > 5000){
    mapped_light = 5000;
  }

  if(mapped_light < 0){
    mapped_light = 0;
  }
  
  Serial.print(mapped_moisture);
  Serial.print(", ");
  Serial.print(mapped_light);
  Serial.print(", ");
  Serial.println(mapped_temperature);
  
}
