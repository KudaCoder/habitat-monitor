#!/usr/bin/env python3
from modules.reminder import Reminder
from modules.control import Control
from modules.monitor import Monitor
from modules.buzzer import Buzzer
from modules.lights import Lights
from modules.display import LCD
from modules.fans import Fans

from comm.redis import get_redis, show_redis

from datetime import datetime, time
from multiprocessing import Process
from time import sleep
import requests


class HabitatMonitor:
    def __init__(self, lcd, reminder):
        self.lcd = lcd
        self.reminder = reminder
        self.reminder.start_reminder()

    def display(self):
        deg_symbol = chr(223)

        while True:
            reading = get_redis("reading")
            if reading is None:
                continue
                
            line_1 = f"    Temp: {reading.temperature}{deg_symbol}C" + "\n"
            line_2 = f"Humidity: {reading.humidity}% RH"
            self.lcd.display((line_1, line_2))

            if self.reminder.food_reminder is not None:
                self.reminder.show_reminder("FEED THE SNAKE!!", "food")
            elif self.reminder.water_reminder is not None:
                self.reminder.show_reminder("WATER THE SNAKE!!", "water")

    def destroy(self):
        self.lcd.destroy()

def run():
    print('Program is starting ... \n')

    print("Warming up containers...\n")
    test_connections()

    sub_processes = []
    monitor = Monitor()
    lights = Lights()
    fans = Fans()
    control = Control(lights, fans)
    sub_processes.append(Process(target=monitor.monitor_temp_hum))
    sub_processes.append(Process(target=control.run))
    for p in sub_processes:
        p.start()

    lcd = LCD()
    reminder = Reminder()
    habitat = HabitatMonitor(lcd, reminder)
    try:
        print("Habitat running...")
        habitat.display()
    except KeyboardInterrupt:
        print("killing all processes...")
        for p in sub_processes:
            p.terminate()

        monitor.destroy()
        lights.destroy()
        fans.destroy()        
        habitat.destroy()

        print("Exiting...Goodbye!")


def test_connections():
    interval = 5
    retries = 2

    for _ in range(retries):
        try:
            test_config = get_redis("environment")
            assert hasattr(test_config, "lights_on_time")
            resp = requests.get("http://habitat-api/api/config")
            resp.raise_for_status()
            print("Success!!...\n")
            break
        except Exception:
            sleep(interval)


if __name__ == '__main__':
    run()
