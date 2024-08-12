FROM python:3.12.1-alpine

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./website /app/app
COPY ./ /app

EXPOSE 8081

CMD ["python", "main.py"]