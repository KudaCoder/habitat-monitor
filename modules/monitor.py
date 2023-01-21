#!/usr/bin/env python3
from utility.dataclass import Reading
from comm.redis import set_redis
from comm import api_tools

import plugins.Freenove_DHT as DHT
import RPi.GPIO as GPIO

# from habitat_tools import APITools
import time

DHTPin = 29
# api_tools = APITools()


class Monitor:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
                
    def monitor_temp_hum(self):
        self.dht = DHT.DHT(DHTPin)

        start_time = time.time()
        check_reading = None
        while True:
            for i in range(0, 15):
                chk = self.dht.readDHT11()
                if chk is self.dht.DHTLIB_OK:
                    break
                time.sleep(0.1)
            
            reading = Reading(
                temperature=self.dht.temperature,
                humidity=self.dht.humidity
            )
            # Sensor has not warmed up yet or is not receiving a reading
            if reading.temperature is None or reading.humidity is None:
                continue
            # Probably fried the GPIO on RPi and getting random 100+ deg C readings
            if check_reading is None:
                check_reading = reading
            if abs(reading.temperature - check_reading.temperature) > 1.5:
                continue
            else:
                set_redis("reading", reading)
                check_reading = reading

            # Save readings every 5 seconds
            end_time = time.time()
            delta = end_time - start_time
            if delta >= 5:
                api_tools.add_reading(
                    temperature=reading.temperature,
                    humidity=reading.humidity
                )
                start_time = time.time()
            
            time.sleep(1)
            
    def destroy(self):
        GPIO.cleanup()
