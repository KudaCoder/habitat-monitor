from comm.redis import get_redis, update_redis

import RPi.GPIO as GPIO

from datetime import datetime
import threading
import time

NIGHT_LIGHT_PIN = 11


class Lights:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(NIGHT_LIGHT_PIN, GPIO.OUT)
            
    def night_light_on(self):
        GPIO.output(NIGHT_LIGHT_PIN, GPIO.LOW)
    
    def night_light_off(self):
        GPIO.output(NIGHT_LIGHT_PIN, GPIO.HIGH)
    
    def control(self):
        return_to_cool = False

        c_time = time.time()
        first = True
        while True:
            c_end_time = time.time()
            delta = c_end_time - c_time
            if delta >= 5 or first:
                config = get_redis("environment")            
                c_time = time.time()
                first = False
            reading = get_redis("reading")
            temp = reading.temp

            now = datetime.now()
            n_time = now.time()
            
            heat_on = False
            # Night time
            if (config.lights_off_time < n_time) or (n_time < config.lights_on_time):
                if temp > config.night_h_sp:
                    return_to_cool = True
                elif (config.night_l_sp <= temp <= config.night_h_sp) and not return_to_cool:
                    heat_on = True
                elif temp < config.night_l_sp:
                    heat_on = True
                    return_to_cool = False
            # Day time
            # elif config.lights_on_time <= n_time <= config.lights_off_time:
            #     if temp > config.day_h_sp:
            #         return_to_cool = True
            #     elif (config.day_l_sp <= temp <= config.day_h_sp) and not return_to_cool:
            #         heat_on = True
            #     elif temp < config.day_l_sp:
            #         heat_on = True
            #         return_to_cool = False

            if heat_on:
                self.night_light_on()
                update_redis("light", {"turned_on": True})
            else:
                self.night_light_off()
                update_redis("light", {"turned_on": False})
            
    def destroy(self):
        GPIO.cleanup()
