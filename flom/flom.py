import RPi.GPIO as GPIO
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from RpiMotorLib import rpiservolib 
import schedule
import functools


#Protect against exceptions
def catch_exceptions(cancel_on_failure=False):
  def catch_exceptions_decorator(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
      try:
        return job_func(*args, **kwargs)
      except:
        import traceback
        print(traceback.format_exc())
        if cancel_on_failure:
          return schedule.CancelJob
    return wrapper
  return catch_exceptions_decorator

# https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/Documentation/Servo_RPI_GPIO.md
myservotest  = rpiservolib.SG90servo("servoone", 50, 3, 11)
servoPIN = 17
servoStartDegrees = 10
degrees = 10
#logfile = "/var/log/flomlog.txt"

# Calculate with 110degrees as middle flood (440 M3s),
# The 50 years flood is then at 175 degree (691 M3s)
# Define the job:

@catch_exceptions(cancel_on_failure=True)
def job():
  global servoStartDegrees
  global degrees
  r = re.compile("verdi=\s*")
  response = urlopen('https://www2.nve.no/h/hd/plotreal/Q/0208.00003.000/')
  soup =  BeautifulSoup(response.read(), 'html.parser')
  for tag in soup.find_all(text=re.compile("verdi=\s*\d+.\d+")):
    newlist = list(filter(r.match, tag.string.split())) 
    value = float(re.sub(r.pattern,'',newlist[0]))
    print(value)
    degrees = (value / 440) * 110
  #to move a servo on GPIO pin servpPIN from 10 degrees to degrees in 3 degree steps every two seconds, with an initial delay of one second and verbose output.
  myservotest.servo_move_step(servoPIN, servoStartDegrees, int(degrees), 2, 3, 1, True)
  print("Moved to", degrees, "degrees")
  servoStartDegrees = int(degrees)
#  f = open(logfile, "a")
#  f.write("value and Degrees")
#  f.write(value)
#  f.write(degrees)
#  f.close()

# Run the job every 10 minutes
schedule.every(10).minutes.do(job)
#schedule.every(10).seconds.do(job)

while True:
  schedule.run_pending()
  time.sleep(1)

# good practise to cleanup GPIO at some point before exit
GPIO.cleanup()

