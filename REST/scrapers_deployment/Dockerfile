FROM ubuntu:20.04

RUN apt-get update && apt-get -y install cron python3 pip vim

WORKDIR /usr/src/

COPY src/auchan.py src/pingodoce.py src/requirements.txt ./

COPY crontab /etc/cron.d/crontab

RUN touch /usr/src/cron.log

RUN pip3 install -r requirements.txt

# run the crontab file
RUN chmod 0744 /etc/cron.d/crontab && crontab /etc/cron.d/crontab

# Executing crontab command
CMD cron && tail -f /usr/src/cron.log

