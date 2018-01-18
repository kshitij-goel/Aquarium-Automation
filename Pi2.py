import RPi.GPIO as gpio
import time
import datetime

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

ch1=23

flag1=0
flag2=0

apstart="07:00:00"
apstop="10:00:00"
shorttime="07:30:00"
current_time="00:00:00"
dayreset="23:59:59"

gpio.setup(ch1,gpio.OUT)

gpio.output(ch1, gpio.HIGH)

def ap_start():
    #starting water pump
    gpio.output(ch1, gpio.LOW)
    print "Air Pump Start"
    return;

def ap_stop():
    #stopping water pump
    gpio.output(ch1, gpio.HIGH)
    print "Air Pump Stop"
    return;

def time_convert( current_time ):
    current_time = datetime.datetime.strftime(datetime.datetime.now(),"%H:%M:%S")
    print "Current time converted"
    return current_time;

try:
    main=0
    while (main == 0):
        current_time=time_convert(current_time)
        if (current_time > apstart and current_time < apstop):
            if (flag1 == 0 and flag2 == 1):
                ap_stop()
                print "Pump stop after 08am"
                flag1=1
                flag2=0
        elif (current_time > apstop or current_time < apstart):
            if (flag2 == 0):
                ap_start()
                print "Pump start after 10am"
                flag1=0
                flag2=1
        print "Iteration wait for 5 secs"
        time.sleep(300)

except KeyboardInterrupt:
    gpio.output(ch1, gpio.low)
    gpio.cleanup()
