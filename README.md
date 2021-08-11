# PixelStrip_CircuitPython

PixelStrip is a small extension to AdaFruit's [Neopixel library](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel) for [CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython).  The PixelStrip library allows you to add Animations to the strip.  Multiple strips can have separate animations that run in parallel.

This library has been tested with the [Adafruit Feather RP2040](https://www.adafruit.com/product/4884).

## Installation

First, [download the latest CircuitPython libraries](https://circuitpython.org/libraries).
This package will contain the latest `neopixel.mpy` library, and others.

Second, [install the latest version of CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) onto your device.  Your device
will then appear as a USB drive on your computer named CIRCUITPY.  The drive will have 
a `lib` directory and the default program named `code.py`.

Now, copy the following libaries into the `lib` directory:
* `neopixel.mpy`
* `adafruit_pixelbuf.mpy`
* `pixelstrip.mpy`

Edit the `code.py` to execute PixelStrip animations.

## Simple Example

Wire up your Neopixels (WS2812B LEDs) for 5 volts, the ground, and digital input connecting 
to one of the board's GPIO pins (pin 12 in the following examples).

In code, create a PixelStrip object and assign colors to specific LEDs. Colors are coded
as tuples of four integers, each between 0 and 255.

```python
import time
import board
import pixelstrip

# Create a PixelStrip object connected to digital IO pin 12
strip = pixelstrip.PixelStrip(board.D12, 8, auto_write=True)

# Assign color values to individual LEDs
while True:
    strip[0] = (128, 0, 0, 0)
    time.sleep(0.5)
    strip[0] = (0, 0, 0, 0)
    time.sleep(0.5)
```

## Animation Example

Animations on a strip can be changed at any time.

New animations should extend `pixelstrip.Animation` and must at least define a new `draw()` function.

```python
import time
import board
import pixelstrip

# Define a new Animation
class BlinkAnimation(pixelstrip.Animation):
    def __init__(self):
        pixelstrip.Animation.__init__(self)

    def reset(self, strip):
        self.set_timeout(1.0)

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.set_timeout(1.0)
            lights_on = strip[0][0] != 0
            if lights_on:
                strip.fill((0, 0, 0, 0))
            else:
                strip[0] = (128, 0, 0, 0)
            strip.show()

# Create a PixelStrip object connected to digital IO pin 12
strip_12 = pixelstrip.PixelStrip(board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW)

# Assign an instance of the new Animation into the strip
strip_12.animation = BlinkAnimation()

# Repeatedly draw the strip, causing the Animation to run
while True:
    strip_12.draw()
    time.sleep(0.02)
```

