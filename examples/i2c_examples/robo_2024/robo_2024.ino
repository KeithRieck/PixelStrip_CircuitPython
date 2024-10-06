#include <Wire.h>

const int CIRCLE1 = 0;
const int CIRCLE2 = 1;
const int CIRCLE3 = 2;

const int LINMATRIX = 3;
const int LINMATRIX1 = 4;
const int LINMATRIX2 = 5;

const int MATRIX = 6;

const int CONWAYS = 7;

const int ORANGE_REVERSE_MATRIX = 8;
const int ORANGE_REVERSE_MATRIX1 = 9;
const int ORANGE_REVERSE_MATRIX2 = 10;
const int ORANGE_REVERSE_MATRIX3 = 11;

const int FLASH = 12;

const int FILLRED = 13;
const int FILLGREEN = 14;
const int FILLWHITE = 15;

const int BITMAP = 16;

const int POINTER = 17;

const int BIGPID = 1;
const int PERIMETERID = 0;
const int HEADID = 2;
const int BACKID = 3;
const int SIDEID = 4;

int send_state = 0;
unsigned long led_time = -1;

const int I2C_ADDRESS = 0x41;

const int BTN_FLINGER_ON = 10;
const int BTN_FLINGER_OFF = 1;
const int BTN_DISABLED = 31;
const int BTN_INTAKE = 16;
const int BTN_NOTE_LOADED = 34;
const int BTN_OTHER = 29;
int btn_list[] = {BTN_FLINGER_ON, BTN_FLINGER_OFF, BTN_DISABLED, BTN_INTAKE, BTN_NOTE_LOADED, BTN_OTHER};

int flinger_on = 0;

  void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(BTN_FLINGER_ON, INPUT_PULLUP);
  pinMode(BTN_FLINGER_OFF, INPUT_PULLUP);
  pinMode(BTN_DISABLED, INPUT_PULLUP);
  pinMode(BTN_INTAKE, INPUT_PULLUP);
  pinMode(BTN_NOTE_LOADED, INPUT_PULLUP);
  pinMode(BTN_OTHER, INPUT_PULLUP);

  send_state = 0;
  led_time = millis() + 500;
  Wire.begin();
  Serial.begin(9600);
}

void loop()
{
  // Read the buttons
  int btn_number = -1;
  for (int i = 0; i < 6; i++)
  {
    if (digitalRead(btn_list[i]) == LOW)
    {
      btn_number = i;
      break;
    }
  }

  if (millis() > (led_time + 500))
  {
    if (btn_number > -1)
    {
      if (send_state == 0)
      {

        if (btn_number == BTN_DISABLED)
        {
          setAnimation(PERIMETERID, LINMATRIX); // linear_matrix.py
          setAnimation(BIGPID, CONWAYS);        // conways_game_of_life.py
          setAnimation(HEADID, LINMATRIX1);     // linear_matrix.py
          setAnimation(BACKID, LINMATRIX2);     // linear_matrix.py
          setAnimation(SIDEID, MATRIX);         // matrix.py
        }
        else if (btn_number == BTN_INTAKE)
        {
          setAnimation(PERIMETERID, CIRCLE1);           // circle_spinner.py
          setAnimation(BIGPID, ORANGE_REVERSE_MATRIX);  // orange_reverse_matrix.py
          setAnimation(HEADID, CIRCLE2);                // circle_spinner.py
          setAnimation(BACKID, CIRCLE3);                // circle_spinner.py
          setAnimation(SIDEID, ORANGE_REVERSE_MATRIX1); // orange_reverse_matrix.py
        }
        else if (btn_number == BTN_NOTE_LOADED)
        {
          setAnimation(PERIMETERID, FLASH); // Flash.py
          setAnimation(BIGPID, FLASH);      // Flash.py
          setAnimation(HEADID, FLASH);      // Flash.py
          setAnimation(BACKID, FLASH);      // Flash.py
          setAnimation(SIDEID, FLASH);      // Flash.py
        }
        else if (btn_number == BTN_OTHER)
        {
          setAnimation(PERIMETERID, FILLGREEN); // Fill.py
          setAnimation(BIGPID, BITMAP);         // animation_bitmap.py
          setAnimation(HEADID, FILLWHITE);      // Fill.py
          setAnimation(BACKID, FILLRED);        // Fill.py
          setAnimation(SIDEID, FILLGREEN);      // Fill.py
        }
        if (btn_number == BTN_FLINGER_ON) {
          flinger_on = 1;
        } else if (btn_number == BTN_FLINGER_OFF) {
          flinger_on - 0;
        }
        if (flinger_on)
        {
          setAnimation(BIGPID, ORANGE_REVERSE_MATRIX2); // orange_reverse_matrix.py
          setAnimation(SIDEID, POINTER);                // pointer.py
        }

        send_state = 1;
        led_time = millis() + 500;
        delay(100);
      }
    }
    else
    {
      if (send_state == 1)
      {
        send_state = 0;
        Serial.println("UP");
      }
    }
  }

  // Turn on LED for a half second after sending a signal
  if (millis() < led_time)
  {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else
  {
    digitalWrite(LED_BUILTIN, LOW);
  }
}

void setAnimation(int strip_number, int anim_number)
{
  byte b = ((strip_number << 5) & 0xE0) + (anim_number & 0x1F);
  Wire.beginTransmission(I2C_ADDRESS);
  int bytesTransmitted = Wire.write(b);
  byte status = Wire.endTransmission();
  Serial.print("WIRE: ");
  Serial.print(bytesTransmitted);
  Serial.print(" bytes : status = ");
  Serial.println(status);
  delay(100);
}