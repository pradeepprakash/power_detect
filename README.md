# Power Detect Scripts


## Files | Description

-   logs                                   | logs directory that contains the log files and pid file
-   cronjobs.txt                           | The cronjob line to include for every 5 minute check.
	- cronlogs.log                         | The logs from cron to debug; can be disabled.
	- gpio_detection.log                   | GPIO state change logs maintained.
	- pwr.pid                              | PID file to maintain pid.
	- sig.log                              | Any SIGNALS caught will be logged here.
-   main_mail.py                           | email worker script using smpt in its simplest form.
-   pwr_det_daemon_rpi3_spawn_if_killed.sh | The file to be installed as cron. Will check if daemon is alive, if not re-spawns, else does nothing.
-   pwr_detect_daemon.py                   | Main python script containing business logic and logging.
-   README.md                              | This file with some help and description.

## What it does
The daemon will inform power failure.It uses Raspberry Pi GPIO pins to implement
the functionality.
These worker scripts will spawn a python daemon that will monitor changes on the 
GPIO pins of the Raspberry Pi. The GPIO pins are connected to a source which 
will change state based on the power present or not. Google search for circuitry 
needed to achieve this hardware.

##  Configuratiosn needed
###  In file <main_mail.py>
    - Replace from.name@someemail.com with email id from which email is to be sent.
    - Replace password_here with the account password. 
    - Replace to.name@someemail.com with email id to which email is to be sent.
    - Replace From_Name with  Sender's name
###  In file <pwr_det_daemon_rpi3_spawn_if_killed.sh>
    - set PWR_DETECT_PATH to path where pwr_detect scripts are located.
###  In file <pwr_detect_daemon.py>
    - set PWR_DETECT_PATH to path where pwr_detect scripts are located.
