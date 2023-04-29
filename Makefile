# Installing mpy-cross : https://ports.macports.org/port/mpy-cross/

build: lib/pixelstrip.mpy lib/colors.mpy lib/i2cp.mpy

lib/pixelstrip.mpy: pixelstrip.py
	mkdir -p lib
	mpy-cross pixelstrip.py -o lib/pixelstrip.mpy

lib/colors.mpy: colors.py
	mkdir -p lib
	mpy-cross colors.py -o lib/colors.mpy

lib/i2cp.mpy: i2cp.py
	mkdir -p lib
	mpy-cross i2cp.py -o lib/i2cp.mpy

clean:
	rm -rf lib
