import RPi.GPIO as gpio
import time


def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)


def forward(sec):  # Turn motor forwards
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()


def reverse(sec):  # Turn motor reverse
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()


def motor_on():
    gpio.setmode(gpio.BCM)
    gpio.setup(21, gpio.OUT)
    gpio.output(21, gpio.HIGH)  # Turn relay motor on
    time.sleep(1)
    gpio.output(pin, gpio.LOW)  # Turn relay motor off
    time.sleep(1)



x = True
while x:
    textinput = input(str("left, right or fire"))
    if textinput == 'left':
        reverse(1)
    elif textinput == 'right':
        forward(1)
    elif textinput == 'fire':
        motor_on()
    else:
        print("error")
