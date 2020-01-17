FROM python:3.6-stretch

RUN mkdir -p /tmp/airtime

WORKDIR /tmp/airtime

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT python main.py config.ini