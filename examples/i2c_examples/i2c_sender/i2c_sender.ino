#include <Wire.h>

// Tester code for i2c_animations.py.

const int I2C_ADDRESS = 0x41;

const int STRIP_0 = 10;
const int STRIP_1 = 4;
const int STRIP_2 = 27;
const int STRIP_3 = 32;
const int STRIP_4 = 12;

const int ANIM_0 = 1;
const int ANIM_1 = 45;
const int ANIM_2 = 17;
const int ANIM_3 = 31;
const int ANIM_4 = 16;
const int ANIM_5 = 34;
const int ANIM_6 = 29;

int strip_list[] = { STRIP_0, STRIP_1, STRIP_2, STRIP_3, STRIP_4};
int strip_count = 5;
int anim_list[] = {ANIM_0, ANIM_1, ANIM_2, ANIM_3, ANIM_4, ANIM_5, ANIM_6};
int anim_count = 7;

int send_state = 0;
unsigned long led_time = -1;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  for (int i = 0; i < strip_count; i++) {
    pinMode(strip_list[i], INPUT_PULLUP);
  }
  for (int i = 0; i < anim_count; i++) {
    pinMode(anim_list[i], INPUT_PULLUP);
  }
  send_state = 0;
  led_time = millis() + 500;
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  int strip_number = -1;
  int anim_number = -1;

  // Read the Strip buttons
  for (int i = 0; i < strip_count; i++) {
    if (digitalRead(strip_list[i]) == LOW) {
      strip_number = i;
      break;
    }
  }

  // Read the animation buttons
  for (int i = 0; i < anim_count; i++) {
    if (digitalRead(anim_list[i]) == LOW) {
      anim_number = i;
      break;
    }
  }

  // If both strip and animation are specified, send out the I2c signal
  if (millis() > (led_time + 500)) {
    if (strip_number > -1 && anim_number > -1) {
      if (send_state == 0) {
        Serial.print("DOWN (");
        Serial.print(strip_number);
        Serial.print(", ");
        Serial.print(anim_number);
        Serial.println(")");

        byte b = ((strip_number << 5) & 0xE0) + (anim_number & 0x1F);
        Wire.beginTransmission(I2C_ADDRESS);
        int bytesTransmitted = Wire.write(b);
        byte status = Wire.endTransmission();  // Try optional true / false parameter
        Serial.print("WIRE: ");
        Serial.print(bytesTransmitted);
        Serial.print(" bytes : status = ");
        Serial.println(status);

        send_state = 1;
        led_time = millis() + 500;
        delay(20);
      }
    } else {
      if (send_state == 1) {
        send_state = 0;
        Serial.println("UP");
      }
    }
  }

  // Turn on LED for a half second after sending a signal
  if (led_time > 0 && millis() < led_time) {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
