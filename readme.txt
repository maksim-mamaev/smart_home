sudo nano /boot/config.txt
dtoverlay=w1-gpio

ls -l /sys/devices/w1_bus_master1
cat /sys/devices/w1_bus_master1/28-00000283c6cd/w1_slave


screen sudo python ./garage_basement_thermostat.py


screen [cmd]
ctrl-A + D - помещаем в фон

screen -r - возвращаемся из фона
