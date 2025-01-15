from time import sleep
from colors import *
import board
import pixelstrip
import digitalio

TIME = 0.500

# matrix = pixelstrip.PixelStrip(board.GP15, width=8, height=8, bpp=4, pixel_order=pixelstrip.GRB, options={pixelstrip.MATRIX_TOP, pixelstrip.MATRIX_LEFT, pixelstrip.MATRIX_ZIGZAG})
matrix = pixelstrip.PixelStrip(board.GP15, width=8, height=8, bpp=4, pixel_order=pixelstrip.GRB, options={pixelstrip.MATRIX_COLUMN_MAJOR, pixelstrip.MATRIX_ZIGZAG})
matrix.clear()
matrix.timeout = TIME

state = 0
p = 0
led_color = BLUE

while True:
    if matrix.is_timed_out():
        matrix.clear()
        if state == 0:
            matrix[0, p] = led_color
            p = p + 1
            if p >= matrix.width:
                state = 1
                p = 1
        elif state == 1:
            matrix[p, matrix.width] = led_color
            p = p + 1
            if p >= matrix.height:
                state = 2
                p = 7
        elif state == 2:
            matrix[matrix.height, p] = led_color
            p = p - 1
            if p >= matrix.width:
                state = 3
                p = 7
        elif state == 3:
            matrix[p, 0] = led_color
            p = p - 1
            if p >= matrix.height:
                state = 0
                p = 0  
        matrix.show()
        matrix.timeout = TIME