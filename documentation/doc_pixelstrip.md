# PixelStrip Objects

`PixelStrip` software objects are interfaces to WS2812 RGB LED collections.
Each WS2812 strip will be connected to a specific pin on your Adafruit Feather
The strip will have a specific size (i.e. number of pixels).

---

## Constructors

```python
strip = pixelstrip.PixelStrip(pin, size)
```
Construct a `PixelStrip` for the given pin and size.


```python
strip = pixelstrip.PixelStrip(pin, n=8, brightness=1.0, auto_write=False)
```

Construct a `PixelStrip` for the given pin.  The strip size is given by the `n` parameter.  Other parameters are optional.


```python
strip = pixelstrip.PixelStrip(pin, width=16, height=8, brightness=1.0, auto_write=False, options=None)
```
Construct a `PixelStrip` for a pixel matrix of the given width and height.  The `brightness`, `auto_write`, and `options` parameters are optional.


The `options` parameter is important for specifying how your pixel matrix is wired and positioned.  If it is not `None`, then it should a Python set containing one or more of the following:
* `MATRIX_TOP`          Pixel 0 is at top of matrix
* `MATRIX_BOTTOM`       Pixel 0 is at bottom of matrix
* `MATRIX_LEFT`         Pixel 0 is at left of matrix
* `MATRIX_RIGHT`        Pixel 0 is at right of matrix
* `MATRIX_ROW_MAJOR`    Matrix is row major (horizontal)
* `MATRIX_COLUMN_MAJOR` Matrix is column major (vertical)
* `MATRIX_PROGRESSIVE`  Same pixel order across each line
* `MATRIX_ZIGZAG`       Pixel order reverses between lines

If you are using a linear strip of LEDs rather than a matrix, don't worry about the `option` parameter.

---

## Array Operations on PixelStrips

