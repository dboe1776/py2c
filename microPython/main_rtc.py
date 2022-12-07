"""
Same as main.py except script attempts to calibrate the Pico clock to real time using an API.
"""

import json
import urequests
import network
import time
import machine
# from sensors.SHT40 import SHT40
from sensors.TMP117 import TMP117

SSID = ''                         # Set SSID
PASSWORD = ''                     # Set password
TIMEOUT = 30
ID = machine.unique_id().hex()
hostname = 'localhost'            # Set hostname 

endpoint = 'http://{hostname}:5000/api/sensor-data'.format(hostname = hostname)


def wait_for_wifi(wlan,timeout):
    conn_start = time.time()

    while (time.time() - conn_start) < timeout:
        if wlan.isconnected() and wlan.status() >=3:
            print('Connection Succesful')
            break 
        else:
            print('Waiting for Connection')
            time.sleep(2)
    return wlan.isconnected()

def establish_connection(wlan):
    wifi_status = False
    time_status = False

    while (not wifi_status) and (not time_status):
        wifi_status = wait_for_wifi(wlan,TIMEOUT)
        time.sleep(1)
        time_status = calibrate_time()
        if wifi_status and time_status:
            break
        else:
            # wait for a bit and then try again.
            time.sleep(60)

def calibrate_time():
    print('Attempting to calibrate time')
    try:
        response = urequests.get("http://worldtimeapi.org/api/ip")
        date = response.json()['utc_datetime'].split('T')[0].split('-')
        date = [int(x) for x in date]
        date.append(0)
        time_ = response.json()['utc_datetime'].split('T')[-1].split('.')[0]
        time_ = time_.split(':')
        time_ = [int(x) for x in time_]
        time_.append(0)
        overall = tuple(date + time_)
        print('Setting Time to {timetuple}'.format(timetuple = overall))
        machine.RTC().datetime(overall)
        print('Time calibrated')
        return True
    except Exception as ex:
        print('Time calibration failed')
        return False
    
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
    if not wlan.isconnected():
        wait_for_wifi()
    data = sensor.get_measurements()
    data = {'host':ID,'tmeas':time.time(),'sensor_data':data}
    packet = json.dumps(data)
    print(packet)
    try:
        r = urequests.post(endpoint,json = packet)
    except Exception as ex:
        print('Data Post Failed',ex)
    try:
        if r.status_code == 200:
            print('Data post successful')
        r.close()
    except Exception as ex:
        print('No response object')
    
    time.sleep(300)

