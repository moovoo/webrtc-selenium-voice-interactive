FROM ubuntu:kinetic

RUN apt-get update && apt-get install -y --no-install-recommends pulseaudio && rm -rf /var/lib/apt/lists/*

ADD pulse.cfg /

EXPOSE 4713

CMD ["/usr/bin/pulseaudio", "--system", "-nF", "pulse.cfg"]
