FROM arm32v7/python:3

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get -y upgrade \
&& apt-get install build-essential cron python3-dev python3-rpi.gpio -y

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY flomDB.py .
COPY flom.py .
CMD [ "python3", "./flom.py" ]

