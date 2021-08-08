import time
import board
import pixelstrip

class SpinningAnimation(pixelstrip.Animation):
    """
    One colored pixel travels across the strip.
    """
    def __init__(self, color, spin_time=1.0):
        self.color = color
        self.current_pixel = 0
        self.spin_time = spin_time
        self.wait_time = self.spin_time / 8

    def reset(self, strip):
        self.current_pixel = 0
        self.wait_time = self.spin_time / strip.n
        self.set_timeout(self.wait_time)

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.set_timeout(self.wait_time)
            self.current_pixel = (self.current_pixel + 1) % strip.n
            strip.clear()
            strip[self.current_pixel] = self.color
            strip.show()

strip = pixelstrip.PixelStrip(board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW)

strip.animation = SpinningAnimation((128, 64, 0, 0))

while True:
    strip.draw()
    time.sleep(0.05)
