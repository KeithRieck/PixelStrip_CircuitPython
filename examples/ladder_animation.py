import time
import board
import pixelstrip

class LadderAnimation(pixelstrip.Animation):
    def __init__(self):
        pixelstrip.Animation.__init__(self)
        self.pixel_state = 0

    def reset(self, strip):
        self.pixel_state = 0
        self.set_timeout(0.5)
        strip.clear()

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.set_timeout(0.5)
            self.pixel_state = (self.pixel_state + 1) % 3
            for p in range(strip.n):
                color = (0, 128, 0, 0) if ((p + self.pixel_state) % 3) == 0 else (0, 0, 0, 0)
                strip[p] = color
            strip.show()

strip_12 = pixelstrip.PixelStrip(board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW)

strip_12.animation = LadderAnimation()

while True:
    strip_12.draw()
    time.sleep(0.02)
