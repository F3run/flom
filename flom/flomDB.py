import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import functools


servoStartDegrees = 10
degrees = 10
#logfile = "/var/log/flomlog.txt"

# Calculate with 110degrees as middle flood (440 M3s),
# The 50 years flood is then at 175 degree (691 M3s)
# Define the job:

response = urlopen('https://www2.nve.no/h/hd/plotreal/Q/0208.00003.000/')
soup =  BeautifulSoup(response.read(), 'html.parser')
r = re.compile("verdi=\s*")

for tag in soup.find_all(text=re.compile("verdi=\s*\d+.\d+")):
  print(tag.string.split())
  newlist = list(filter(r.match, tag.string.split()))
  value = float(re.sub(r.pattern,'',newlist[0]))
  print("value: ", value)
  degrees = (value / 440) * 110
  print("Moved to", degrees, "degrees")

