import pixelstrip

class MultiMatrix(pixelstrip.PixelStrip):
    """
    Makes one large matrix out of multiple pixel matrices.
    Connect the matrices together in series.
    Parameters
    ----------
    m : int
        Number of matrices
    w : int
        Width of one matrix
    h : int
        Height of one matrix
    """
    def __init__(self, pin, m=1, w=32, h=8, brightness=1.0, auto_write=False, bpp=4,  pixel_order=None ):
        pixelstrip.PixelStrip.__init__(self, pin, n=w*h*m, 
                                       brightness=brightness, auto_write=auto_write, bpp=bpp, 
                                       pixel_order=pixel_order)
        self.m = m
        self.w = w
        self.h = h
        self.height = m * h
        self.width = w

    def _translate_pixel(self, x, y):
        xx = x
        yy = y % self.h
        mm = int(y / self.h)
        if xx % 2 == 1:
            yy = self.h - (yy + 1)
        return xx * self.h + yy + mm * (self.w * self.h)
