import sys, RPi.GPIO as GPIO

pin = int(sys.argv[1])
on = int(sys.argv[2])

print pin
print on

# Use the pin numbers from the ribbon cable board.
GPIO.setmode(GPIO.BCM)
# Set up the pin you are using ("18" is an example) as output.
GPIO.setup(pin, GPIO.OUT)
# Turn on the pin and see the LED light up.
#GPIO.output(pin, GPIO.HIGH)
# Turn off the pin to turn off the LED.
if on == 1:
	GPIO.output(pin, GPIO.HIGH)
elif on == 0:
	GPIO.output(pin, GPIO.LOW)

