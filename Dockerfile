FROM python:3.8

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip3 install -r /app/requirements.txt
RUN chmod +x /app/main.py

CMD python3 /app/main.py;