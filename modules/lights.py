from comm.redis import get_redis

import RPi.GPIO as GPIO

from datetime import datetime
import threading
import time

DAY_BIG_PIN = 7
DAY_SMALL_PIN = 16
NIGHT_SMALL_PIN = 11
NIGHT_BIG_PIN = 12


class Lights:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(DAY_BIG_PIN, GPIO.OUT)
        GPIO.setup(DAY_SMALL_PIN, GPIO.OUT)
        GPIO.setup(NIGHT_BIG_PIN, GPIO.OUT)
        GPIO.setup(NIGHT_SMALL_PIN, GPIO.OUT)
            
    def night_big_heat_on(self):
        GPIO.output(NIGHT_BIG_PIN, GPIO.LOW)
    
    def night_big_heat_off(self):
        GPIO.output(NIGHT_BIG_PIN, GPIO.HIGH)

    def night_small_heat_on(self):
        GPIO.output(NIGHT_SMALL_PIN, GPIO.LOW)
    
    def night_small_heat_off(self):
        GPIO.output(NIGHT_SMALL_PIN, GPIO.HIGH)

    def day_big_light_on(self):
        GPIO.output(DAY_BIG_PIN, GPIO.LOW)
    
    def day_big_light_off(self):
        GPIO.output(DAY_BIG_PIN, GPIO.HIGH)

    def day_small_light_on(self):
        GPIO.output(DAY_SMALL_PIN, GPIO.LOW)
    
    def day_small_light_off(self):
        GPIO.output(DAY_SMALL_PIN, GPIO.HIGH)

    def all_lights_off(self):
        self.night_big_heat_off()
        self.night_small_heat_off()
        self.day_big_light_off()
        self.day_small_light_off()

    def control(self, cycle, big, small):
        controller = {
            "day": {
                "big": {
                    True: self.day_big_light_on,
                    False: self.day_big_light_off
                },
                "small": {
                    True: self.day_small_light_on,
                    False: self.day_small_light_off
                }
            },
            "night": {
                "big": {
                    True: self.night_big_heat_on,
                    False: self.night_big_heat_off
                },
                "small": {
                    True: self.night_small_heat_on,
                    False: self.night_small_heat_off
                }
            },
        }

        controller[cycle]["big"][big]()
        controller[cycle]["small"][small]()

    def destroy(self):
        GPIO.cleanup()
