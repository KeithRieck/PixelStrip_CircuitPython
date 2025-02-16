# Pixelstrip Example Code

This directory contains example code using the PixelStrip framework.

## Basic code
* [blink.py](blink.py) : This program just blinks the microcontroller's onboard LED.  This program is useful for verifying that your hardware is working properly.
* [neopixel_blink.py](neopixel_blink.py) : This program just blinks a pixel. This program that does _not_ use the PixelStrip framework, but goes directly to Adafruit's [NeoPixel](https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels) library.
* [pixelstrip_blink.py](pixelstrip_blink.py) : This program just blinks a pixel using the PixelStrip framework.

 ## Animation Examples
 * [animation_minimal.py](animation_minimal.py) : This is a template to be used when createing a new Animation class.  This example uses a [timeout](../documentation/doc_animation.md#timeout), but you can create a non-timeout Animation by removing that code.
 * [animation_spinning.py](animation_spinning.py) : Animation that causes a colored pixel to travel across a strip, or spin around a ring.  It uses a timeout for timing.
 * [animation_pulse.py](animation_pulse.py) : An Animation that causes pixels to brighten or fade using a sine wave.  It operates as fast as possible, without using a timeout.

 ## Matrix Examples
 * [matrix_test.py](matrix_test.py) : This program tests a pixel matrix by running through all the pixels.  It can be used to determine the correct [options](../documentation/matrix_notes.md) to use when constructing a PixelStrip matrix object. 
 * [multi_matrix.py](multi_matrix.py) : Defines a `MultiMatrix` class that can be used when multiple matrixes are wired together.
