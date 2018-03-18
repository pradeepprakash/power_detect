#!/bin/bash
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
PWR_DETECT_PATH='/your/path/to/pwr_detect'
PIDFILE="$PWR_DETECT_PATH/logs/pwr.pid"

/bin/ps up `cat $PIDFILE` >/dev/null && up=1 || up=0

if [[ $up -eq 1 ]]; then
  echo `date` ":Already running."
  exit 99
fi

echo " Reached here!"
/usr/bin/python $PWR_DETECT_PATH/pwr_detect_daemon.py 
echo "Waiting for 5 seconds for Daemon to settle down...."
sleep 5
echo "Done waiting for 5 seconds...."
