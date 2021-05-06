FROM python:3.8

COPY . /yt-api
WORKDIR /yt-api

RUN pip install -r requirements.txt

CMD ["sh", "run.sh"]

