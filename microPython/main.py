"""
Main script for measuring and transmiting data from a sensor.

SAMPLE .json sent by this program:
    {'sensor_data': {'temp': 19.59375}, 'host': 'e6614864d32c8c36'}
    {'sensor_data': {'temp': 13.48471,'humidity':46.39872}, 'host': 'e6614864d32d8a41'},
"""

import json
import urequests
import network
import time
import machine
import config
# from sensors.SHT40 import SHT40
from sensors.TMP117 import TMP117


SSID = config.SSID                   # Set SSID
PASSWORD = config.PASSWORD           # Set password
TIMEOUT = 30
ID = machine.unique_id().hex()
HOSTNAME = config.HOSTNAME 
PORT=config.PORT
endpoint = config.ENDPOINT
led = machine.Pin("LED", machine.Pin.OUT)
led.off()

def wait_for_wifi(wlan,timeout):
    conn_start = time.time()

    while (time.time() - conn_start) < timeout:
        led.toggle()
        if wlan.isconnected() and wlan.status() >=3:
            print('Connection Successful')
            break 
        else:
            print('Waiting for Connection')
            time.sleep(1)
    led.off()
    return wlan.isconnected()

def establish_connection(wlan,max_tries = 2):
    led.off()
    tries = 0
    while (not wait_for_wifi(wlan,TIMEOUT)):
        tries+=1
        if tries < max_tries:
            time.sleep(30)
        else:
            print('Unable to connect after {n} tries... resetting'.format(n=tries))
            machine.reset()
    
    led.on()
#####################################
## Program
#####################################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

# stay here till we have a connection
establish_connection(wlan)

SCL = machine.Pin(9)
SDA = machine.Pin(8)
i2c_bus = machine.I2C(0, scl = SCL, sda = SDA) 
# sensor = SHT40.SHT40(i2c_bus)
sensor  = TMP117(i2c_bus)

while True:
    if wlan.status() <3:
        establish_connection()
    data = sensor.get_measurements()
    data = {'host':ID,'sensor_data':data}
    packet = json.dumps(data)
    print(packet)
    failed = False
    try:
        r = urequests.post(endpoint,json = packet)
    except Exception as ex:
        print('Data Post Failed',ex)
        failed = True
    try:
        if (r.status_code == 200) and not failed:
            print('Data post successful')
        r.close()
    except Exception as ex:
        print('No response object')

    time.sleep(config.DELAY)