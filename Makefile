# Compile Python files into CircuitPython MPY files

# MPY_CROSS = $(HOME)/Documents/bin/mpy-cross-macos-11-8.2.7-universal
MPY_CROSS = $(HOME)/Documents/bin/mpy-cross-macos-11-9.0.5-universal

build: lib lib/pixelstrip.mpy lib/i2cp.mpy lib/bmp.mpy lib/colors.mpy

lib:
	mkdir -p lib

lib/pixelstrip.mpy: src/pixelstrip.py
	$(MPY_CROSS) src/pixelstrip.py -o lib/pixelstrip.mpy

lib/i2cp.mpy: src/i2cp.py
	$(MPY_CROSS) src/i2cp.py -o lib/i2cp.mpy


lib/bmp.mpy: src/bmp.py
	$(MPY_CROSS) src/bmp.py -o lib/bmp.mpy

lib/colors.mpy: src/colors.py
	$(MPY_CROSS) src/colors.py -o lib/colors.mpy

clean:
	rm -rf lib


# Installing myp-cross: https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/
# Installing mpy-cross on Mac: https://ports.macports.org/port/mpy-cross/
# See also: https://pypi.org/project/mpy-cross/
# See also: http://adafru.it/mpy-update
