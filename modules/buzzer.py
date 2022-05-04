import RPi.GPIO as GPIO
import time
import math


class Buzzer:
    def __init__(self):
        self.buzzer_pin = 13
        self.button_pin = 12

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.setup(
            self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP
        )  # Set buttonPin to INPUT mode, and pull up to HIGH level, 3.3V
        self.p = GPIO.PWM(self.buzzer_pin, 1)
        self.p.start(0)

        self.buzzer_active = False

    def loop(self):
        while True:
            if self.buzzer_active:
                self.alertor()
            elif not self.buzzer_active:
                self.stop_alertor()
                break

            if GPIO.input(self.button_pin) == GPIO.LOW:
                self.buzzer_active = False

    def alertor(self):
        self.p.start(50)
        for x in range(0, 361):
            sinVal = math.sin(x * (math.pi / 180.0))  # calculate the sine value
            toneVal = (
                2000 + sinVal * 500
            )  # Add to the resonant frequency with a Weighted
            self.p.ChangeFrequency(toneVal)  # Change Frequency of PWM to toneVal
            time.sleep(0.001)

    def stop_alertor(self):
        self.p.stop()

    def destroy(self):
        GPIO.output(self.buzzer_pin, GPIO.LOW)
        self.p.stop()
        GPIO.cleanup()
