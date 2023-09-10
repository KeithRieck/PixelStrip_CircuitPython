from adafruit_bitmap_font import bitmap_font
from pixelstrip import PixelStrip
import board

# Load this program on you Pico or Feather to test out fonts.
# You don't need any LED strips attached to your microcontroller.
# When executed, this program will print out the message to the
# serial monitor with one character per pixel.


class FontTester(PixelStrip):
    def __init__(self):
        PixelStrip.__init__(self, board.GP12)
        self.matrix = None
        self.num_rows = 1
        self.num_cols = 1

    def test_text(self, message):
        print(f"font = {self.font_file}  : {self.font}")
        width, height, dx, dy = self.font.get_bounding_box()
        print(f"font_file: {self.font_file}")
        print(
            f"bounding_box : {width} x {height}       x-offset / y-offset : {dx} / {dy}")

        self.font.load_glyphs(message)
        glyph = self.font.get_glyph(ord("M"))
        self.num_cols = len(message) * glyph.width
        self.num_rows = height
        print(
            f"M_size : {glyph.width} x {glyph.height}       message_size : {self.num_cols} x {self.num_rows}")

        self.matrix = []
        for yy in range(self.num_rows):
            self.matrix.append([' '] * self.num_cols)

        self.draw_text(message, 0, 0)

        self.print_grid()

    def __setitem__(self, index, color):
        x = index[0]
        y = index[1]
        row = self.matrix[y]
        if x < len(row):
            row[x] = '#'

    def print_grid(self):
        for row in self.matrix:
            print("".join(row))


tester = FontTester()
tester.load_font("fonts/proggy_tiny_12pt.bdf")
tester.test_text("Volts: 12.3456")
