import board
import pixelstrip
import digitalio
from animation_pulse import PulseAnimation
import busio

I2C_ADDRESS = 4
BRIGHTNESS = 0.5

# List of Animations
animation = [
    PulseAnimation(),
    PulseAnimation([(0, 136, 0, 0), (64, 64, 0, 0)]),
    PulseAnimation([(0, 0, 136, 0), (0, 64, 64, 0)]),
]

# List of PixelStrips
strip = [
    pixelstrip.PixelStrip(
        board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW, brightness=BRIGHTNESS
    )
]

def receive_message(time=0.02):
    with busio.I2C(scl=board.SCL, sda=board.SDA) as i2c:
        if i2c.try_lock():
            try:
                buffer = bytearray(2)
                i2c.readfrom_into(1, buffer)
                strip_num = int(buffer[0])
                anim_num = int(buffer[1])
                return (strip_num, anim_num)
            finally:
                i2c.unlock()
        else:
            return None


# The built-in LED will turn on for half a second after every message
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def main():
    for s in strip:
        s.clear()
    last_msg_time = 0.0
    while True:
        for s in strip:
            s.draw()
        message = receive_message(time=0.02)
        if message:
            strip_num = message[0]
            anim_num = message[1]
            strip[strip_num] = animation[anim_num]
            last_msg_time = pixelstrip.current_time()
        led = pixelstrip.current_time() < last_msg_time + 0.5


main()
