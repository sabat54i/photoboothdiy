# Photobooth DIY

Here you will find code for my wedding photobooth made with a Raspberry pi under Raspbian.
It can be optimised but I didn't have time to do.

You can see all steps to make a photobooth on this instructables: https://www.instructables.com/id/Wedding-Event-Photobooth/

Requires for the code works:

1. Enable Camera module

To enable the camera module there is a little configuration to do: https://www.raspberrypi.org/documentation/usage/camera/

2. Prepare Raspbian with all librairies you need

* Install Python (because program is made with Python), you will find how to do here: https://www.raspberrypi.org/documentation/linux/software/python.md

* Install Pygame (library for python graphical interface), more information here: https://www.packtpub.com/mapt/book/hardware_and_creative/9781785285066/3/ch03lvl1sec19/installing-pygame

* Install Picamera (library for the camera module of Raspberry pi): https://www.raspberrypi.org/documentation/linux/software/python.md

* Install Python module RPI.GPIO (library for control Raspberry GPIO for the arcade button): https://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio

* Install CUPS to add a printer on Raspbian, you will find how to do here: https://www.howtogeek.com/169679/how-to-add-a-printer-to-your-raspberry-pi-or-other-linux-computer/

* Install PIL (library for images on Python): https://www.pkimber.net/howto/python/modules/pillow.html

To run it you just have to launch a terminal, navagate to the program folder and type "sudo python camera.py"

If you want to test it without a button wire on GPIO Pin 25 of the raspberry, you can push down arrow of your keyboard.

Finally, I wanted to run the program at startup of the raspberry pi so I followed this tuto https://www.simplified.guide/linux/automatically-run-program-on-startup

The script which launch at startup is on the Github: photobooth-script.sh 
