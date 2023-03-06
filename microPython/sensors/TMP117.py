import machine
from time import sleep

def convert_twos_complement(raw_bytes,nbits = 16):
    bits = bin(int(bytearray(raw_bytes).hex(),nbits))[2:]
    
    # Sadly no zfill in micro-python
    bits = '0'*(nbits - len(bits)) + bits
    msb = int(bits[0])
    value = int(bits[1:],2) - msb*2**15
    return value

class TMP117:
    # yellow -> SCL
    # Blue -> SDA

    # Commands
    
    TEMP_REGISTER = 0x00
    CONFIG_REGISTER = 0x01
    DEVICE_ID_REGISTER = 0x0F 
    
    TEMP_RESET = 0x8000
    SOFT_RESET = 0x0002

    def __init__(self,i2c,address = 0x48):
        self.ADDRESS=address
        self.i2c = i2c

    def write_to_register(self,reg,cmd):
        print('Writing {cmd} to device on register {reg}'.format(cmd = cmd,reg = reg))
        self.i2c.writeto_mem(self.ADDRESS,reg,bytes([cmd]))
        sleep(0.1)  

    def read_from_register(self,reg,n_bytes = 2):
        print('Reading from register {reg}'.format(reg = reg))
        bytes_read = bytearray(n_bytes)
        self.i2c.readfrom_mem_into(self.ADDRESS,reg,bytes_read)
        sleep(0.1)  
        return bytes_read

    def get_measurements(self):
        """
        We get 2 bytes (16 bits) back, represents two's complement of temperature 
        """
        raw_bytes = self.read_from_register(TMP117.TEMP_REGISTER,n_bytes=2)
        raw_temp = convert_twos_complement(raw_bytes)
        temp = self.raw_to_centigrade(raw_temp)
        print('Temperature: {temp}C'.format(temp = temp))
        return dict(temp = temp)
        
    def raw_to_centigrade(self,raw):
        return raw*7.8125e-3
        

if __name__ =='__main__':
    SCL = machine.Pin(9)
    SDA = machine.Pin(8)
    i2c_bus = machine.I2C(0, scl = SCL, sda = SDA) 
    sensor=TMP117(i2c_bus)
    led = machine.Pin("LED", machine.Pin.OUT)
    while True:
        led.value(True)
        print('Fetching Measurements')
        data = sensor.get_measurements()
        led.value(False)
        sleep(10)