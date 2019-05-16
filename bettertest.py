import RPi.GPIO as gpio
import time


def init():  # creates a callable gpio set up for motor with wheel
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)


def forward(sec):  # orders gpio pins to create forwards motion
    init()  # calls gpio set up
    gpio.output(17, True)  # turns on True gpio
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()  # resets the gpio pins


def reverse(sec):  # orders gpio pins to create backwards motion
    init()  # calls gpio set up
    gpio.output(17, False)  # turns on True gpio
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()  # resets the gpio pins


def motor_on():
    gpio.setmode(gpio.BCM)
    gpio.setup(21, gpio.OUT)  # calls gpio pin
    gpio.output(21, gpio.HIGH)  # Turn relay motor on
    time.sleep(1)  # waits so it runs smoothly
    gpio.output(21, gpio.LOW)  # Turn relay motor off
    time.sleep(3)  # waits three second while it runs
    gpio.cleanup()  # resets the gpio pins to turn it off


while True:  # runs forever
    textinput = input(str("left, right or fire"))  # takes your input
    if textinput == 'left':
        reverse(1)  # runs motor reverse for 1 second
    elif textinput == 'right':
        forward(1)  # runs motor forward for 1 second
    elif textinput == 'fire':
        motor_on()  # runs the motor controlled by a relay
    else:
        print("error")  # defencive coding
