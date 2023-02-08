FROM python:3

WORKDIR /home/app
RUN mkdir -p /home/app
COPY *.py /home/app
CMD python /home/app/forwarder.py
