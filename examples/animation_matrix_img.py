import board
import pixelstrip
from colors import *


class ImageAnimation(pixelstrip.Animation):

    def __init__(self, cycle_time=0.1)):
        pixelstrip.Animation.__init__(self)
        self.cycle_time = cycle_time
        self.current_frame = 0
        self.imgdata = [[[0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 2, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 2, 0, 1], [1, 1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 1, 2, 1], [3, 3, 0, 4, 4, 0, 0, 0]]]
        self.colorlist = [(12, 0, 0), (0, 0, 0), (0, 12, 12), (8, 0, 0), (11, 0, 12)]

    def reset(self, matrix):
        self.timeout = self.cycle_time
        matrix.clear()
        matrix.show()
        self.current_frame = 0

    def draw(self, matrix, delta_time):
        if self.is_timed_out():
            self.draw_image(matrix, self.current_frame)
            self.current_frame = (self.current_frame + 1) % len(self.imgdata)
            matrix.show()
            self.timeout = self.cycle_time
    
    def draw_image(self, matrix, frame):
        matrix.clear()
        for i in range(len(self.imgdata[frame])):
            print(self.imgdata[frame])
            for j in range(len(self.imgdata[frame][0])):
                matrix[i, 7-j] = self.colorlist[self.imgdata[frame][i][j]]
    



if __name__ == "__main__":
    matrix_gp15 = pixelstrip.PixelStrip(board.GP15, 8, bpp=4, pixel_order=pixelstrip.GRB)
    matrix_gp15.animation = ImageAnimation()
    while True:
        matrix_gp15.draw()
