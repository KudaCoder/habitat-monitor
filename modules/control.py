from comm.redis import get_redis

from datetime import datetime
import threading
import time


class Control:
    def __init__(self, lights, fans):
        self.lights = lights
        if self.lights is None:
            raise ValueError("Lights module must be provided!")
        self.fans = fans
        if self.fans is None:
            raise ValueError("Fans module must be provided!")
        
        self.return_to_high = False
        self.return_to_cool = False
        self.small_light = False
        self.big_light = False
        self.extract = False
        self.supply = False

    def run(self):
        first = True
        c_time = time.time()

        while True:
            c_end_time = time.time()
            delta = c_end_time - c_time
            if delta >= 5 or first:
                config = get_redis("environment")
                c_time = time.time()
                first = False

            # TODO: Don't like this
            reading = get_redis("reading")
            if reading is None:
                continue
            temp = reading.temperature
            hum = reading.humidity
            if temp is None or hum is None:
                continue

            n_time = datetime.now().time()
            # Day time
            if config.lights_on_time <= n_time <= config.lights_off_time:
                cycle = "day"
                self.h_sp = config.day_h_sp
                self.l_sp = config.day_l_sp

                self.lights.control("night", False, False)
                self.day_config(temp)
            # Night time
            else:
                cycle = "night"
                self.h_sp = config.night_h_sp
                self.l_sp = config.night_l_sp

                self.lights.control("day", False, False)
                self.night_config(temp)
            
            if hum < config.humidity_l_sp:
                self.extract = False
                self.supply = False
            if hum >= (config.humidity_l_sp + 3.0):
                self.extract = True
            if hum >= config.humidity_h_sp:
                self.supply = True
            
            self.lights.control(cycle, self.big_light, self.small_light)
            self.fans.control(self.supply, self.extract)

    # This if/else fiasco is necessary until I get an
    # external temp sensor to compare to the internal
    def night_config(self, temp):
        if temp > (self.h_sp + 1.0):
            self.return_to_cool = True
            self.small_light = False
            self.big_light = False
        elif temp > self.h_sp and not self.return_to_cool:
            self.return_to_cool = True
            self.small_light = True
            self.big_light = False
        elif ((self.h_sp - 1.0) <= temp < self.h_sp) and not self.return_to_cool:
            self.small_light = False
        elif (self.l_sp <= temp <= self.h_sp) and not self.return_to_cool:
            self.big_light = True
        elif temp < self.l_sp:
            self.big_light = True
            self.small_light = True
            self.return_to_cool = False

    def day_config(self, temp):
        if temp < (self.l_sp - 1.0):
            self.small_light = True
            self.big_light = True
            self.return_to_heat = False
        elif temp < self.l_sp and not self.return_to_heat:
            self.small_light = True
            self.big_light = False
            self.return_to_heat = True
        elif temp >= self.l_sp:
            self.small_light = True
            self.big_light = False
            self.return_to_heat = True
        elif temp > self.h_sp:
            self.big_light = False
            self.small_light = False
            self.return_to_cool = True
