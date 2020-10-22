
import time 
import RPi.GPIO as GPIO 
import time 
from datetime import datetime, timedelta, date, time as dt_time
 
FREQ = 60 # 1 min
run = True
heatStatus = -1 # -1-onStart;0-off;1-on
heatStatusBalkon = -1
fanStatus = -1

relayPinLight = 22
relayPinRoom = 17
relayPinBalkon = 27
relayPinFan = 18
w1_room_address = "28-00044c023eff"
w1_balkon_address = "28-00043b8066ff"

normallyOpen = False

#22-22.5 - it's cold for the night +0.5, may be ok for the day
#22.5-23 - is ok fot the night
#21.10: 21.5-22 try increase to day temp
#22.10 night down 0.5
dayMinTemp = 23 #23.25
dayMaxTemp = 23.25 #23.5
nightMinTemp = 22.75 #22.75 -> 23
nightMaxTemp = 23 #23 -> 23.25

balkonMinTemp = 21 #20.5
balkonMaxTemp = 21.2 #21

def get_temp(w1_address):
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

def heat(relayPin, heat_on):
	result = ""
	pin_status = GPIO.HIGH

	if heat_on:
		result = 'Heat on'

		if normallyOpen:
			pin_status = GPIO.HIGH
		else:
			pin_status = GPIO.LOW
	else:
		result = 'Heat off'

		if normallyOpen:
			pin_status = GPIO.LOW
		else:
			pin_status = GPIO.HIGH

	try:
		# Use the pin numbers from the ribbon cable board.
		GPIO.setmode(GPIO.BCM)

		# Set up the pin as output.
		GPIO.setup(relayPin, GPIO.OUT)

		GPIO.output(relayPin, pin_status)

	finally:
		pass
#		GPIO.cleanup()
	
	return result 

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

def fanEnabled(curTemp):
	d = datetime.today()
	m = d.minute

	return curTemp >= 22 and ((m > 0 and m <=5) or (m > 30 and m <= 35)) # or (m > 15 and m <=20) or (m > 45 and m <=50))

def log(s):
        print s

	f1=open('./logs/climate.log', 'a')
	f1.write(s+'\n')
	f1.close()

def log2(s):
        print s

        f1=open('./logs/climate_balkon.log', 'a')
        f1.write(s+'\n')
        f1.close()

roomHeatEnabled = True
roomFanEnabled = True
balkonHeatEnabled = True

while(run):
        try:
                time.sleep(FREQ)
		
		curT = get_temp(w1_room_address)
		minT = get_min_temperature()
		maxT = get_max_temperature()

                if(roomHeatEnabled):
			params = (time.strftime("%Y-%m-%d %H:%M"), str(curT), str(minT), str(maxT), str(heatStatus))
			log('{0} curT={1};minT={2};maxT={3};heat_status(-1-onStart;0-off;1-on)={4}'.format(*params))
		
			if(curT < minT):
				if(heatStatus != 1):
					res = heat(relayPinRoom, True)
					log(res)
					heatStatus = 1

			elif(curT > maxT):
				if(heatStatus != 0):
					res = heat(relayPinRoom, False)
					log(res)
					heatStatus = 0

		if(balkonHeatEnabled):
			curTBalkon = get_temp(w1_balkon_address)
        	        params = (time.strftime("%Y-%m-%d %H:%M"), str(curTBalkon), str(balkonMinTemp), str(balkonMaxTemp), str(heatStatusBalkon))
                	log2('{0} curT={1};minT={2};maxT={3};heat_status(-1-onStart;0-off;1-on)={4}'.format(*params))
		
	                if(curTBalkon < balkonMinTemp):
	                        if(heatStatusBalkon != 1):
	                                res = heat(relayPinBalkon, True)
	                                log2(res)
					heatStatusBalkon = 1

        	        elif(curTBalkon > balkonMaxTemp):
	                        if(heatStatusBalkon != 0):
        	                        res = heat(relayPinBalkon, False)
					log2(res)
                        	        heatStatusBalkon = 0

		if(roomFanEnabled):
			params = (time.strftime("%Y-%m-%d %H:%M"), str(curT), str(fanStatus))			
			log('{0} curT={1};fan_status(-1-onStart;0-off;1-on)={2}'.format(*params))

			if(fanEnabled(curT)):
				if(fanStatus != 1):
					res = heat(relayPinFan, True)
					log(res)					
					fanStatus = 1
			else:
                                if(fanStatus != 0):
                                        res = heat(relayPinFan, False)
					log(res)                                        
					fanStatus = 0

        except KeyboardInterrupt:
                run = False

