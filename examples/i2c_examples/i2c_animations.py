import digitalio
import board
from i2ctarget import I2CTarget
from pixelstrip import PixelStrip, current_time
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
    PixelStrip(board.GP4, 8, bpp=4, pixel_order="RGB", brightness=BRIGHTNESS),
    PixelStrip(board.GP5, 8, bpp=4, pixel_order="RGB", brightness=BRIGHTNESS)
]

# The built-in LED will turn on for half a second after every message
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

i2c = I2CTarget(scl=board.GP7, sda=board.GP6, addresses=[I2C_ADDRESS])

# Receive one byte through I2C, if available 
def receive_message():
    global i2c
    message = i2c.request()
    if message:
        b = message.read(n=1)[0]
        strip_num = int((b & 0xE0) >> 5)
        anim_num = int(b & 0x1F)
        return (strip_num, anim_num)
    else:
        return None

def main(): 
    global strip, led
    blink(3)
    last_msg_time = 0.0
    while True:
        for s in strip:
            s.draw()
        message = receive_message()
        if message:
            strip_num = message[0]
            anim_num = message[1]
            if strip_num < len(strip) and anim_num < len(animation):
                strip[strip_num].animation = animation[anim_num]
            elif strip_num < len(strip):
                strip[strip_num].animation = None
            last_msg_time = current_time()
        led.value = (current_time() < last_msg_time + 0.5)

def blink(n, color=BLUE, sleep_time=0.4): 
    """Blink lights to show that the program has loaded successfully"""
    global strip
    for s in strip:
        s.clear()
    for _ in range(n):
        for s in strip:
            s[0] = color
            s.show()
        sleep(sleep_time)
        for s in strip:
            s.clear()
            s.show()
        sleep(sleep_time)


if __name__ == "__main__":
    main()
