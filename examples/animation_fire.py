from time import sleep
from random import randint
from math import sin, floor
import board
import digitalio
import pixelstrip

PIN = 4
NUM_PIXELS = 144

blendSelf = 2
blendNeighbor1 = 3
blendNeighbor2 = 2
blendNeighbor3 = 1
blendTotal = (blendSelf + blendNeighbor1 + blendNeighbor2 + blendNeighbor3)


class FireAnimation(pixelstrip.Animation):
    """
    See https://github.com/davepl/DavesGarageLEDSeries/blob/master/LED%20Episode%2010/include/fire.h
    """
    def __init__(self, cooling=60, sparking=50, sparks=3, sparkheight=4):
        pixelstrip.Animation.__init__(self)
        self.cooling = cooling
        self.sparking = sparking
        self.sparks = sparks
        self.sparkHeight = sparkheight
        self.heat = None

    def reset(self, strip):
        self.heat = [0] * strip.n
        strip.clear()

    def draw(self, strip, delta_time):
        size = strip.n
        
        # First cool each cell by a little bit
        cool_range = floor(((self.cooling * 10) / size) + 2)
        for p in range(size):
            self.heat[p] = max(0, floor(self.heat[p] - randint(0, cool_range)))
            
        # Next drift heat up and diffuse it a little bit
        for p in range(3, size):
            self.heat[p] = floor((self.heat[p] * blendSelf + 
                       self.heat[(p - 1) % strip.n] * blendNeighbor1 + 
                       self.heat[(p - 2) % strip.n] * blendNeighbor2 + 
                       self.heat[(p - 3) % strip.n] * blendNeighbor3) / blendTotal) % 256

        # Randomly ignite new sparks down in the flame kernel
        for _ in range(self.sparks):
            if randint(0, 255) < self.sparking:
                p = randint(0, self.sparkHeight)
                self.heat[p] = (self.heat[p] + randint(160, 255)) % 256

        for p in range(size):
            strip[p] = heat_color(self.heat[p])

        strip.show()
        
def heat_color(temperature):
    """Translate a temperature number (0-255) into a color representing its heat"""
    t192 = scale8_video(temperature, 192)
    heatramp = (t192 & 0x3F) << 2
    if t192 & 0x80:
        return (0xFF, 0xFF, heatramp, 0x00)
    elif t192 & 0x40:
        return (0xFF, heatramp, 0x00, 0x00)
    else:
        return (heatramp, 0x00, 0x00, 0x00)
    
def scale8_video(i, sc):
    return floor((i * sc) / 256)

def blink(n, strip=None):
    """Blink lights to show that the program has loaded successfully"""
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    if strip:
        strip.clear()
    for _ in range(n):
        led.value = True
        if strip:
            strip[0] = (0, 128, 0, 0)
            strip.show()
        sleep(0.3)
        led.value = False
        if strip:
            strip.clear()
            strip.show()
        sleep(0.3)


if __name__ == "__main__":
    strip_gp15 = pixelstrip.PixelStrip(board.GP15, NUM_PIXELS, bpp=4, pixel_order=pixelstrip.GRB)
    strip_gp15.animation = FireAnimation(cooling=70, sparking=30)
    blink(3, strip=strip_gp15)
    while True:
        strip_gp15.draw()
        sleep(0.02)
        





