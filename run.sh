#!/bin/bash
# Run as super-user

sudo python3 transmission/main.py &
sudo python3 lcd/main.py &
sudo python3 airquality/main.py &
