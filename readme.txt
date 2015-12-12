Для работы с датчиком температуры подгружаем модули:
sudo modprobe w1-gpio && sudo modprobe w1_therm

6th May 2015 Update
--------
sudo nano /boot/config.txt
dtoverlay=w1-gpio

ls -l /sys/bus/w1/devices/
cat /sys/bus/w1/devices/28-00000283c6cd/w1_slave

