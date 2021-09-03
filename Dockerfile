FROM python:3.8-slim

ENV DEEPSPEECH_VERSION=0.9.3

WORKDIR /opt

RUN apt-get update -y && apt-get install -y wget

RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm && \
    wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

RUN pip install deepspeech ffmpeg moviepy

RUN apt-get install sox -y

COPY main.py .

CMD [ "python", "main.py" ]