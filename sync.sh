#!/usr/bin/env bash
# Convenience script to copy the code to my rapsberry pi
rsync -rvuh --delete --force --exclude '.venv/' --exclude '__pycache__' ./ pi@192.168.1.254:/home/pi/TempMeter/