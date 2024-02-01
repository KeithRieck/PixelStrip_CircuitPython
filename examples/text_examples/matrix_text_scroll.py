import board
import pixelstrip
from colors import *

# This Animation displays a text message scrolling across a 32x8 matrix.


class ScrollAnimation(pixelstrip.Animation):
    def __init__(self, message, color=YELLOW, cycle_time=0.5):
        pixelstrip.Animation.__init__(self)
        self.color = color
        self.cycle_time = cycle_time
        self.message = message
        self.xx = 0

    def reset(self, strip):
        self.xx = 0
        strip.clear()
        strip.show()
        self.timeout = self.cycle_time

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.timeout = self.cycle_time
            strip.clear()
            p = strip.draw_text(self.message, x=self.xx, color=self.color)
            self.xx = self.xx - 1 if p > 0 else 0
            strip.show()


if __name__ == "__main__":
    matrix = pixelstrip.PixelStrip(board.GP4, width=32, height=8,
                                   bpp=4, pixel_order=pixelstrip.GRB,
                                   options={pixelstrip.MATRIX_TOP, pixelstrip.MATRIX_LEFT,
                                            pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix.brightness = 0.3
    matrix.load_font("fonts/proggy_tiny_12pt.bdf")
    matrix.animation = ScrollAnimation(
        "The quick brown fox jumped over the lazy dog.", 
        cycle_time=0.1, color=GREEN)
    while True:
        matrix.draw()

