import time
import board
import pixelstrip

# This is a a minimal example of an Animation.
# All Animations must define a draw().  It's also a good
# idea to define an __init__ function for initializing the 
# Animation and a reset function to reset things every time
# the Animation restarts.

class MyAnimation(pixelstrip.Animation):
    def __init__(self):
        self.pixel_state = 0

    def reset(self, strip):
        self.pixel_state = 0
        self.set_timeout(0.5)
        strip.clear()

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.set_timeout(0.5)
            self.pixel_state = (self.pixel_state + 1) % 3
            for i in range(strip.n):
                color = (0, 128, 0, 0) if ((i + self.pixel_state) % 3) == 0 else (0, 0, 0, 0)
                strip[i] = color
            strip.show()

strip = pixelstrip.PixelStrip(board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW)

strip.animation = MyAnimation()

while True:
    strip.draw()
    time.sleep(0.05)
