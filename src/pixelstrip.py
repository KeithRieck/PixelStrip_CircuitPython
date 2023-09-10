# Copyright (c) 2023, Keith Rieck
# All rights reserved.

import time
import neopixel
from adafruit_bitmap_font import bitmap_font

RGB = "RGB"
GRB = "GRB"
RGBW = "RGBW"
GRBW = "GRBW"


def current_time():
    """
    Returns the current time in seconds.
    """
    return time.monotonic()


MATRIX_TOP = 0x01           # Pixel 0 is at top of matrix
MATRIX_BOTTOM = 0x02        # Pixel 0 is at bottom of matrix
MATRIX_LEFT = 0x04          # Pixel 0 is at left of matrix
MATRIX_RIGHT = 0x08         # Pixel 0 is at right of matrix
MATRIX_ROW_MAJOR = 0x10     # Matrix is row major (horizontal)
MATRIX_COLUMN_MAJOR = 0x20  # Matrix is column major (vertical)
MATRIX_PROGRESSIVE = 0x40   # Same pixel order across each line
MATRIX_ZIGZAG = 0x80        # Pixel order reverses between lines


class PixelStrip():
    """
    Extends NeoPixel, but supporting Animations.
    """

    def __init__(
        self, pin, n=8, width=None, height=None, brightness=1.0, options=None, auto_write=False, bpp=4,  pixel_order=None
    ):
        self._options = {MATRIX_PROGRESSIVE,
                         MATRIX_ROW_MAJOR, MATRIX_TOP, MATRIX_LEFT}
        self.width = n
        self.height = 1
        if width is not None and height is not None:
            n = width * height
            self.width = width
            self.height = height
        if options is not None:
            self._options = options
        self._timeout = None
        self._animation = None
        self._prev_time = current_time()
        self.wrap = False
        self.CLEAR = (0, 0, 0, 0) if bpp == 4 else (0, 0, 0)
        self.font = None
        self.npxl = neopixel.NeoPixel(
            pin,
            n,
            brightness=brightness,
            auto_write=auto_write,
            bpp=bpp,
            pixel_order=pixel_order,
        )

    def show(self):
        self.npxl.show()

    def fill(self, color):
        self.npxl.fill(color)

    def _setitem(self, index, color):
        self.npxl[index] = color

    @property
    def n(self):
        return len(self.npxl)

    def __len__(self):
        return len(self.npxl)

    def draw(self):
        """
        Draw one cycle of the strip animation.
        """
        if self._animation is not None:
            delta_time = current_time() - self._prev_time
            self._animation.draw(self, delta_time)
            self._prev_time = current_time()

    def reset(self):
        """
        Reset the strip animation.
        """
        self._prev_time = current_time()
        if self._animation is not None:
            self._animation.reset(self)
        else:
            self.clear()

    def clear(self):
        """
        Turn all pixels off.
        """
        self.fill(self.CLEAR)
        self.show()

    def __getitem__(self, index):
        return self.npxl[index]

    def __setitem__(self, index, color):
        if type(index) is tuple:
            nn = self._translate_pixel(index[0], index[1])
        else:
            nn = index
        if self.wrap:
            while nn < 0:
                nn += len(self)
            while nn >= len(self):
                nn -= len(self)
        self._setitem(nn, color)

    def _translate_pixel(self, x, y):
        xx = x
        yy = y

        if MATRIX_TOP in self._options and MATRIX_RIGHT in self._options:
            xx = y
            yy = self.height - (x + 1)
        elif MATRIX_BOTTOM in self._options and MATRIX_RIGHT in self._options:
            xx = self.width - (x + 1)
            yy = self.height - (y + 1)
        elif MATRIX_BOTTOM in self._options and MATRIX_LEFT in self._options:
            xx = self.width - (y + 1)
            yy = x

        if MATRIX_ZIGZAG in self._options:
            if MATRIX_COLUMN_MAJOR in self._options and xx % 2 == 1:
                yy = self.height - (yy + 1)
            elif MATRIX_ROW_MAJOR in self._options and yy % 2 == 1:
                xx = self.width - (xx + 1)

        if MATRIX_COLUMN_MAJOR in self._options:
            return xx * self.height + yy
        else:
            return xx + yy * self.width

    @property
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, anim):
        self._animation = anim
        if self._animation is not None:
            self._animation.reset(self)
        else:
            self.clear()

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, t):
        """
        Set or reset a timeout (in seconds) on this PixelStrip.
        Setting with None cancels the timeout.
        """
        if t < 0 or t is None:
            self._timeout = None
        else:
            self._timeout = current_time() + t

    def is_timed_out(self):
        """
        Determine if the timeout has been reached.
        """
        if self._timeout is None:
            return False
        else:
            return current_time() >= self._timeout

    def load_font(self, font_file):
        """
        Loads a bdf or pcf font file.
        """
        self.font_file = font_file
        self.font = bitmap_font.load_font(font_file)

    def draw_text(self, message, x=0, y=0, color=(0xFF, 0xFF, 0xFF, 0x00), monospace=True):
        pixels_changed = 0
        if self.font is None:
            return 0
        width, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(message)
        for yy in range(height):
            xx = 0
            for c in message:
                glyph = self.font.get_glyph(ord(c))
                if not glyph or c == ' ':
                    xx += width
                    continue
                glyph_y = yy + (glyph.height - (height + dy)) + glyph.dy
                if 0 <= glyph_y < glyph.height:
                    for i in range(glyph.width):
                        value = glyph.bitmap[i, glyph_y]
                        xxx = int(x+xx+i)
                        yyy = int(y+yy)
                        if value > 0 and xxx >= 0 and xxx < self.width and yyy >= 0 and yyy < self.height:
                            self.__setitem__((xxx, yyy), color)
                            pixels_changed = pixels_changed + 1
                if monospace:
                    xx += width
                else:
                    xx += glyph.width + 1
        return pixels_changed

    def draw_line(self, x1, y1, x2, y2, color=(0xFF, 0xFF, 0xFF, 0x00)):
        pixels_changed = 0
        if y1 == y2:
            xx = x1 if x1 <= x2 else x2
            ww = 1 + abs(x2 - x1)
            for i in range(ww):
                self.__setitem__((xx+i, y1), color)
                pixels_changed = pixels_changed + 1
        elif x1 == x2:
            yy = y1 if y1 <= y2 else y2
            hh = 1 + abs(y2 - y1)
            for i in range(hh):
                self.__setitem__((x1, yy+i), color)
                pixels_changed = pixels_changed + 1
        else:
            xx = x1 if x1 <= x2 else x2
            yy = y1 if y1 <= y2 else y2
            ww = 1 + abs(x2 - x1)
            hh = float(y2 - y1)
            for i in range(ww):
                j = int(i/hh)
                self.__setitem__((xx+i, yy+j), color)
                pixels_changed = pixels_changed + 1
        return pixels_changed

    def draw_rect(self, x, y, w, h, fill=False, color=(0xFF, 0xFF, 0xFF, 0x00)):
        pixels_changed = 0
        if fill:
            for i in range(h):
                pixels_changed = self.draw_line(x, y+i, x+w, y+i, color) + pixels_changed
        else:
            pixels_changed = self.draw_line(x, y, x+w, y, color) + pixels_changed
            pixels_changed = self.draw_line(x, y, x, y+h, color) + pixels_changed
            pixels_changed = self.draw_line(x, y+h, x+w, y+h, color) + pixels_changed
            pixels_changed = self.draw_line(x+w, y, x+w, y+h, color) + pixels_changed
        return pixels_changed


class Animation:
    """
    Base class for all animations.
    """

    def __init__(self, name=None):
        self._timeout = None
        self._name = name

    def __repr__(self):
        t = self.__class__.__name__
        n = "" if self._name is None else self._name
        return "{}({})".format(t, n)

    def __str__(self):
        t = self.__class__.__name__
        return t if self._name is None else self._name

    def reset(self, strip):
        """
        Reset this animation for the given pixel strip.
        """
        pass

    def draw(self, strip, delta_time):
        """
        Draw one cycle of this animation against the given pixel strip.
        The delta_time is the number of seconds since the last draw call.
        """
        pass

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, t):
        """
        Set or reset a timeout (in seconds) on this PixelStrip.
        Setting with None cancels the timeout.
        """
        if t < 0 or t is None:
            self._timeout = None
        else:
            self._timeout = current_time() + t

    def is_timed_out(self):
        """
        Determine if the timeout has been reached.
        """
        if self._timeout is None:
            return False
        else:
            return current_time() >= self._timeout
