import RPi.GPIO as GPIO

from comm.redis import get_redis

from datetime import datetime
import threading
import time

SUPPLY_FAN_PIN = 16
EXTRACT_FAN_PIN = 18


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

    def control(self):
        return_to_high = False
        first = False
        
        extract = False
        supply = False

        c_time = time.time()
        # TODO: not a fan of redis returning None. Need method to ensure
        # key is either present or can wait for key to be created by relevant module
        while True:
            c_end_time = time.time()
            delta = c_end_time - c_time
            if delta >= 5 or not first:
                config = get_redis("environment")
                if config is None:
                    continue    
                c_time = time.time()
                first = True

            reading = get_redis("reading")
            if reading is None:
                continue
            temp = reading.temp
            hum = reading.hum

            # lights = get_redis("light")
            # if lights is None:
            #     continue

            # now = datetime.now()
            # n_time = now.time()
            
            # override = False
            # # Night time

            # TODO: Make this work with temperatures as well as humidity!            
            if hum >= config.humidity_l_sp and not return_to_high:
                extract = True
            elif hum < config.humidity_l_sp:
                extract = False
                supply = False
                return_to_high = True
            elif hum >= (config.humidity_l_sp + 3.0):
                extract = True
                return_to_high = False
            if hum >= config.humidity_h_sp:
                supply = True

            if supply: 
                self.fan_on(SUPPLY_FAN_PIN)
            else:
                self.fan_off(SUPPLY_FAN_PIN)
            if extract:
                self.fan_on(EXTRACT_FAN_PIN)
            else:
                self.fan_off(EXTRACT_FAN_PIN)

    def destroy(self):
        GPIO.cleanup()

    def start_fans(self):
        thread = threading.Thread(target=self.control, daemon=True)
        thread.start()
