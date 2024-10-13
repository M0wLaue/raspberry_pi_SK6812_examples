# raspberry_pi_SK6812_examples

Da wir PWM verwenden muss auch noch das Soundmodule der ARM CPU deaktiviert werden. Andernfalls könnte es zu Störungen kommen:
sudo nano /boot/config.txt

und dort am Ende der Datei
dtparam=audio=on

auskommentieren:
#dtparam=audio=on

Dann noch das nachträgliche Laden des Modules unterbinden:
sudo nano /etc/modprobe.d/snd-blacklist.conf

und
blacklist snd_bcm2835

einfügen.

Nach einen Systemneustart kann mit dem Befehl:
lsmod

nachgeschaut werden ob das  “snd_bcm2835” Module nicht mehr geladen ist. Es sollte in der Auflistung nicht mehr auftauchen.

`sudo pip3 install rpi_ws281x --break-system-packages`
