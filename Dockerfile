FROM python:3.13

RUN pip install --upgrade pip
RUN pip install dnspython>=2.7 requests
ADD dns-watchdog.py /app

ENV TIMEOUT=15
ENV SERVERS=192.168.1.2;192.168.1.9
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/usr/bin/env", "python", "/app" ]
