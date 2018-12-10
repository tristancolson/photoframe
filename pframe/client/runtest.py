#!/usr/bin/python3
from subprocess import Popen
import sys
import os

filename = sys.argv[1]
while True:
    if os.path.exists('killclient'):
        print ("\nKillClient received, exiting...")
        sys.exit()
    print ("\nStarting " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()

