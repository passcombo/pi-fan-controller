#!/usr/bin/env python3
import datetime
import subprocess
import time

from gpiozero import OutputDevice


ON_THRESHOLD = 61  # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 48  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 10  # (seconds) How often we check the core temperature.
GPIO_PIN = 17  # Which GPIO pin you're using to control the fan.
TEMPERATUR_SYS_PATH='/sys/class/thermal/thermal_zone0/temp'



def log_time(file_path,mode='w'): #  'a+' for append

        x=datetime.datetime.today()
        time_format='%Y-%m-%d %H:%M:%S'

        x1=x.strftime(time_format)

        with open(file_path, mode) as f:

                f.write(x1+'\n')
                f.close()





def get_temp():
        """Get the core temperature.
        Run a shell script to get the core temp and parse the output.
        Raises:
                RuntimeError: if response cannot be parsed.
        Returns:
                float: The core temperature in degrees Celsius.
        """
        output = subprocess.run(['cat',TEMPERATUR_SYS_PATH],capture_output=True)
        temp_str = output.stdout.decode()

        try:
                return float(temp_str)/1000
        except (IndexError, ValueError):
                raise RuntimeError('Could not parse temperature output.')

                
                
                

if __name__ == '__main__':

        tmp=subprocess.run(['sudo','chmod','o+rw','/dev/gpiomem'],capture_output=True)

        log_time('last_start.txt')
        # Validate the on and off thresholds
        if OFF_THRESHOLD >= ON_THRESHOLD:
                raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

        fan = OutputDevice(GPIO_PIN)

        # test run to ensure it is running
        fan.on()
        time.sleep(15)
        fan.off()


        while True:
                log_time('last_loop.txt','a+')

                temp = get_temp()
                # Start the fan if the temperature has reached the limit and the fan
                # isn't already running.
                # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
                if temp > ON_THRESHOLD and not fan.value:
                        fan.on()

                # Stop the fan if the fan is running and the temperature has dropped
                # to 10 degrees below the limit.
                elif fan.value and temp < OFF_THRESHOLD:
                        fan.off()

                time.sleep(SLEEP_INTERVAL)
