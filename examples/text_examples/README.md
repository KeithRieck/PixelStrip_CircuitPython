# Text display on an LED matrix

The `PixelStrip` can display text on LED matrices.  This functionality uses the Adafruit Bitmap Font library.

You must put the full directory for the `adafruit_bitmap_font` libraries into your `lib` directory, and you must have the font files installed and available to your CircuitPython program:

![Files](../../documentation/img/ciruitPython_files_TEXT.png)

Before drawing text, you must first load a font.  Fonts should be in [BDF](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format) format.  You can convert TrueType or OTF fonts to BDF using the [otf2bdf](https://linux.die.net/man/1/otf2bdf) tool or with [FontForge](https://fontforge.org/en-US/).


## References:
* [Fonts for CircuitPython Displays](https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display)
* [Adafruit Bitmap Font Library](https://docs.circuitpython.org/projects/bitmap-font/en/latest/index.html)
* [Adafruit fontio Library](https://docs.circuitpython.org/en/latest/shared-bindings/fontio/index.html)
