#!/usr/bin/python
# -*- coding:utf-8 -*-



import logging
import time
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG)

servo_pin = 18

class bbh_servo:

    current_position = 0

    def __init__(self):
        servo_pin = 18

    def set_position(self, percentage):
        position = 28

        logging.debug(f'percentage = {percentage}')


        if percentage < -10:
            position = 22
        elif percentage < -5:
            position = 23
        elif percentage < -2.5:
            position = 24
        elif percentage < -1:
            position = 25
        elif percentage < -0.5:
            position = 26
        elif percentage < 0.5:
            position = 27
        elif percentage < 1:
            position = 28
        elif percentage < 2.5:
            position = 29
        elif percentage < 5:
            position = 30
        elif percentage < 10:
            position = 31
        else:
            position = 32


        logging.debug(f'position = {position}')


        if (position != self.current_position):


            # Setting the GPIO Mode to BOARD => Pin Count Mapping
            # GPIO.setmode(GPIO.BOARD)

            # Setting the GPIO Mode to BCM => GPIO Mapping
            # Uncomment below line for to use GPIO number
            GPIO.setmode(GPIO.BCM)

            # Setting the GPIO 18 as PWM Output
            GPIO.setup(servo_pin,GPIO.OUT)

            # Disable the warning from the GPIO Library
            GPIO.setwarnings(False)

            # Starting the PWM and setting the initial position of the servo with 50Hz frequency
            servo = GPIO.PWM(servo_pin,200)
            servo.start(0)

            servo.ChangeDutyCycle(position)
            time.sleep(1)

            servo.stop()
            GPIO.cleanup()

            self.current_position = position

        else:
            logging.debug(f'position not changed')
