import digitalio
from i2cp import i2cSlave
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
    pixelstrip.PixelStrip(
        board.D12, 8, bpp=4, pixel_order=pixelstrip.RGBW, brightness=BRIGHTNESS
    ),
    pixelstrip.PixelStrip(
        board.D11, 8, bpp=4, pixel_order=pixelstrip.RGBW, brightness=BRIGHTNESS
    )
]

# The built-in LED will turn on for half a second after every message
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

i2c_slave = i2cSlave(0,sda=16,scl=17,slave_address=I2C_ADDRESS)

def receive_message():
    global i2c_slave
    if i2c_slave.any():
        b = i2c_slave.get()
        strip_num = int((b & 0xF0) >> 4)
        anim_num = int(b & 0x0F)
        return (strip_num, anim_num)
    else:
        return None

def main():
    global strip, led
    for s in strip:
        s.clear()
    last_msg_time = 0.0
    while True:
        for s in strip:
            s.draw()
        message = receive_message()
        if message:
            strip_num = message[0]
            anim_num = message[1]
            strip[strip_num].animation = animation[anim_num]
            last_msg_time = current_time()
        led.value = (current_time() < last_msg_time + 0.5)

main()
