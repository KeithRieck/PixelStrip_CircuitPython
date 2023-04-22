# Setup for CircuitPython

Microcontrollers are miniature computers for use with electronics.  We will be programming the [Adafruit Feather RP2040](https://www.adafruit.com/product/4884) with the [CircuitPython](https://circuitpython.org/) language, which is an implementation of [Python 3](https://www.python.org/) for microcontrollers.  This is a powerful language in its own right, but skills developed in Python will be applicable to programming in [Java](https://en.wikipedia.org/wiki/Java_(programming_language)), [C](https://en.wikipedia.org/wiki/C_(programming_language)), or other languages.

![Raspberry Pi Pico](./img/rpi_pico_pinouts_bw.png)

You will need a Feather RP2040, a USB C cable, and a laptop. Install the [Visual Studio Code](https://code.visualstudio.com/) application.  Within Visual Studio Code (VSC), add the [CircuitPython plugin](https://marketplace.visualstudio.com/items?itemName=joedevivo.vscode-circuitpython).

To set up your Feather, you'll need to get the UF2 file containing the [latest version of CircuitPython](https://circuitpython.org/board/adafruit_feather_rp2040/).  Connect the micro USB cable to you Feather. Hold down the BOOTSEL button on the Pico before connecting the cable to your laptop.  A new drive should appear on the laptop.  Drag the UFC file onto the new drive.  After the file has loaded, unplug the cable from your laptop and then replug it.

The Feather will appear as a new flash disk called CIRCUITPY.  If you edit files on this volume, they will immedietly start executing under CircuitPython.  You can restart the code at any time by clicking the "Reset" button on the Feather.

## Blink Code

In the main window, type the following:

```python
from machine import Pin
from utime import sleep
led = Pin(25, Pin.OUT)
while True:
    led.on()
    sleep(0.5)
    led.off()
    sleep(2.0)
```

Save this program onto your Raspberry Pi Pico with the file name `main.py`, and then click the little green "Run" icon.  A small LED on the Pico should start blinking.  You can start and stop the program.  Modify the program to blink at different rates.

![led_setup](./img/led_setup_50.png)

Now try setting up this circuit on your breadboard.  The resistor can be any size, and should be connected to GPIO pin 16.  Note that the LED has a long wire and a short wire; the short wire should connect to the blue ground rail and the long wire should be connected near the resistor. (The long wire is called the Annode, while the short wire is called the Cathode.) Next, try adding more LEDs

```python
from machine import Pin
from utime import sleep

pin_16 = Pin(16, Pin.OUT)

while True:
    pin_16.toggle()
    sleep(1.0)
```

---

## Other Things to Try:
* Add switches for digital inputs.
* Code a traffic light

## References:
* MicroPython on the Pico:  https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
* Latest MicroPyton UFC for the [Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf): https://micropython.org/download/rp2-pico/rp2-pico-latest.uf2
* Latest MicroPyton UFC for the [Pico W](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf): https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2
* UFC to reset everything: https://cdn-learn.adafruit.com/assets/assets/000/099/419/original/flash_nuke.uf2
* Raspberry Pi Pico Pinout diagram:  https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf 

## Pinouts:
![Pinouts](./img/rpi_pico_pinouts.jpg)
