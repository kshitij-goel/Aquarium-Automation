#Program to automise the fish tank functionality
#Created by: Kshitij Goel
#Dated: 6 May 2017

import RPi.GPIO as gpio
import time
import datetime

gpio.cleanup()

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

ch1=18
ch2=25
trig=23
echo=24

flag1=0
flag2=0
flag3=0
flag4=0

wpstart="10:00:00"
wpstop="22:00:00"
waterinletstart="07:00:00"
shorttime="06:45:00"
dayreset="23:59:59"

gpio.setup(ch1,gpio.OUT)
gpio.setup(ch2,gpio.OUT)
gpio.setup(trig,gpio.OUT)
gpio.setup(echo,gpio.IN)

gpio.output(ch1, gpio.HIGH)
gpio.output(ch2, gpio.HIGH)

def dist_measure():
    gpio.output(trig,False)
    time.sleep(2)
    gpio.output(trig,True)
    time.sleep(0.00001)
    gpio.output(trig,False)
    while gpio.input(echo)==0:
            pulse_start=time.time()
    while gpio.input(echo)==1:
            pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    return distance;

def wp_start():
    #starting water pump
    gpio.output(ch1, gpio.LOW)
    print "Water Pump Start"
    return;

def wp_stop():
    #stopping water pump
    gpio.output(ch1, gpio.HIGH)
    print "Water Pump Stop"
    return;

def solenoid_start():
    #water inlet start
    gpio.output(ch2, gpio.LOW)
    print "Solenoid Start"
    return;

def solenoid_stop():
    #water inlet stop
    gpio.output(ch2, gpio.HIGH)
    print "Solenoid Stop"
    return;

def emergency():
    #checks water level for emergency droppage at every 5 mins
    on=0
    global flag3
    flag5=0
    flag6=0
    while (on == 0):
        distance=dist_measure()
        if (distance >= 52):
            if (flag5 == 0 and flag3 == 1):
                wp_stop()
                print "Emergency water pump stop"
                flag3=0
                flag5=1
                flag6=0
                print "Iteration stop for 5 min"
                time.sleep(300)
        if (distance < 52):
            if (flag6 == 0 and flag3 == 0):
                wp_start()
                print "Water pump start after emergency"
                flag3=1
                flag5=0
                flag6=1
            on=1
    return;

def time_convert( timerec ):
    now = datetime.datetime.now()
    my_time_string = timerec
    my_datetime = datetime.datetime.strptime(my_time_string, "%H:%M:%S")
    # I am supposing that the date must be the same as now
    my_datetime = now.replace(hour=my_datetime.time().hour, minute=my_datetime.time().minute, second=my_datetime.time().second, microsecond=0)
    return my_datetime;

def alltimes():
    global dayreset
    dayreset=time_convert(dayreset)
    global wpstart
    wpstart=time_convert(wpstart)
    global wpstop
    wpstop=time_convert(wpstop)
    global waterinletstart
    waterinletstart=time_convert(waterinletstart)
    global shorttime
    shorttime=time_convert(shorttime)
    return;

dayreset=time_convert(dayreset)
wpstart=time_convert(wpstart)
wpstop=time_convert(wpstop)
waterinletstart=time_convert(waterinletstart)
shorttime=time_convert(shorttime)

try:
    main=0
    while (main == 0):
        current_time=datetime.datetime.now()
        if(current_time > dayreset):
            alltimes()
        elif (current_time > shorttime and current_time < wpstart):
            distance=dist_measure()
            if (distance > 35 and current_time > waterinletstart):
                if (flag1 == 0):
                    solenoid_start()
                    print "Water inlet start for routine filling"
                    flag1=1
                    flag2=0
            if (distance <=19):
                if (flag2 == 0):
                    solenoid_stop()
                    print "Water inlet stop after routine filling"
                    flag1=0
                    flag2=1
        elif (current_time > wpstart and current_time < dayreset):
            print "coming at 1"
            if (current_time > wpstart and current_time < wpstop):
                if (flag3 == 0):
                    wp_start()
                    print "Pump start after 10am"
                    flag3=1
                    flag4=0
            if (current_time > wpstop):
                if (flag4 == 0):
                    wp_stop()
                    print "Pump stop after 10pm"
                    flag3=0
                    flag4=1
                #time.sleep(300)
                #time.sleep(1)
                #print "Iteration wait for 5 secs"
                #time.sleep(5)
            if (flag3 == 1):
                print "Entering emergency protocol"            
                emergency()
            print "Iteration wait for 5 mins"
            #time.sleep(300)
        elif (current_time < shorttime):
             print "Iteration wait for 5 mins"
        print "Iteration wait for 5 mins"
        time.sleep(300)
        

except KeyboardInterrupt:
    gpio.output(ch1, gpio.low)
    gpio.output(ch2, gpio.low)
    gpio.output(trig, False)
    gpio.cleanup()
