# Annimation Objects

`Animation` classes define how LEDs change over time.  Constructing instances of one of these clases yields `Animation` objects that can be attached to `PixelStrip` objects.

---

## Constructors

```python
strip1 = pixelstrip.Animation()
strip2 = pixelstrip.Animation(name='Blinking animation')
```
Construct an `Animation`.

`Animation` is an abstract class, so you will never construct an `Animation` directly.  Instead, you will create your own class that extends `Animation`, which will then have its own constructor.   Your custom animation class will call the parent `Animation` constructor.

The `name` parameter is optional, but it allows you to attach a name to any `Animation` object.  This may be useful while debugging.

Here is a minimal `Animation` class to get you started:

```python
class MyAnimation(pixelstrip.Animation):
    def __init__(self):
        pixelstrip.Animation.__init__(self)
        # variable setup

    def reset(self, strip):
        # reset variables
        # set timeout if needed
        strip.clear()
        strip.show()

    def draw(self, strip, delta_time):
        # change pixel values
        strip.show()
```

---

## Properties

### timeout

```python
self.timeout = 0.5   # Nmber of seconds
```
Setting the `timeout` property to a number of seconds means that the `Animation` will be timed out that many
seconds in the future.  Setting `timeout` to `None` clears the timeout.

Note that there is also an [is_timed_out](#is_timed_out) that returns `True` or `False` to tell you if the timeout has expired.

Note that this is very similar to the timeout on `PixelStrip`, but it is a _different timeout_.  If you set the timeout on your `PixelStrip`, but then try to use that same timeout on your `Animation`, you will be confused about why it is not working.


---

## Methods

### draw(strip, delta_time)

```python
def draw(self, strip, delta_time):
    # Change some pixels
    strip.show()
```

This is the main routine you must define within your new `Animation` class.  It determines what the animation does.  The `delta_time` variable is the number of seconds since the last `draw()` call.

It is mandatory to define this method in each custom animation class. However, you will probably never call it directly.  
Instead, call the `PixelStrip` method to `draw()`.


### reset(strip)

```python
def reset(self, strip):
    # reset variables
```

This method will be called whenever you assign the `Animation` to a strip or whenever you call the `reset()` method on the `PixelStrip`.

Defining the `reset()` method is optional.  If you don't need to reset anything, you need not create it.  

You will probably never call it directly.  Instead, call the similar method on `PixelStrip`.


### is_timed_out()

```python
if self.is_timed_out():
    pass
```

Returns `True` if the animation's timeout has expired.

