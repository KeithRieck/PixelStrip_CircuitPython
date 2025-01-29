import board
import pixelstrip
from colors import *

class VoltageAnimation(pixelstrip.Animation):
    """
    Display's the robot's current voltage on a matrix.
    Voltage is received into the 'param' property.
    """
    def __init__(self, cycle_time=0.25):
        pixelstrip.Animation.__init__(self)
        self.cycle_time = cycle_time

    def reset(self, strip):
        self.timeout = self.cycle_time
        strip.clear()

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            strip.clear()
            strip.draw_text('V:', color=GRAY)
            voltage_val = float(self.param)
            cc = GREEN if voltage_val >= 11.5 else RED
            strip.draw_text(str(voltage_val), x=7, color=cc)
            strip.show()
            self.timeout = self.cycle_time


if __name__ == "__main__":
    matrix = pixelstrip.PixelStrip(board.GP15, width=32, height=8,
                                   bpp=4, pixel_order=pixelstrip.GRB,
                                   options={pixelstrip.MATRIX_TOP, pixelstrip.MATRIX_LEFT,
                                            pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
    matrix.brightness = 0.3
    matrix.load_font("fonts/proggy_tiny_12pt.bdf")
    a = VoltageAnimation()
    a.param = '0.0'
    matrix.animation = a
    
    while True:
        matrix.draw()
