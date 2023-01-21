import RPi.GPIO as GPIO

from datetime import datetime
import threading
import time

SUPPLY_FAN_PIN = 18
EXTRACT_FAN_PIN = 22


class Fans:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(SUPPLY_FAN_PIN, GPIO.OUT)
        GPIO.setup(EXTRACT_FAN_PIN, GPIO.OUT)

    def fan_on(self, fan_pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(fan_pin, GPIO.LOW)

    def fan_off(self, fan_pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(fan_pin, GPIO.HIGH)

    def supply_on(self):
        self.fan_on(SUPPLY_FAN_PIN)
    
    def supply_off(self):
        self.fan_off(SUPPLY_FAN_PIN)

    def extract_on(self):
        self.fan_on(EXTRACT_FAN_PIN)
    
    def extract_off(self):
        self.fan_off(EXTRACT_FAN_PIN)

    def control(self, supply, extract):
        if supply:
            self.supply_on()
        else:
            self.supply_off()
        # if extract:
        #     self.extract_on()
        # else:
        #     self.extract_off()

    def destroy(self):
        GPIO.cleanup()
