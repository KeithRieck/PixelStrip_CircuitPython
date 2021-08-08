# PixelStrip_CircuitPython

PixelStrip is a small extension to AdaFruit's [Neopixel library](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel) for [CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython).  The PixelStrip library allows you to add Animations to the strip.  Multiple strips can have separate animations that run in parallel.

Animations on a strip can be changed at any time.

New animations should extend `pixelstrip.Animation` and must at least define a new `draw()` function.

```python
import time
import board
import pixelstrip

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


strip_12 = pixelstrip.PixelStrip(board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW)
strip_12.animation = BlinkAnimation()

while True:
    strip_12.draw()
    time.sleep(0.05)
```

