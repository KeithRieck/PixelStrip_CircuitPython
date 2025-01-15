import board
import pixelstrip

strip = pixelstrip.PixelStrip(board.GP15, 8)
strip.timeout = 0.0

cycle_time = 2.0
current_pixel = 0

while True:
    if strip.is_timed_out():
        strip.timeout = cycle_time / strip.n
        strip.fill((0, 0, 0, 0))
        for p in range(current_pixel):
            strip[p] = (64, 64, 0, 0)
        current_pixel = (current_pixel % strip.n) + 1
        strip.show()
