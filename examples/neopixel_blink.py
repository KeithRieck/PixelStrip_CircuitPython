from time import sleep
import board
import neopixel

pixel = neopixel.NeoPixel(board.GP15, 1)
# pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pixel.brightness = 0.3

while True:
    pixel.fill((255, 0, 0, 0))
    sleep(0.5)
    pixel.fill((0, 255, 0, 0))
    sleep(0.5)
    pixel.fill((0, 0, 255, 0))
    sleep(0.5)