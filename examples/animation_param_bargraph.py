import board
import pixelstrip
from colors import *

class BarGraphAnimation(pixelstrip.Animation):
    """
    Fills in a strip where the number of pixels lit is determined
    by this Animation's 'param' value.
    """
    def __init__(self, cycle_time=0.5):
        pixelstrip.Animation.__init__(self)
        self.cycle_time = cycle_time

    def reset(self, strip):
        self.timeout = self.cycle_time
        strip.clear()

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.timeout = self.cycle_time
            param_val = 0 if self.param is None else int(self.param)
            for p in range(param_val):
                strip[p] = GRAY
            strip[param_val] = RED
            self.pixel_state = (self.pixel_state + 1) % 3
            strip.show()


if __name__ == "__main__":
    strip_gp15 = pixelstrip.PixelStrip(board.GP15, 24, bpp=4, pixel_order=pixelstrip.GRB)
    strip_gp15.animation = BarGraphAnimation()
    strip_gp15.animation.param = '7'
    while True:
        strip_gp15.draw()

