# from .buzzer import Buzzer
from .display import LCD

import threading
from datetime import datetime, time
from time import sleep

class Reminder:
    def __init__(self):
        self.lcd = LCD()
        # self.buzzer = Buzzer()

        self.water_reminder = None
        self.food_reminder = None

    def reset_reminder(self, category):
        if category == "food":
            self.food_reminder = None
        elif category == "water":
            self.water_reminder = None

    def show_reminder(self, message, category):
        self.lcd.clear()
        self.lcd.display([message])

        # self.buzzer.buzzer_active = True
        # buzzer_thread = threading.Thread(target=self.buzzer.loop, daemon=True)
        # buzzer_thread.start()

        # Approx 20 seconds of reminder
        for _ in range(0, 10):
            # if not self.buzzer.buzzer_active:
            #     break
            self.lcd.backlight(1)
            sleep(0.6)
            self.lcd.backlight(0)
            sleep(1.4)

        # If button was not pressed to stop reminder
        # if self.buzzer.buzzer_active:
        #     self.buzzer.buzzer_active = False

        self.lcd.clear()
        self.reset_reminder(category)

    def reminder(self, period):
        sleep(period)

        now = datetime.utcnow()
        now_time = now.time()
        day = now.weekday()
        if time(12, 00) <= now_time <= time(12, 30):
            # Reminder to water snake at 12pm each day
            self.water_reminder = True
        elif day == 6 and time(21, 00) <= now_time <= time(21, 30):
            # If Sunday past 9pm, reminder to feed snake
            self.food_reminder = True

        self.start_reminder()

    def start_reminder(self):
        # Check for reminders every 30 minutes
        period = 30 * 60
        thread = threading.Thread(target=self.reminder, args=(period,), daemon=True)
        thread.start()
    
    def destroy(self):
        # self.buzzer.destroy()
        pass


