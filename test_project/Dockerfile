FROM python:3.10

RUN apt-get update && apt-get install -y pulseaudio-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /tests

ADD hello-world.wav .
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD test_webrtc_voice.py .

CMD ["pytest"]