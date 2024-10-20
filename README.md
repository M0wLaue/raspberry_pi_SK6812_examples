# raspberry_pi_SK6812_examples

PWM wird verwendet -> Soundmodule der ARM CPU deaktivieren, sonst gibts Störungen:
sudo nano /boot/config.txt
`dtparam=audio=on` -> `#dtparam=audio=on`

Laden des Modules unterbinden:
sudo nano /etc/modprobe.d/snd-blacklist.conf
+ `blacklist snd_bcm2835`

Nach Systemneustart mit `lsmod` prüfen. -> Das Modul `snd_bcm2835` sollte nicht geladen sein.

laden
`git clone https://github.com/M0wLaue/raspberry_pi_SK6812_examples`

dependencies
`pip3 install -r requirements.txt`
auf dem pi entweder mit apt installieren oder einfach hardcore über den superschönen Parameter `--break-system-packages`
Hier als Beispiel:
`sudo apt install python3-rpi_ws281x`
oder alternativ
`sudo pip3 install rpi_ws281x --break-system-packages`

start
`python3 main.py`
