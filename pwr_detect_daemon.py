import os, time
import RPi.GPIO as GPIO
import signal
import syslog
import sys
import main_mail
import os.path

PWR_DETECT_PATH='/your/path/to/pwr_detect/logs/'

def powerUpOrDown(channel):
    if GPIO.input(channel):     # if port 23 == 1  
        pwr_event = "POWER_ON"
        print "Power Up Detected on Channel ", channel, "\n"
        main_mail.mail_func("ON")
    else:                       # if port 23 != 1  
        pwr_event = "POWER_OFF"
        print "Power Down Detected on Channel ", channel, "\n"
        main_mail.mail_func("OFF")
    # Open the file in write mode
    path = PWR_DETECT_PATH + "gpio_detection.log"
    print "Writing to log file: [", path," ]"
    with open(path, "w") as gpio_file:
        print >> gpio_file, time.ctime(), "::Power State: [ ", pwr_event, " ]\n"

def handleSIGUSR(signal, frame):
    print('Received:', signal)
    path = PWR_DETECT_PATH + "sig.log"
    print "Writing to log file: [", path," ]"
    with open(path, "w") as sig_file:
         print >> sig_file, time.ctime(), "::Ho Ho Ho - Received [ ", signal, " ]\n"
    main_mail.mail_func(signal)
    GPIO.cleanup()

def handleSIGNALS(signal, frame):
    print('Received:', signal)
    path = PWR_DETECT_PATH + "sig.log"
    print "Writing to log file: [", path," ]"
    with open(path, "w") as sig_file:
         print >> sig_file, time.ctime(), "::Ho Ho Ho - Received [ ", signal, " ]\n"
    main_mail.mail_func(signal)
    GPIO.cleanup()


def createDaemon():
  """
      This function create a service/Daemon that will execute a det. task
  """

  try:
    # Store the Fork PID
    pid = os.fork()

    if pid > 0:
      print 'PID: %d' % pid
      # Open the file in write mode
      path = PWR_DETECT_PATH + "pwr.pid"
      print "Writing to log file: [", path, " ]"
      with open(path, "w") as pid_log_file:
           print >> pid_log_file, pid
      os._exit(0)

  except OSError, error:
    print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
    os._exit(1)

  doTask()

def doTask():
  """
      This function create a task that will be a daemon
  """
  #Email of a new spawn because this daemon got killed and getting 
  #respawned or a new spawn
  main_mail.mail_func("Spawned")
  print "\n"

  print "Calling handler for:SIGTERM\n"
  signal.signal(signal.SIGTERM, handleSIGNALS)
  print "Calling handler for:SIGINT\n"
  signal.signal(signal.SIGINT, handleSIGNALS)
  print "Calling handler for:SIGHUP\n"
  signal.signal(signal.SIGHUP, handleSIGNALS)
  print "Calling handler for:SIGUSR1\n"
  signal.signal(signal.SIGUSR1, handleSIGUSR)
  print "Calling handler for:SIGUSR2\n"
  signal.signal(signal.SIGUSR2, handleSIGUSR)


  try:
      # GPIO 23 set up as input.
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(23, GPIO.IN)
      while True:
          if not 'event' in locals():
             print "Adding event\n"
             # GPIO add event callback
             event = GPIO.add_event_detect(23, GPIO.BOTH, callback=powerUpOrDown, bouncetime=2000)
          else:
             #print "Continuing....\n"
             time.sleep(2)
  finally:
          GPIO.cleanup()

if __name__ == '__main__':

  # Create the Daemon
  createDaemon()
