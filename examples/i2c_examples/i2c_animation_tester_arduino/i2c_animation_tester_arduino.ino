
#include <Wire.h>

// Tester code for i2c_animations.py.
// This Arduino program sends out a change-animation signal
// every five seconds.


const int I2C_ADDRESS = 0x41;
const int MAX_ANIMATIONS = 3;          // Must be 32 or less
const int MAX_STRIPS = 2;              // Must be 8 or less

void setup()
{
  Wire.begin();
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

byte strip_number = 0;
byte anim_number = 0;

void loop()
{
  strip_number = (strip_number + 1) % MAX_STRIPS;
  if (strip_number == 0) {
    anim_number = (anim_number + 1) % (MAX_ANIMATIONS + 1);
  }

  Serial.print("sent ");
  Serial.print(strip_number); Serial.print(" ");
  Serial.print(anim_number); Serial.print("     ");
  byte b = ((strip_number << 5) & 0xE0) + (anim_number & 0x1F);
  Wire.beginTransmission(I2C_ADDRESS);
  if (anim_number == 0) {
    char message[4] = "x25";
    message[0] = b;
    Wire.write(message);
    Serial.println("message");
  } else {
    Wire.write(b);
    Serial.println("byte");
  }
  Wire.endTransmission();

  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);

  delay(4500);
}