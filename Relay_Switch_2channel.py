import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

ch1=18
ch2=25
n=0

gpio.setup(ch1,gpio.OUT)
gpio.setup(ch2,gpio.OUT)


gpio.output(ch1,gpio.HIGH)
gpio.output(ch2,gpio.HIGH)

try:
    i=0
    while(n<1):
        gpio.output(ch1,gpio.LOW)
        print "channel 1 ON"
        time.sleep(5)
        n=1

    while (n==1):
        gpio.output(ch1,gpio.HIGH)
        gpio.output(ch2,gpio.LOW)
        print "channel 2 ON"
        time.sleep(5)
        gpio.output(ch2,gpio.HIGH)
        n=2

    while (n==2):
        print "both off"
        time.sleep(2)
        n=3

    while(n==3):
        gpio.output(ch1,gpio.LOW)
        gpio.output(ch2,gpio.LOW)
        print "both on"
        time.sleep(5)
        n=4

    print "Program Complete"
    gpio.output(ch1,gpio.LOW)
    gpio.output(ch2,gpio.LOW)
    gpio.cleanup()

except KeyboardInterrupt:
    print "Quit"
    gpio.output(ch1,gpio.LOW)
    gpio.output(ch2,gpio.LOW)
    gpio.cleanup()
