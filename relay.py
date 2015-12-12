import RPi.GPIO as GPIO
# Use the pin numbers from the ribbon cable board.
GPIO.setmode(GPIO.BCM)
# Set up the pin you are using ("18" is an example) as output.
GPIO.setup(17, GPIO.OUT)
# Turn on the pin and see the LED light up.
#GPIO.output(17, GPIO.HIGH)
# Turn off the pin to turn off the LED.
GPIO.output(17, GPIO.LOW)
