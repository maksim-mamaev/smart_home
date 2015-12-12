
import time
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta, date, time as dt_time
 
FREQ = 300 # 5 min
f = True
run = True

#22-22.5 - it's cold for the night +0.5, may be ok for the day
#22.5-23 - is ok, try to decrease -0.25
minTemp = 22.5
maxTemp = 23
heatStatus = -1 # -1-onStart;0-off;1-on

def get_temp():
	# Open the file that we viewed earlier so that python can see what is in it. Re$
	tfile = open("/sys/devices/w1_bus_master1/28-00000477f239/w1_slave")
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

def heat(b):
	try: 
		# Use the pin numbers from the ribbon cable board.
		GPIO.setmode(GPIO.BCM)
		# Set up the pin you are using ("18" is an example) as output.
		GPIO.setup(17, GPIO.OUT)
		# Turn on the pin and see the LED light up.
		if b == 1:
			GPIO.output(17, GPIO.LOW)
		else:
			# Turn off the pin to turn off the LED.
			GPIO.output(17, GPIO.HIGH)
	finally:		
		pass
#		GPIO.cleanup()

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
		
		t = get_temp();
		
		log(time.strftime("%Y-%m-%d %H:%M ") + 't=' + str(t) + ';nobody_home='+str(nobody_home())+';heat_status(-1-onStart;0-off;1-on)='+str(heatStatus))
		
		if(t < minTemp and not nobody_home()):
			if(heatStatus != 1):
				heat(1)
				heatStatus = 1
				log('Heat on')
				
		elif(t > maxTemp or nobody_home()):
			if(heatStatus != 0):
				heat(0)
				heatStatus = 0
				log('Heat off')

        except KeyboardInterrupt:
                run = False

