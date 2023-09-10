from time import sleep
from colors import *
import pixelstrip
import board

# This is an absolutly minimal program to demonstrate text displayed
# on a 32x8 matrix.

matrix = pixelstrip.PixelStrip(board.GP4, width=32, height=8, auto_write=True,
                               bpp=4, pixel_order=pixelstrip.GRB,
                               options={pixelstrip.MATRIX_TOP, pixelstrip.MATRIX_LEFT,
                                        pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})

matrix.brightness = 0.3
matrix.load_font("fonts/proggy_tiny_12pt.bdf")
matrix.clear()

while True:
    matrix.draw_text("Hello", monospace=False, color=YELLOW)
    sleep(1.0)
    matrix.clear()
    matrix.draw_text("World", monospace=False, color=BLUE)
    sleep(2.0)
    matrix.clear()
