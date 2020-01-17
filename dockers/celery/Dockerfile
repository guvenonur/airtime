FROM python:3.6

RUN mkdir -p /tmp/airtime

WORKDIR /tmp/airtime

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT celery -A main.celery -b redis://redis:6379 worker