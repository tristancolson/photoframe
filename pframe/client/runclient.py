#!/usr/bin/python3
from subprocess import Popen
import sys
import os

filename = sys.argv[1]
killfile = '/home/pi/pframe/killclient'
try:
    os.remove(killfile)
except OSError:
    pass


while True:
    if os.path.exists('/home/pi/pframe/killclient'):
        print ("\nKillClient received, exiting...")
        sys.exit()
    print ("\nStarting " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()

try:
    os.remove(killfile)
except OSError:
    pass
