from time import sleep
import digitalio
import board
from pixelstrip import current_time
from i2ctarget import I2CTarget


I2C_ADDRESS = 0x41

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

i2c = I2CTarget(scl=board.GP7, sda=board.GP6, addresses=[I2C_ADDRESS])

def receive_message():
    global i2c
    i2c_request = i2c.request()
    if not i2c_request:
        return None
    return i2c_request.read()

last_msg_time = 0.0
while True:
    message = receive_message()
    if message:
        print(message)
        last_msg_time = current_time()
    led.value = (current_time() < last_msg_time + 0.5)
    sleep(0.1)