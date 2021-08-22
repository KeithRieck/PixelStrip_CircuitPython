import time
import board
import pixelstrip
from math import sin, floor

class PulseAnimation(pixelstrip.Animation):
    """
    Pixels are colored alternattely based on a color_list.
    Then, the different colors are pulsed bright to dark, each color
    slightly out of sequence.
    """
    def __init__(self, color_list=[(136, 0, 0, 0), (64, 64, 0, 0)], cycle_time=2.0):
        pixelstrip.Animation.__init__(self)
        self.color_list = color_list
        self.cycle_time = cycle_time

    def reset(self, strip):
        strip.clear()
        strip.show()

    def draw(self, strip, delta_time):
        t = pixelstrip.current_time() % self.cycle_time
        for p in range(strip.n):
            color_num = p % len(self.color_list)
            time_shift = color_num * (self.cycle_time / len(self.color_list))
            brightness = self.fade((t + time_shift) % self.cycle_time)
            color1 = self.color_list[color_num]
            color2 = self.fade_color(color1, brightness)
            strip[p] = color2
        strip.show()
    
    def fade(self, t):
        theta = 3.14159 * 2 * t / self.cycle_time
        return (sin(theta) + 1.0) / 2.0
    
    @staticmethod
    def fade_color(color, brightness):
        return (
            floor(color[0] * brightness),
            floor(color[1] * brightness),
            floor(color[2] * brightness),
            floor(color[3] * brightness),
        )

def main():
    strip_12 = pixelstrip.PixelStrip(board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW)
    strip_12.animation = PulseAnimation()
    while True:
        strip_12.draw()
        time.sleep(0.02)

main()
