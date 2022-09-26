import machine
from time import sleep


class SHT40:
    # yellow -> SCL
    # Blue -> SDA

    ADDRESS=0x44

    # Commands
    MEASURE_HIGH = 0xFD
    MEASURE_MED = 0xF6
    MEASURE_LOW = 0xE0
    READ_SERIAL_NUM = 0x89
    SOFT_RESET=0x94

    def __init__(self,SCL = machine.Pin(9),SDA = machine.Pin(8)):
        self.i2c = machine.I2C(0, scl = SCL, sda = SDA)
        self.write_to_device(SHT40.SOFT_RESET)

    def write_to_device(self,cmd):
        print('Writing {cmd} to device'.format(cmd = cmd))
        self.i2c.writeto(SHT40.ADDRESS,bytes([cmd]))
        sleep(0.1)  

    def write_and_read(self,cmd,n_bytes=6):
        print('Writing {cmd} to device'.format(cmd = cmd))
        bytes_read = bytearray(n_bytes)
        self.i2c.writeto(SHT40.ADDRESS,bytes([cmd]))
        sleep(0.1)
        self.i2c.readfrom_into(SHT40.ADDRESS,bytes_read)
        sleep(0.1)
        print("".join("{:02x}".format(x) for x in bytes_read))
        return list(bytes_read)

    def get_measurements(self):
        """We get 6 bytes back, first two are MSB and LSB for temperaure,
            third is checksum, 4th and 5th are msb and lsb for humidity
        """
        raw_bytes = self.write_and_read(SHT40.MEASURE_HIGH)
        raw_temp = raw_bytes[0]*256 + raw_bytes[1]  
        raw_humid = raw_bytes[3]*256 + raw_bytes[4]
        
        temp = self.raw_to_centigrade(raw_temp)
        humid = self.raw_to_rumidity(raw_humid)
        
        print('Temperature: {temp}C, Humidity: {humid} %RH'.format(temp = temp, humid = humid))
        return temp,humid

    def raw_to_rumidity(self,raw):
        return - 6 + 125 * raw/(2**16 - 1)
        
    def raw_to_centigrade(self,raw):
        return -45 + 175 * raw/(2**16 -1)


if __name__ =='__main__':
    h=SHT40()
    led = machine.Pin("LED", machine.Pin.OUT)
    while True:
        led.value(True)
        print('Fetching Measurements')
        temp,humid = h.get_measurements()
        led.value(False)
        sleep(5)