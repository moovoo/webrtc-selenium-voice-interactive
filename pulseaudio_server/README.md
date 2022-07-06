# PulseAudio server container
1. Start a server with TCP transport enabled (warning: open for 0.0.0.0) in system mode (no forking)
2. Create two null sinks
   1. one for speakers 
   2. one for microphone (with remapping to source)
    
Transport module: https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#module-native-protocol-unixtcp

Sink module: https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#module-null-sink

Creating virtual source from sink monitor: https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#module-remap-source
