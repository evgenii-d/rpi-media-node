#!/bin/bash
media=""
module="any"
playback="-L"
rc_host="127.0.0.1"
rc_port="50000"

vlc $media -f -I dummy -V $module $playback --aout="alsa" --alsa-audio-device="sysdefault:CARD=Headphones" --one-instance --key-next="Page Up" --key-prev="Page Down" --video-on-top --no-video-title-show --playlist-autostart --extraintf oldrc --rc-fake-tty --rc-host=$rc_host:$rc_port
