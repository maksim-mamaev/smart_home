
import time
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta, date, time as dt_time
 
FREQ = 300 # 5 min
run = True
heatStatus = -1 # -1-onStart;0-off;1-on

relayPin = 17
w1_address = "28-00000477f239"
normallyOpen = True

#22-22.5 - it's cold for the night +0.5, may be ok for the day
#22.5-23 - is ok fot the night
dayMinTemp = 22
dayMaxTemp = 22.5
nightMinTemp = 22.5
nightMaxTemp = 23

def get_temp():
	# Open the file that we viewed earlier so that python can see what is in it. Re$
	tfile = open("/sys/devices/w1_bus_master1/" + w1_address + "/w1_slave")
	# Read all of the text in the file.
	text = tfile.read()
	# Close the file now that the text has been read.
	tfile.close()
	# Split the text with new lines (\n) and select the second line.
	secondline = text.split("\n")[1]
	# Split the line into words, referring to the spaces, and select the 10th word $
	temperaturedata = secondline.split(" ")[9]
	# The first two characters are "t=", so get rid of those and convert the temper$
	temperature = float(temperaturedata[2:])
	# Put the decimal point in the right place and display it.
	temperature = temperature / 1000

	return temperature

def heat(heat_on):
	pin_status = GPIO.LOW

	if heat_on:
		log('Heat on')

		if normallyOpen:
			pin_status = GPIO.LOW
		else:
			pin_status = GPIO.HIGH
	else:
		log('Heat off')

		if normallyOpen:
			pin_status = GPIO.HIGH
		else:
			pin_status = GPIO.LOW

	try:
		# Use the pin numbers from the ribbon cable board.
		GPIO.setmode(GPIO.BCM)

		# Set up the pin as output.
		GPIO.setup(relayPin, GPIO.OUT)

		GPIO.output(relayPin, pin_status)

	finally:
		pass
#		GPIO.cleanup()

def get_min_temperature():
	d = datetime.today()
	h = d.hour

	if h >= 0 and h <= 7:
		resT = nightMinTemp
	else:
		resT = dayMinTemp

	return resT

def get_max_temperature():
	d = datetime.today()
	h = d.hour

	if h >= 0 and h <= 7:
		resT = nightMaxTemp
	else:
		resT = dayMaxTemp

	return resT

def nobody_home():
	d = datetime.today()
	wd = d.weekday()
	h = d.hour
	
	return (wd >= 0 and wd < 5 and h > 7 and h < 20) 

def log(s):
        print s

	f1=open('./climate.log', 'a')
	f1.write(s+'\n')
	f1.close()

while(run):
        try:
                time.sleep(FREQ)
		
		curT = get_temp()
		minT = get_min_temperature()
		maxT = get_max_temperature()

		params = (time.strftime("%Y-%m-%d %H:%M"), str(curT), str(minT), str(maxT), str(nobody_home()), str(heatStatus))
		log('{0} curT={1};minT={2};minT={3};nobody_home={4};heat_status(-1-onStart;0-off;1-on)={5}'.format(*params))

		if(curT < minT and not nobody_home()):
			if(heatStatus != 1):
				heat(True)
				heatStatus = 1

		elif(curT > maxT or nobody_home()):
			if(heatStatus != 0):
				heat(False)
				heatStatus = 0

        except KeyboardInterrupt:
                run = False

