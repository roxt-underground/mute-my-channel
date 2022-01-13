FROM python:3.9-alpine

WORKDIR /

RUN mkdir /bot && \
    adduser -h /bot -s /bin/bash -G root -u 1001 --disabled-password bot

WORKDIR /bot
USER bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./
RUN ls
ENTRYPOINT /bot/bot.py
