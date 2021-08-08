import time
import neopixel

RGB = "RGB"
GRB = "GRB"
RGBW = "RGBW"
GRBW = "GRBW"

class PixelStrip(neopixel.NeoPixel):
    """
    Subclass of NeoPixel, but supporting Animations.
    """

    def __init__(
        self, pin, n, bpp=3, brightness=1.0, auto_write=False, pixel_order=None
    ):
        neopixel.NeoPixel.__init__(
            self,
            pin,
            n,
            bpp=bpp,
            brightness=brightness,
            auto_write=auto_write,
            pixel_order=pixel_order,
        )
        self._animation = None
        self._prev_time = time.monotonic()
        self.CLEAR = (0, 0, 0, 0) if bpp == 4 else (0, 0, 0)

    def draw(self):
        """
        Draw one cycle of the strip animation.
        """
        if self._animation is not None:
            delta_time = time.monotonic() - self._prev_time
            self._animation.draw(self, delta_time)
            self._prev_time = time.monotonic()

    def reset(self):
        """
        Reset the strip animation.
        """
        self._prev_time = time.monotonic()
        if self._animation is not None:
            self._animation.reset(self)
    
    def clear(self):
        """
        Turn all pixels off.
        """
        self.fill(self.CLEAR)

    @property
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, anim):
        self._animation = anim
        if self._animation is not None:
            self._animation.reset(self)


class Animation:
    """
    Base class for all animations.
    """
    def __init__(self):
        self._timeout = None

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
    
    def set_timeout(self, t):
        """
        Set or reset a timeout (in seconds) on this Animation.
        Setting with None cancels the timeout.
        """
        if t == 0 or t is None:
            self._timeout = None
        else:
            self._timeout = time.monotonic() + t
    
    def is_timed_out(self):
        """
        Determine if the timeout has been reached.
        """
        if self._timeout is None:
            return False
        else: 
            return time.monotonic() >= self._timeout
