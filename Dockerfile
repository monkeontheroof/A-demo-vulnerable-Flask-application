FROM python:3.12.1

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y cron
RUN echo "FLAG{Wh0s3_r3qU3s7_1s_17?}" >> /etc/passwd

COPY ./ /app

EXPOSE 8081

RUN mkdir /etc/cron.custom
RUN echo "*/5 * * * * root rm -rf /app/app/static/uploads/*" > /etc/cron.custom/cleanup-cron
RUN echo "* * * * * root cd / && run-parts --report /etc/cron.custom" | tee -a /etc/crontab
# Give execution rights on the cron job
RUN chmod +x /etc/cron.custom/cleanup-cron
RUN crontab /etc/cron.custom/cleanup-cron
RUN crontab /etc/crontab

CMD ["sh", "-c", "cron && python main.py"]