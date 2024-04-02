# Notes about how to work with LED matrices

## How to set the strip options

When you are physically mounting LED strips or rings, you usually don't worry how they're oriented.  With LED matrices however, we often want to display a 2-dimensional image where it's important which side is up.  Depending on how you physically mount your matrix, you have to worry about which corner will be the "origin", i.e. the upper left corner.

Another complication with LED matrices is that some of them are wired in a zig-zag pattern, while others are wired in a progressive (orthogonal) layout.  Different layouts change the math about how to locate pixels within the `PixelStrip` library.

The constructor for `PixelStrip` has an `options` parameter which allows us to handle the layout variations and also to re-orient the matrix's origin.  

You may use the "matrix_test.py" program to figure out the optimal options. When this program runs it goes through the following sequence:
* The zeroth pixel (the first pixel in the strip) will blink red.
* The currently defined "origin" pixel will blink green.  We want to set the options so the origin pixel will be in the upper left corner.
* Yellow pixels will then trace out the full strip.  This will allow you to see whether the layout is zig-zag or progressive.
* Blue and white pixels will trace out the rows.  We want to set options so the lights progress from left to right and then from top to bottom.

To determine the correct options, do the following:
1. Set the options to be empty and run the program:  `options={}`   
2. Based on the yellow lights, determine if the layout is zig-zag or progressive.  If it is zig-zag, add `pixelstrip.MATRIX_ZIGZAG`.
3. If the green origin light is on the top row, add `pixelstrip.MATRIX_TOP` to the options.  If the green origin is on the bottom, add `pixelstrip.MATRIX_BOTTOM` to the options.  If the green origin is on the left or right, add either `pixelstrip.MATRIX_LEFT` or `pixelstrip.MATRIX_RIGHT`.
4. If the blue and white lights are tracing out columns instead of rows, add `pixelstrip.MATRIX_COLUMN_MAJOR` to the options.

