import time
import board
import pixelstrip

class SpinningAnimation(pixelstrip.Animation):
    """
    One colored pixel travels across the strip.
    """
    def __init__(self, color, cycle_time=1.0):
        pixelstrip.Animation.__init__(self)
        self.color = color
        self.current_pixel = 0
        self.cycle_time = cycle_time
        self.wait_time = self.cycle_time / 8

    def reset(self, strip):
        self.current_pixel = 0
        self.wait_time = self.cycle_time / strip.n
        self.set_timeout(self.wait_time)

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.set_timeout(self.wait_time)
            self.current_pixel = (self.current_pixel + 1) % strip.n
            strip.clear()
            strip[self.current_pixel] = self.color
            strip.show()

strip_12 = pixelstrip.PixelStrip(board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW)

strip_12.animation = SpinningAnimation((128, 64, 0, 0))

while True:
    strip_12.draw()
    time.sleep(0.05)
