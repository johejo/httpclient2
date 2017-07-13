#!/usr/bin/env bash
python client.py http://165.242.111.73/sample.mp4 5 &
sleep 3m
python movie_play.py
