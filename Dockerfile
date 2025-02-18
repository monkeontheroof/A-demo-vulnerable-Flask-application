FROM python:3.12.1

RUN mkdir -p /app

WORKDIR /app

# Selenium configuration
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    wget https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.119/linux64/chromedriver-linux64.zip -P /app && \
    unzip /app/chromedriver-linux64.zip -d /app && \
    rm /app/chromedriver-linux64.zip && \
    mv -f /app/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chown root:root /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y cron supervisor wget unzip google-chrome-stable curl

RUN echo "FLAG{Wh0s3_r3qU3s7_1s_17?}" >> /etc/passwd

COPY ./ /app

EXPOSE 8081

# Cronjob configuration
RUN mkdir /etc/cron.custom
RUN echo "*/5 * * * * root rm -rf /app/web/static/uploads/*" > /etc/cron.custom/cleanup-cron
# RUN echo "* * * * * root cd / && run-parts --report /etc/cron.custom" | tee -a /etc/crontab
RUN echo "SHELL=/bin/sh" >> /etc/crontab
RUN echo "*/5 * * * * root run-parts /etc/cron.custom" >> /etc/crontab

# Copy Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start Supervisor
CMD ["/usr/bin/supervisord"]