import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)

trig=23
echo=24

print "Distance Measurement in Progress"

gpio.setup(trig,gpio.OUT)
gpio.setup(echo,gpio.IN)

gpio.output(trig,False)
print "Waiting for Sensor to settle"
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
print "Distance: ", distance, "cm"





gpio.cleanup()
