# Pi Fan Controller

Raspberry Pi fan controller.

Added features:
1. Start log file, 
2. loop logs, 
3. start fan run for 15 seconds to be sure it is working, 
4. different method of temperature measuring (more general for other rpi OS like Ubuntu)
5. added chmod to be able to read and write gpio on Ubuntu

## Description

This repository provides scripts that can be run on the Raspberry Pi that will
monitor the core temperature and start the fan when the temperature reaches
a certain threshold.

To use this code, you'll have to install a fan. The full instructions can be
found on our guide: [Control Your Raspberry Pi Fan (and Temperature) with Python](https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python).
