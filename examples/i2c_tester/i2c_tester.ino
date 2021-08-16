
#include <Wire.h>

// Tester code for i2c_animations.py.
// This Arduino program sends out a change-animation signal
// every five seconds.


const int I2C_ADDRESS = 4;
const int MAX_ANIMATIONS = 3;

void setup()
{
  Wire.begin();
  pinMode(LED_BUILTIN, OUTPUT);
}

byte strip_number = 0;
byte anim_number = 0;

void loop()
{
  Wire.beginTransmission(I2C_ADDRESS); 
  Wire.write(strip_number);
  Wire.write(anim_number);
  Wire.endTransmission();

  anim_number = (anim_number + 1) % MAX_ANIMATIONS;

  digitalWrite(LED_BUILTIN, HIGH);  
  delay(500);  
  digitalWrite(LED_BUILTIN, LOW); 

  delay(4500);
}
