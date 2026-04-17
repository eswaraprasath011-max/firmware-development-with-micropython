from machine import I2C, Pin
from lcd_i2c import LCD
import utime

# I2C setup — GP0 = SDA, GP1 = SCL (I2C0)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)

# Scan to confirm LCD is found
devices = i2c.scan()
print("I2C devices found:", [hex(d) for d in devices])

# Init LCD
lcd = LCD(i2c, address=0x27, cols=16, rows=2)

# --- Example Usage ---

# Line 1
lcd.set_cursor(0, 0)
lcd.print("  Hello, Pico!")

# Line 2
lcd.set_cursor(0, 1)
lcd.print("  I2C LCD 16x2")

utime.sleep(99)

# Scrolling counter example
lcd.clear()
