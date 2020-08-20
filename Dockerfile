FROM python:3.8.2
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
CMD python /app/bot.py
