# PixelStrip Animations

Up until now, we have been creating moving lights on a single strip of WS2812B LEDs.

When we deploy to the robot, we will want to control multiple strips of LEDs running simultaneously. Also, we'd like to be able to switch animations as needed.  To do this, we will abstract out each animation as a separate `Animation` object.  This is not too complex.  I should point out that doing this in Python is much simpler than the way we used to do it in C++.

For each animation type, you must define an Animation `class`.  The class then allows you to create separate animation `objects`.   When you attach an animation object each strip object, that animation can start executing.   Here is a simple example of an `Animation`:

```Python
from pixelstrip import PixelStrip, Animation, GRB
import board
from colors import *

# Define a new Animation
class BlinkAnimation(Animation):
    def __init__(self):
        Animation.__init__(self)

    def reset(self, strip):
        self.timeout = 0.0

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            is_light_on = (strip[0][0] + strip[0][1] + strip[0][2]) > 0
            if is_light_on:
                strip.clear()
            else:
                strip[0] = BLUE
            strip.show()
            self.timeout = 1.0

if __name__ == "__main__":
    # Create a PixelStrip object connected to digital IO pin GP15
    strip = PixelStrip(board.GP15, 24, bpp=4, pixel_order=GRB)

    # Assign an instance of the new Animation into the strip
    strip.animation = BlinkAnimation()

    # Repeatedly draw the strip, causing the Animation to run
    while True:
        strip.draw()
```

Here is another animation.  Note that this animation uses a local variable `p` to store the curent location of the moving pixel:

```Python
from pixelstrip import PixelStrip, Animation, GRB
import board
from colors import *

class SparkAnimation(Animation):
    def __init__(self):
        Animation.__init__(self)
        self.p = 0
        
    def reset(self, strip):
        self.timeout = 0.0

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            strip.clear()
            strip[self.p] = WHITE
            strip[self.p - 1] = YELLOW
            strip[self.p - 2] = MAROON
            strip.show()
            self.p = (self.p + 1) % strip.n
            self.timeout = 0.3

if __name__ == "__main__":
    strip = PixelStrip(board.GP15, 24, bpp=4, pixel_order=GRB)
    strip.wrap = True
    strip.animation = SparkAnimation()
    while True:
        strip.draw()
```
