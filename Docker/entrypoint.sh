#!/bin/bash

export DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --nopidfile --fork)
echo $DBUS_SESSION_BUS_ADDRESS > dbus.session
/usr/lib/ring/dring &
python3 echo.py
