import board
import pixelstrip
from math import sin, floor, ceil


class RippleAnimation(pixelstrip.Animation):
    """
    Pixels fade in and out of color, based on the sum of sine curves.
    """
    def __init__(
        self,
        color_list=[(0, 0, 0, 0), (255, 0, 0, 0), (128, 128, 0, 0), (0, 0, 0, 0)],
        curve_list=[(0.125, 1.0, 1.0), (0.156, 0.8, 0.9), (0.100, 1.1, 1.1)],
        cycle_time=40.0,
        x_span=100,
    ):
        pixelstrip.Animation.__init__(self)
        self.color_list = color_list
        self.cycle_time = cycle_time
        self.x_span = x_span
        self.curve_list = curve_list

    def reset(self, strip):
        strip.clear()
        strip.show()

    def draw(self, strip, delta_time):
        m = pixelstrip.current_time() * 1000.0
        for p in range(strip.n):
            c = 0.0
            for curve in self.curve_list:
                c = c + self.g(p, m, curve[0], curve[1], curve[2])
            c = c / len(self.curve_list)
            c = min(max(c, 0.0), 1.0)
            strip[p] = self.shift_color(c)
        strip.show()

    def f(self, x, t, w):
        return sin(t + 6.28 * x / (w * 2 * self.x_span))

    def g(self, x, m, w, a, d):
        s = d * self.cycle_time
        t0 = ((m % (s * 2)) - s) / s
        t = 6.28 * sin(6.28 * t0)
        return self.f(x, t, w) * a

    def shift_color(self, c):
        color_list_size = len(self.color_list) - 1
        color_num_0 = floor(c * color_list_size)
        color_num_1 = ceil(c * color_list_size)
        c0 = (c - color_num_0 / color_list_size) * color_list_size
        c1 = 1.0 - c0
        return (
            (c0 * self.color_list[color_num_0][0] + c1 * self.color_list[color_num_1][0]),
            (c0 * self.color_list[color_num_0][1] + c1 * self.color_list[color_num_1][1]),
            (c0 * self.color_list[color_num_0][2] + c1 * self.color_list[color_num_1][2]),
            (c0 * self.color_list[color_num_0][3] + c1 * self.color_list[color_num_1][3])
        )


if __name__ == "__main__":
    strip_gp15 = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB)
    strip_gp15.animation = RippleAnimation(x_span=8)
    while True:
        strip_gp15.draw()
