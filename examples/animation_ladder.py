import board
import pixelstrip

class LadderAnimation(pixelstrip.Animation):
    """
    Every third pixel is colored.  The pixels travel down the strip.
    """
    def __init__(self, color=(0, 128, 0, 0), cycle_time=0.5):
        pixelstrip.Animation.__init__(self)
        self.color = color
        self.cycle_time = cycle_time
        self.pixel_state = 0

    def reset(self, strip):
        self.pixel_state = 0
        self.timeout = self.cycle_time
        strip.clear()

    def draw(self, strip, delta_time):
        if self.is_timed_out():
            self.timeout = self.cycle_time
            self.pixel_state = (self.pixel_state + 1) % 3
            for p in range(strip.n):
                color = self.color if ((p + self.pixel_state) % 3) == 0 else (0, 0, 0, 0)
                strip[p] = color
            strip.show()


if __name__ == "__main__":
    strip_gp15 = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB)
    strip_gp15.animation = LadderAnimation()
    while True:
        strip_gp15.draw()

