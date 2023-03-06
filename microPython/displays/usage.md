Basic Usage
```
import machine
from ssd1306 import SSD1306_I2C

SCL = machine.Pin(9)
SDA = machine.Pin(8)
i2c_bus = machine.I2C(0, scl = SCL, sda = SDA)
oled = SSD1306_I2C(width=128,height=32,i2c=i2c_bus)


oled.fill(0)
oled.text('testing',0,1)
oled.show()
```