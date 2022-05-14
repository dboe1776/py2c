import smbus2 as smbus
import time

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

    def __init__(self,bus_n=1):
        self.bus=smbus.SMBus(bus_n)
        time.sleep(0.2)
        self.bus.write_byte(HTU21DF.ADDRESS,HTU21DF.SOFT_RESET)
        time.sleep(1)

    def read_temperature(self):
        print('\nReading Temperature')
        write=smbus.i2c_msg.write(HTU21DF.ADDRESS,[HTU21DF.HOLD_TEMPERATURE])
        read=smbus.i2c_msg.read(HTU21DF.ADDRESS,3)
        try:
            self.bus.i2c_rdwr(write)
            time.sleep(0.1)
            self.bus.i2c_rdwr(read)
            raw_bytes=list(read)
            msb=raw_bytes[0]
            lsb=raw_bytes[1]
            print(f'Temperature Read - MSB: {msb}, LSB: {lsb}')
            raw_value= msb*256 + lsb
            return (raw_value * 175.72 / 65536.0) - 46.85
        except Exception as ex:
            print(ex)
            return None        

    def read_humidity(self):
        print('\nReading Humidity')
        write=smbus.i2c_msg.write(HTU21DF.ADDRESS,[HTU21DF.HOLD_HUMIDITY])
        read=smbus.i2c_msg.read(HTU21DF.ADDRESS,3)
        try:
            self.bus.i2c_rdwr(write)
            time.sleep(0.1)
            self.bus.i2c_rdwr(read)
            raw_bytes=list(read)
            msb=raw_bytes[0]
            lsb=raw_bytes[1]
            print(f'Humidy Read - MSB: {msb}, LSB: {lsb}')
            raw_value= msb*256 + lsb
            return (raw_value * 125.0 / 65536.0) - 6.0
        except Exception as ex:
            print(ex)
            return None

    def reset(self):
        print('RESET')
        try:
            self.bus.write_byte(HTU21DF.ADDRESS,HTU21DF.SOFT_RESET)
        except Exception as ex:
            print(ex)
            return None

if __name__== '__main__':
    print('Creating Sensor Object')
    H=HTU21DF()
    print(H.__class__.__name__)
    try:
        while True:
            temp=H.read_temperature()
            hum=H.read_humidity()
            print(f'Temperature: {temp} C, Relative Humidity: {hum} %')
            time.sleep(5)
    except KeyboardInterrupt:
        print('Keyboard Interrupt - Shutting Down')