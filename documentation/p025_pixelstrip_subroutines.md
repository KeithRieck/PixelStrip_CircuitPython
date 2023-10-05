# PixelStrip in CircuitPython - Subroutines

Here is code that defines a subroutine to draw a spark, which moves across the strip.

```python
import pixelstrip
import board
from colors import *

strip = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB)
strip.wrap = True
strip.timeout = 0.0

def draw_spark(s, p):
    s[p] = WHITE
    s[p-1] = RED
    s[p-2] = YELLOW

p = 4
while True:
    if strip.is_timed_out():
        strip.clear()
        draw_spark(strip, p)
        p = (p + 1) % strip.n
        strip.show()
        strip.timeout = 0.1
```

Try changing the spark drawing subroutine.  Try causing two or three sparks to move across the strip.

Here is code that makes one pixel move back and forth.:

```python
import pixelstrip
import board
from colors import *

strip = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB)
strip.timeout = 0.0
c = GREEN
p = 0
j = 1

while True:
    if strip.is_timed_out():
        strip.clear()
        strip[p] = c
        if p == strip.n-1:
            j = -1
            p = p - 1
        elif p == 0:
            j = 1
            p = 1
        else:
            p = p + j
        strip.show()
        strip.timeout = 0.2
```

Change the above code so the pixel changes colors every time it bounces off the top or bottom.  Try changing the speed of the pixel so gets slower as it reaches the top of the strip, so it looks like a bouncing ball.

This code defines a function that generates new colors that are midway between two other colors:

```python
import pixelstrip
import board
from colors import *

strip = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB)
strip.wrap = True
strip.timeout = 0.0

def shift_color(c1, c2, m):
    r = int(c1[0] * m + c2[0] * (1-m))
    g = int(c1[1] * m + c2[1] * (1-m))
    b = int(c1[2] * m + c2[2] * (1-m))
    return (r, g, b, 0)

i = 0
while True:
    if strip.is_timed_out():
        for p in range(strip.n):
            m = p / float(strip.n)
            strip[p+i] = shift_color(BLUE, YELLOW, m)
        i = (i + 1) % strip.n
        strip.show()
        strip.timeout = 0.2
```
