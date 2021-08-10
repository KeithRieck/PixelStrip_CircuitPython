import time
import board
import pixelstrip

strip = pixelstrip.PixelStrip(board.D12, 8, auto_write=True)

while True:
    strip[0] = (128, 0, 0, 0)
    time.sleep(0.5)
    strip[0] = (0, 0, 0, 0)
    time.sleep(0.5)
