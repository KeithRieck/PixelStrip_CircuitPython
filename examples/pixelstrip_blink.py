from time import sleep
from colors import *
import pixelstrip
import board

pixel = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB, auto_write=True)

pixel.brightness = 0.3
pixel.clear()

while True:
    pixel.fill(RED)
    sleep(0.5)
    pixel.fill(GREEN)
    sleep(0.5)
    pixel.fill(BLUE)
    sleep(2.5)
    