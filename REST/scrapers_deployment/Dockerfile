FROM python:3

RUN apt-get update && apt-get -y install cron

WORKDIR /usr/src/scrapers

COPY scrapers_deployment/scrapers/auchan.py scrapers_deployment/scrapers/pingodoce.py scrapers_deployment/scrapers/requirements.txt ./

COPY scrapers_deployment/crontab /etc/cron.d/crontab

RUN pip3 install -r requirements.txt

# run the crontab file
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# Executing crontab command
CMD ["cron", "-f"]
#CMD ["python3","pingodoce.py"]
