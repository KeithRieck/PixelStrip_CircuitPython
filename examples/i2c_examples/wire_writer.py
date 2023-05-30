from time import sleep
import digitalio
import board
from pixelstrip import current_time
import busio
from circuitpython_typing import ReadableBuffer


I2C_ADDRESS = 0x41

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(scl=board.GP7, sda=board.GP6)

def write_message(address, message):
    global i2c
    i2c.writeto(address, bytes(message))

x = 0
timeout = current_time() + 1.0
last_msg_time = 0.0
while True:
    if current_time() >= timeout:
        message = "x is {}".format(x)
        write_message(I2C_ADDRESS, message)
        x = x + 1
        timeout = current_time() + 3.0
        last_msg_time = current_time()
    led.value = (current_time() < last_msg_time + 0.5)
    sleep(0.1)
