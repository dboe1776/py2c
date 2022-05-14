import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice
from time import sleep

# https://docs.circuitpython.org/projects/busdevice/en/latest/examples.html

SDA=board.GP4
SCL=board.GP5


class HTU21DF:


    ADDRESS=0x40

    # Commands
    HOLD_HUMIDITY=0xE5
    HOLD_TEMPERATURE=0xE3
    NOHOLD_HUMIDITY=0xF5
    NOHOLD_TEMPERATURE=0xF3
    WRITE_USR_REGISTER=0xE6
    READ_USR_REGISTER=0xE7
    SOFT_RESET=0xFE

    def __init__(self):
        self.bus = busio.I2C(SCL, SDA)
        self.write_to_device(HTU21DF.SOFT_RESET)

    def read_temprature(self):
        self.write_and_read(HTU21DF.HOLD_TEMPERATURE)

    def read_humidity(self):
        self.write_and_read(HTU21DF.HOLD_HUMIDITY)

    def write_to_device(self,cmd):
        print(f'Writing {cmd} to device')
        # with busio.I2C(SCL, SDA) as bus:
        with I2CDevice(self.bus, HTU21DF.ADDRESS) as device:
                device.write(bytes([cmd]))
        sleep(0.1)

    def write_and_read(self,cmd,n_read=3):
        bytes_read = bytearray(n_read)
        # with busio.I2C(SCL, SDA) as bus:
        # device = I2CDevice(self.bus, HTU21DF.ADDRESS)
        with I2CDevice(self.bus, HTU21DF.ADDRESS) as device:
            device.write(bytes([cmd]))
            sleep(0.1)
            device.readinto(bytes_read)
            sleep(0.1)
        print("".join("{:02x}".format(x) for x in bytes_read))




h=HTU21DF()
while True:
    print('Attempting to communicate')
    h.read_humidity()
    sleep(0.1)
    h.read_temprature()
    print('done')
    sleep(5)


# """Example for Pico. Turns on the built-in LED."""
# import board
# import digitalio
# import time

# led = digitalio.DigitalInOut(board.LED)
# led.direction = digitalio.Direction.OUTPUT

# led_ext = digitalio.DigitalInOut(board.GP16)
# led_ext.direction = digitalio.Direction.OUTPUT

# led.value = True
# led_ext.value = False
# while True:
#     time.sleep(1)
#     led.value = not (led.value)
#     led_ext.value = not (led_ext.value)
