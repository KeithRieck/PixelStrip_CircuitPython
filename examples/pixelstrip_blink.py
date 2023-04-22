from time import sleep
import board
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)
color = (0, 128, 128)

while True:
    lights_on = pixel[0][0] + pixel[0][1] + pixel[0][2] > 0
    next_color = (0, 0, 0) if lights_on else color
    pixel.fill(next_color)
    sleep(0.5)