All `PixelStrip` objects can be treated as if they were [Python arrays](https://www.w3schools.com/python/python_lists.asp), so you can set colors into strip at any given pixel number.  For instance, writing a color into `strip[0]` will change the color of the first pixel.  You can also read back the color by reading `strip[0]`.

Colors on the `PixelStrip` are represented as a three-number [Python tuple](https://www.w3schools.com/python/python_tuples.asp).  The three numbers give the amount of red, green, and blue in the color.  Each number should be in the range from 0 to 255.  Typically we use hexadecimal numbers, although you can also use normal decimal.

Examples:
```python
strip[0] = RED                 # Set the first pixel to be red
strip[1] = (0x00, 0xff, 0x00)  # Set the second pixel to be green
strip[2] = (255, 255, 0)       # Set the third pixel to be yellow
strip[2,6] = BLUE              # Set a pixel in the third column and seventh row of a matrix
```

Other ways to change pixel colors would be to call the fill() or clear() commands.  

---

## Properties

### n

```python
strip.n     # number of pixels on the strip
len(strip)  # another way to get the number of pixels
```
Reading `n` tells the total number of pixels on the strip.  Do not try to modify this property.


### width

```python
strip.width    # number of pixel columns in a matrix
```
The `width` and `height` properties give the dimensions of a matrix.  The `width` gives the number of pixels on the horizontal axis.  Do not try to modify this property.


### height

```python
strip.height    # number of pixel rows in a matrix
```
The `height` gives the number of pixels on the vertical axis.   If the given `PixelStrip` is not a matrix, then the height will be 1.  Do not try to modify this property.


### animation

```python
strip.animation = SpinningAnimation(LIGHTBLUE)   # Animation object or None
```

Setting the `animation` property to an [Animation](doc_animation.md) object causes that animation to reset and started.  It is best not to assign the same `Animation` object to multiple strips.

Setting the `animation` property to `None` stops all animaton on the strip and clears all pixels.


### timeout

```python
strip.timeout = 2.0   # Number of seconds
```
Setting the `timeout` property to a number of seconds means that the strip will be timed out that many
seconds in the future.  Setting `timeout` to `None` clears the timeout.

Note that there is also a [is_timed_out](#is_timed_out)] function that returns `True` or `False` to tell you if the timeout has expired.

Timeouts are a big deal in `PixelStrip` animations.  A timeout is like a timer allowing you to cause something to happen in the future.  For instance, if you want to update your pixels five times a second, then you might set a timeout for 0.2 seconds.  You would code an `if` statement to change pixels colors after the timeout.  The last item in your `if` body would reset the timeout to occur again 0.2 seconds from now.


### brightness

```python
strip.brightness = 0.7   # Relative brightness between 0.0 and 1.0
```
Setting `brightness` instantly changes the strips brightness.


### auto_write

```python
strip.auto_write = True   # Boolean value.
```
If `auto_write` is set to `True`, then changes are written automatically, without having to call the [show()](#show)  method.  By default, this property is `False`.

It is recommended that you leave this value as `False`.  It will be more efficient to push all changes out at the same time with `strip.show()`.


### wrap

```python
strip.wrap = True   # Boolean value.
```
If `wrap` is set to `True`, then specfiying indices outside the strip's range will be automatically be
wrapped forward or backward.   By default, this property is `False`.


---

## Methods

### show()

```python
strip.show()
```

Causes all pixel changes to be written out to the strip.

Normal operation is to change pixel colors and then call the `show()` method.  Alternatively, you could set the strip's [auto_write](#auto_write) property to `True`, in which case all changes are pushed out to the strip as they are made.


### fill(color)

```python
strip.fill(GREEN)
```

Causes all pixels on the strip to be set to the given color.  You must call [show()](#show) for this to be visible.


### clear()

```python
strip.clear()
```

Causes all pixels on the strip to be turned off.   You must call [show()](#show)  for this to be visible.


### draw()

```python
strip.draw()
```

Cause the strip to draw the next cycle of the current [Animation](doc_animation.md)

If the strip has no `Animation` specified, nothing will happen.

Changes will not be visible until [show()](#show)  is called, or if [auto_write](#auto_write) is turned on.


### reset()

```python
strip.reset()
```

Cause the strip to call the current [Animation](doc_animation.md) `reset()` method.  Typically, this will cause the `Animation` to restart from the beginning.

If the strip has no `Animation` specified, nothing will happen.


### is_timed_out()

```python
if strip.is_timed_out():
    pass
```

Returns `True` if the strip's timeout has expired.


---

## Colors

A number of useful color constants are defined by the `colors.py` file:


| | | | | |
|---------|---------|----------|----------|----------|
| `ALICEBLUE` | `AMETHYST` | `ANTIQUEWHITE` | `AQUA` | `AQUAMARINE` |
| `AZURE` | `BEIGE` | `BISQUE` | `BLACK` | `BLANCHEDALMOND` |
| `BLUE` | `BLUEVIOLET` | `BROWN` | `BURLYWOOD` | `CADETBLUE` |
| `CHARTREUSE` | `CHOCOLATE` | `CORAL` | `CORNFLOWERBLUE` | `CORNSILK` |
| `CRIMSON` | `CYAN` | `DARKBLUE` | `DARKCYAN` | `DARKGOLDENROD` |
| `DARKGRAY` | `DARKGREY` | `DARKGREEN` | `DARKKHAKI` | `DARKMAGENTA` |
| `DARKOLIVEGREEN` | `DARKORANGE` | `DARKORCHID` | `DARKRED` | `DARKSALMON` |
| `DARKSEAGREEN` | `DARKSLATEBLUE` | `DARKSLATEGRAY` | `DARKSLATEGREY` | `DARKTURQUOISE` |
| `DARKVIOLET` | `DEEPPINK` | `DEEPSKYBLUE` | `DIMGRAY` | `DIMGREY` |
| `DODGERBLUE` | `FIREBRICK` | `FLORALWHITE` | `FORESTGREEN` | `FUCHSIA` |
| `GAINSBORO` | `GHOSTWHITE` | `GOLD` | `GOLDENROD` | `GRAY` |
| `GREY` | `GREEN` | `GREENYELLOW` | `HONEYDEW` | `HOTPINK` |
| `INDIANRED` | `INDIGO` | `IVORY` | `KHAKI` | `LAVENDER` |
| `LAVENDERBLUSH` | `LAWNGREEN` | `LEMONCHIFFON` | `LIGHTBLUE` | `LIGHTCORAL` |
| `LIGHTCYAN` | `LIGHTGOLDENRODYELLOW` | `LIGHTGREEN` | `LIGHTGREY` | `LIGHTPINK` |
| `LIGHTSALMON` | `LIGHTSEAGREEN` | `LIGHTSKYBLUE` | `LIGHTSLATEGRAY` | `LIGHTSLATEGREY` |
| `LIGHTSTEELBLUE` | `LIGHTYELLOW` | `LIME` | `LIMEGREEN` | `LINEN` |
| `MAGENTA` | `MAROON` | `MEDIUMAQUAMARINE` | `MEDIUMBLUE` | `MEDIUMORCHID` |
| `MEDIUMPURPLE` | `MEDIUMSEAGREEN` | `MEDIUMSLATEBLUE` | `MEDIUMSPRINGGREEN` | `MEDIUMTURQUOISE` |
| `MEDIUMVIOLETRED` | `MIDNIGHTBLUE` | `MINTCREAM` | `MISTYROSE` | `MOCCASIN` |
| `NAVAJOWHITE` | `NAVY` | `OLDLACE` | `OLIVE` | `OLIVEDRAB` |
| `ORANGE` | `ORANGERED` | `ORCHID` | `PALEGOLDENROD` | `PALEGREEN` |
| `PALETURQUOISE` | `PALEVIOLETRED` | `PAPAYAWHIP` | `PEACHPUFF` | `PERU` |
| `PINK` | `PLAID` | `PLUM` | `POWDERBLUE` | `PURPLE` |
| `RED` | `ROSYBROWN` | `ROYALBLUE` | `SADDLEBROWN` | `SALMON` |
| `SANDYBROWN` | `SEAGREEN` | `SEASHELL` | `SIENNA` | `SILVER` |
| `SKYBLUE` | `SLATEBLUE` | `SLATEGRAY` | `SLATEGREY` | `SNOW` |
| `SPRINGGREEN` | `STEELBLUE` | `TAN` | `TEAL` | `THISTLE` |
| `TOMATO` | `TURQUOISE` | `VIOLET` | `WHEAT` | `WHITE` |
| `WHITESMOKE` | `YELLOW` | `YELLOWGREEN` |  |

