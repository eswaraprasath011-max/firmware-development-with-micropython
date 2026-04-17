import utime
from machine import I2C

# LCD I2C Driver for PCF8574 backpack (address 0x27)
LCD_CHR = 1  # character mode
LCD_CMD = 0  # command mode

LCD_BACKLIGHT    = 0x08
LCD_NOBACKLIGHT  = 0x00
ENABLE           = 0b00000100

class LCD:
    def __init__(self, i2c, address=0x27, cols=16, rows=2):
        self.i2c      = i2c
        self.addr     = address
        self.cols     = cols
        self.rows     = rows
        self.backlight = LCD_BACKLIGHT
        self._init_lcd()

    def _write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data]))

    def _pulse_enable(self, data):
        self._write_byte(data | ENABLE)
        utime.sleep_us(500)
        self._write_byte(data & ~ENABLE)
        utime.sleep_us(100)

    def _write4bits(self, data):
        self._write_byte(data | self.backlight)
        self._pulse_enable(data | self.backlight)

    def send(self, value, mode):
        high = value & 0xF0
        low  = (value << 4) & 0xF0
        self._write4bits(high | mode)
        self._write4bits(low  | mode)

    def command(self, cmd):
        self.send(cmd, LCD_CMD)

    def write_char(self, ch):
        self.send(ord(ch), LCD_CHR)

    def _init_lcd(self):
        utime.sleep_ms(50)
        self._write4bits(0x30)
        utime.sleep_ms(5)
        self._write4bits(0x30)
        utime.sleep_us(150)
        self._write4bits(0x30)
        self._write4bits(0x20)          # switch to 4-bit mode

        self.command(0x28)              # 2-line, 5x8 font
        self.command(0x0C)              # display ON, cursor OFF
        self.command(0x06)              # auto-increment cursor
        self.clear()

    def clear(self):
        self.command(0x01)
        utime.sleep_ms(2)

    def set_cursor(self, col, row):
        row_offsets = [0x00, 0x40]
        self.command(0x80 | (col + row_offsets[row]))

    def print(self, text):
        for ch in text:
            self.write_char(ch)

    def backlight_on(self):
        self.backlight = LCD_BACKLIGHT
        self._write_byte(self.backlight)

    def backlight_off(self):
        self.backlight = LCD_NOBACKLIGHT
        self._write_byte(self.backlight)
