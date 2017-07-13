#!/usr/bin/env bash
rm -rf sample.mp4
python client.py http://165.242.111.73/sample.mp4 $1 &
sleep $2s
vlc sample.mp4
