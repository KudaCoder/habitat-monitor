#!/usr/bin/env python3
from comm.redis import update_redis
from utility.dataclass import Reading
from comm import api_tools

import plugins.Freenove_DHT as DHT
import RPi.GPIO as GPIO

import time

DHTPin = 15


class Monitor:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
                
    def monitor_temp_hum(self):
        self.dht = DHT.DHT(DHTPin)

        start_time = time.time()
        while True:
            for i in range(0, 15):
                chk = self.dht.readDHT11()
                if chk is self.dht.DHTLIB_OK:
                    break
                time.sleep(0.1)
            
            temp = self.dht.temperature
            hum = self.dht.humidity

            update_redis("reading", {
                "temp": temp, 
                "hum": hum,
            })

            # Save readings every 5 seconds
            end_time = time.time()
            delta = end_time - start_time
            if delta >= 5:
                try:
                    resp = api_tools.add_reading(temp=temp, hum=hum)
                except Exception:
                    pass
                start_time = time.time()
            
    def destroy(self):
        GPIO.cleanup()
