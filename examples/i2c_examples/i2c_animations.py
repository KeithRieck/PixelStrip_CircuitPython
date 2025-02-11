import digitalio
import board
from time import sleep
from i2ctarget import I2CTarget
from pixelstrip import PixelStrip, current_time
from colors import *

from animation_pulse import PulseAnimation

I2C_ADDRESS = 0x41
BRIGHTNESS = 0.5

# List of Animations
animation = [
    PulseAnimation(),
    PulseAnimation([(0, 136, 0, 0), (64, 64, 0, 0)]),
    PulseAnimation([(0, 0, 136, 0), (0, 64, 64, 0)]),
]

# List of PixelStrips
strip = [
    PixelStrip(board.GP8, 8, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS),
    PixelStrip(board.GP5, 8, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS)
]

# The built-in LED will turn on for half a second after every message 
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

i2c = None


def receive_message():
    """
    Receive a message through I2C, if available.  The first byte will
    contain the strip number and animation number, packed into the single
    byte.  If there is a param associated with this message, it is 
    concatenated after the first byte.
    """
    global i2c
    message = i2c.request()
    if not message:
        return None
    with message:
        message_bytes = message.read()
        b = message_bytes[0]
        strip_num = int((b & 0xE0) >> 5)
        anim_num = int(b & 0x1F)
        param = None 
        if len(message_bytes) > 1:
            param = message_bytes[1:].decode('utf-8')
        print(f"received {len(message_bytes)} bytes      {(strip_num, anim_num, param)}")
        return (strip_num, anim_num, param)


def main(i2c): 
    "Main program loop, for reading messages and changing Animations."
    global strip, led
    last_msg_time = 0.0
    while True:
        for s in strip:
            s.draw()
        message = receive_message()
        if message is not None:
            strip_num = message[0]
            anim_num = message[1]
            if strip_num < len(strip) and anim_num < len(animation):
                strip[strip_num].animation = animation[anim_num]
                if message[2] is not None or animation[anim_num].param is not None:
                    animation[anim_num].param = message[2]
            elif strip_num < len(strip):
                strip[strip_num].animation = None
            last_msg_time = current_time()
        led.value = (current_time() < last_msg_time + 0.5)


def blink(n, color=BLUE, sleep_time=0.4): 
    "Blink lights to show that the program is progressing."
    global strip, led
    for s in strip:
        s.clear()
    for _ in range(n):
        for s in strip:
            s[0] = color
            s.show()
            led.value = True
        sleep(sleep_time)
        for s in strip:
            s.clear()
            s.show()
            led.value = False
        sleep(sleep_time)


if __name__ == "__main__": 
    blink(2, BLUE)
    with I2CTarget(scl=board.GP7, sda=board.GP6, addresses=[I2C_ADDRESS]) as i2c:
        blink(1, GREEN)
        main(i2c) 