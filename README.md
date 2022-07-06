# Interactive audio in Selenium testing using PulseAudio server
General idea:
1. Have a PulseAudio instance running with TCP transport enabled with special null sinks
2. Run a headless browser with PULSE_SERVER environment variable
3. Communicate with PulseAudio server using pulseaudio-utils (`paplay`, `pacat`) 

Purpose: 
testing complex audio scenarios, SIP calls, IVRs etc. when default browser fake audio device is not suitable  
## How to run the example
Build images:
```shell
cd pulseaudio_server/
sudo podman build -t pulseaudio .
cd ../test_project
sudo podman build -t testproject .
```
Run containers in a separate network: 
```shell
sudo podman network create test1
# run pulseaudio server
sudo podman run -d --name=pulse --network=test1 pulseaudio
# run standalone chrome, important to set PULSE_SERVER to corresponding hostname or ip address
sudo podman run -d --name chrome -e PULSE_SERVER=pulse --network=test1 --shm-size="2g" selenium/standalone-chrome
# run the test, PULSE_SERVER also must be set. also remote selenium address is 'chrome' as per container name
sudo podman run -it --rm -v "$(pwd):/artifacts/" --network=test1 -e PULSE_SERVER=pulse testproject pytest --driver Remote --selenium-host chrome --selenium-port 4444 --capabilit
y browserName chrome --html=/artifacts/report.html
```
You should see report.html and speakers.wav with a few "hello world" phrases in your current directory meaning that browser has successfully recorded an audio from fake microphone and then played the recording back to a fake speakers

TODO: docker+compose
### Note:
Running multiple browsers/tabs/calls with single Pulseaudio server makes it use same sinks
Changing default sinks runtime causes all clients to switch to a new default sink

### Workaround
1. Have a server with default speaker/mic sinks
2. A browser starts a session/call with default speaker/mic sinks
3. Using Pulseaudio CLI socket `module-cli-protocol-{unix,tcp}` (or pactl) create a new pair of sinks specific for that session/call
4. Assuming you know PID of a browser move existing streams (sink input, source output) to a new pair of sinks, see `pactl move-sink-input` and `pactl move-source-output` 

Limitations:
1. Remote Selenium does not provide browser PID, therefore can't find needed stream ID. Technically possible with Firefox (`capabilities['moz:profile']`), but see limitation #2
2. For some reason FF creates Pulseaudio sinks with DONT_MOVE flag, which makes step #4 impossible (unless fixed in source code of FF or Pulseaudio) 
