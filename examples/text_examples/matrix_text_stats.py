import board
import pixelstrip
from colors import *

# This Animation displays a series of texts.


class StatsAnimation(pixelstrip.Animation):
    def __init__(self, messages, color=BLUE, cycle_time=2.0):
        pixelstrip.Animation.__init__(self)
        self.color = color
        self.cycle_time = cycle_time
        self.stat_num = 0
        self.stats(messages)
        self.indent = self.width / 2

    def reset(self, strip):
        strip.clear()
        strip.show()
        self.timeout = self.cycle_time

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.timeout = self.cycle_time
            strip.clear()
            key = self.keys[self.stat_num]
            value = self.messages[key]
            print(f"{key} : {value}")
            strip.draw_text(key, color=WHITE)
            strip.draw_text(value, x=self.indent, color=GREEN)
            strip.show()
            self.stat_num = (self.stat_num + 1) % len(self.keys)

    def stats(self, messages):
        self.messages = messages
        self.keys = messages.keys()
        self.stat_num = 0


def main():
    matrix = pixelstrip.PixelStrip(board.GP4, width=32, height=8,
                                   bpp=4, pixel_order=pixelstrip.GRB,
                                   options={pixelstrip.MATRIX_TOP, pixelstrip.MATRIX_LEFT,
                                            pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix.brightness = 0.3
    matrix.load_font("fonts/proggy_tiny_12pt.bdf")
    messages = {'V': '11.5', 'A': '3.14', 'Z': ' 19.0', 'X': '18.2'}
    matrix.animation = StatsAnimation(messages,   cycle_time=0.1, color=GREEN)
    while True:
        matrix.draw()


main()
