sudo nano /boot/config.txt
dtoverlay=w1-gpio

ls -l /sys/devices/w1_bus_master1
cat /sys/devices/w1_bus_master1/28-00000283c6cd/w1_slave


screen sudo python ./garage_basement_thermostat.py


screen [cmd]
ctrl-A + D - помещаем в фон

screen -r - возвращаемся из фона


17 - батарея
18 - вентилятор
22 - точки
23 - точки 2 группа
24 - лента 2 группа
25 - лента


