import board
import pixelstrip
from colors import *

# This is a a minimal example of an Animation.
# All Animations must define a draw().  It's also a good
# idea to define an __init__ function for initializing the 
# Animation and a reset function to reset things every time
# the Animation restarts.

class MyAnimation(pixelstrip.Animation):
    """
    Write a description of this Animation here.
    """
    def __init__(self, cycle_time=0.5)):
        pixelstrip.Animation.__init__(self)
        self.cycle_time = cycle_time
        # variable setup

    def reset(self, strip):
        self.timeout = self.cycle_time
        strip.clear()
        strip.show()
        # reset variables

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            # change pixel values
            strip.show()
            self.timeout = self.cycle_time


if __name__ == "__main__":
    strip_gp15 = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB)
    strip_gp15.animation = MyAnimation()
    while True:
        strip_gp15.draw()

