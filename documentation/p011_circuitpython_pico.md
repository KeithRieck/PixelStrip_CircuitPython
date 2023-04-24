# Setup for CircuitPython on a Raspberry Pi Pico

Microcontrollers are miniature computers for use with electronics.  We will be programming the [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) with the [CircuitPython](https://circuitpython.org/) language, which is an implementation of [Python 3](https://www.python.org/) for microcontrollers.  This is a powerful language in its own right, but skills developed in Python will be applicable to programming in [Java](https://en.wikipedia.org/wiki/Java_(programming_language)), [C](https://en.wikipedia.org/wiki/C_(programming_language)), or other languages.

![Raspberry Pi Pico](./img/pico.jpg)

You will need a Pico, a micro USB cable, and a laptop. Install the [Visual Studio Code](https://code.visualstudio.com/) application.  Within Visual Studio Code (VSC), add the [CircuitPython plugin](https://marketplace.visualstudio.com/items?itemName=joedevivo.vscode-circuitpython).

To set up your microcontroller, you'll need to get the UF2 file containing the [latest version of CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/) specific for your board.  Connect the USB cable to your board. Hold down the BOOTSEL button before connecting the cable to your laptop.  A new drive should appear on the laptop.  Drag the UF2 file onto the new drive.  After the file has loaded, unplug the cable from your laptop and then replug it.

The microcontroller will appear as a new flash disk called CIRCUITPY.  If you edit files on this volume, they will immedietly start executing under CircuitPython.  On a Feather board you can restart the code at any time by clicking the "Reset" button.

## Blink Code

In the main editor window, type the following and save with the file name `main.py`:

```python
from time import sleep
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    sleep(0.5)
    led.value = False
    sleep(0.5)
```

Once saved, the program should start executing and a small LED on the board should start blinking.  You can start and stop the program.  Modify the program to blink at different rates.

![led_setup](./img/led_setup_50_pico.png)

Now try setting up this circuit on your breadboard.  The resistor can be any size, and should be connected to GPIO pin 16.  Note that the LED has a long wire and a short wire; the short wire should connect to the blue ground rail and the long wire should be connected near the resistor. (The long wire is called the Annode, while the short wire is called the Cathode.) Next, try adding more LEDs

```python
from time import sleep
import board
import digitalio

pin_15 = digitalio.DigitalInOut(board.GP15)
pin_15.direction = digitalio.Direction.OUTPUT
toggle = True

while True:
    pin_15.value = toggle
    sleep(1.0)
    toggle = not toggle
```

> Note that the Pico is a little different from the Feather.
> The pins are numbered differently.  For these examples, use `board.GP15` on the Pico instead of `board.D12`.  On the Pico the number 15 pin will be on the corner.

---

## Other Things to Try:
* Add switches for digital inputs.
* Code a traffic light

## References:
* Raspberry Pi Pico documentation:  https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html
* Raspberry Pi Pico Pinout diagram:  https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg

