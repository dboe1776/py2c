import busio
import board
import digitalio
from adafruit_bus_device.i2c_device import I2CDevice
from time import sleep

# https://docs.circuitpython.org/projects/busdevice/en/latest/examples.html

SDA=board.GP16
SCL=board.GP17

# Setup the LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False

class SHT420:
    # Datasheet https://cdn-learn.adafruit.com/assets/assets/000/099/223/original/Sensirion_Humidity_Sensors_SHT4x_Datasheet.pdf?1612388531

    ADDRESS=0x44

    # Commands
    MEASURE_HIGH = 0xFD
    MEASURE_MED = 0xF6
    MEASURE_LOW = 0xE0
    READ_SERIAL_NUM = 0x89
    SOFT_RESET=0x94


    def __init__(self):
        self.bus = busio.I2C(SCL, SDA)
        self.write_to_device(SHT420.SOFT_RESET)

    def get_measurements(self):
        """We get 6 bytes back, first two are MSB and LSB for temperaure,
            third is checksum, 4th and 5th are msb and lsb for humidity
        """
        raw_bytes = self.write_and_read(SHT420.MEASURE_HIGH)
        raw_temp = raw_bytes[0]*256 + raw_bytes[1]  
        raw_humid = raw_bytes[3]*256 + raw_bytes[4]
        
        temp = self.raw_to_centigrade(raw_temp)
        humid = self.raw_to_rumidity(raw_humid)
        return temp,humid

    def write_to_device(self,cmd):
        print(f'Writing {cmd} to device')
        # with busio.I2C(SCL, SDA) as bus:
        with I2CDevice(self.bus, SHT420.ADDRESS) as device:
                device.write(bytes([cmd]))
        sleep(0.1)  

    def write_and_read(self,cmd,n_bytes=6):
        bytes_read = bytearray(n_bytes)
        # with busio.I2C(SCL, SDA) as bus:
        # device = I2CDevice(self.bus, HTU21DF.ADDRESS)
        with I2CDevice(self.bus, SHT420.ADDRESS) as device:
            device.write(bytes([cmd]))
            sleep(0.1)
            device.readinto(bytes_read)
            sleep(0.1)
        # print("".join("{:02x}".format(x) for x in bytes_read))
        return list(bytes_read)

    def raw_to_rumidity(self,raw):
        return - 6 + 125 * raw/(2**16 - 1)
        
    def raw_to_centigrade(self,raw):
        return -45 + 175 * raw/(2**16 -1)


h=SHT420()
while True:
    led.value = True
    print('Fetching Measurements')
    temp,humid = h.get_measurements()
    print(f'Temperature: {temp}C, Humidity: {humid} %RH')
    led.value = False
    sleep(5)


