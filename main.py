#!/usr/bin/env python3
from modules.reminder import Reminder
from modules.monitor import Monitor
from modules.buzzer import Buzzer
from modules.display import LCD
from modules.lights import Lights
from modules.fans import Fans

from comm.redis import get_redis
from datetime import datetime, time
from multiprocessing import Process


class HabitatMonitor:
    def __init__(self):
        self.lcd = LCD()
        self.reminder = Reminder()
        self.reminder.start_reminder()

    def display(self):
        deg_symbol = chr(223)

        while True:
            reading = get_redis("reading")
            line_1 = f"Temp: {reading.temp} {deg_symbol}C" + "\n"
            line_2 = f"Humidity: {reading.hum}% RH"
            self.lcd.display((line_1, line_2))

            if self.reminder.food_reminder is not None:
                self.reminder.show_reminder("FEED THE SNAKE!!", "food")
            elif self.reminder.water_reminder is not None:
                self.reminder.show_reminder("WATER THE SNAKE!!", "water")

    def destroy(self):
        self.lcd.destroy()

def run():
    print('Program is starting ... ')

    sub_processes = []

    monitor = Monitor()
    lights = Lights()
    fans = Fans()
    sub_processes.append(Process(target=monitor.monitor_temp_hum))
    sub_processes.append(Process(target=lights.control))
    sub_processes.append(Process(target=fans.control))
    for p in sub_processes:
        p.start()

    habitat = HabitatMonitor()
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


if __name__ == '__main__':

    

    run()
