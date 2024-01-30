# Copyright (c) 2024, Keith Rieck
# All rights reserved.

import struct

class BmpFile:
    """
    Reads and parses a BMP pixel file.
    """
    def __init__(self, file_name): 
        with open(file_name, 'rb') as fp:
            self.file_name = file_name

            # File Header
            self.bfType = fp.read(2)
            self.bfSize = struct.unpack('I', fp.read(4))[0]
            self.bfReserved1 = fp.read(2)
            self.bfReserved2 = fp.read(2)
            self.bfOffBits = struct.unpack('I', fp.read(4))[0]

            # Info Header
            self.biSize = struct.unpack('I', fp.read(4))[0]
            self.biWidth = abs(struct.unpack('i', fp.read(4))[0])
            self.biHeight = abs(struct.unpack('i', fp.read(4))[0])
            self.biPlanes = struct.unpack('H', fp.read(2))[0]
            self.biBitCount = struct.unpack('H', fp.read(2))[0]
            self.biCompression = struct.unpack('I', fp.read(4))[0]
            self.biSizeImage = struct.unpack('I', fp.read(4))[0]
            self.biXPelsPerMeter = struct.unpack('i', fp.read(4))[0]
            self.biYPelsPerMeter = struct.unpack('i', fp.read(4))[0]
            self.biClrUsed = struct.unpack('I', fp.read(4))[0]
            self.biClrImportant = struct.unpack('I', fp.read(4))[0]
            self.width = self.biWidth
            self.height = self.biHeight

            assert (self.biBitCount == 32 or self.biBitCount == 24), "Only 32 and 24 bit images are supported"
            assert (self.biCompression == 0), "Compression is not supported"

            # Pixel Data
            fp.seek(self.bfOffBits)
            self.values = []
            for i in range(self.width * self.height):
                b = struct.unpack('B', fp.read(1))[0]
                g = struct.unpack('B', fp.read(1))[0]
                r = struct.unpack('B', fp.read(1))[0]
                if self.biBitCount == 32:
                    fp.read(1)
                self.values.append((r, g, b, 0))

    def __iter__(self):
        yield from self.values
    
    def __getitem__(self, index):
        if type(index) is tuple:
            x = index[0]
            y = index[1]
            return self.values[x + y * self.width]
        else:
            return self.values[index]
    
    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return f"BmpFile('{self.file_name}', width={self.biWidth}, height={self.biHeight}, bits={self.biBitCount})"

    def info(self):
        return f"""file_name:       {self.file_name}
bfType:          {self.bfType}
bfSize:          {self.bfSize} 
bfOffBits:       {self.bfOffBits} 
biSize:          {self.biSize}
biWidth:         {self.biWidth}
biHeight:        {self.biHeight} 
biPlanes:        {self.biPlanes}
biBitCount:      {self.biBitCount}
biCompression:   {self.biCompression}
biSizeImage:     {self.biSizeImage}
biXPelsPerMeter: {self.biXPelsPerMeter}
biYPelsPerMeter: {self.biYPelsPerMeter}
biClrUsed:       {self.biClrUsed}
biClrImportant:  {self.biClrImportant}
"""


