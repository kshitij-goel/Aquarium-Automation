import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

ch1=18
n=0

gpio.setup(ch1,gpio.OUT)


gpio.output(ch1,gpio.HIGH)

try:
    while(n<1):
        gpio.output(ch1,gpio.LOW)
        print "channel 1 ON"
        time.sleep(5)
        n=1
    gpio.output(ch1,gpio.HIGH)
    print"channel 1 off)
    time.sleep(5)

    print "Program Complete"
    gpio.output(ch1,gpio.LOW)
    gpio.cleanup()

except KeyboardInterrupt:
    print "Quit"
    gpio.output(ch1,gpio.LOW)
    gpio.cleanup()
