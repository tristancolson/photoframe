#/usr/bin/env python

import os
import signal
from websocket import create_connection
import datetime
import sys
import time



if __name__ == "__main__":
    ws = create_connection("ws://192.168.4.99:8000/")
    ws.send("KillClient")
    ws.close();
