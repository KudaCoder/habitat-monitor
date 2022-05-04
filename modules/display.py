from plugins.PCF8574 import PCF8574_GPIO
from plugins.Adafruit_LCD1602 import Adafruit_CharLCD


class LCD:
    def __init__(self):
        self.PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        self.PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.

        try:
            self.mcp = PCF8574_GPIO(self.PCF8574_address)
        except Exception:
            try:
                self.mcp = PCF8574_GPIO(self.PCF8574A_address)
            except Exception:
                print('I2C Address Error !')
                exit(1)

        self.lcd = Adafruit_CharLCD(
            pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=self.mcp
        )

        self.lcd.begin(16, 2)  # Set number of LCD columns and lines        
        self.backlight(1)

    def backlight(self, status):
        self.mcp.output(3, status)

    def display(self, messages):
        self.lcd.setCursor(0, 0)
        for msg in messages:
            self.lcd.message(msg)

    def clear(self):
        self.lcd.clear()

    def destroy(self):
        self.backlight(0)
        self.clear()
