#/usr/bin/env python

import os
import signal
import websocket
import datetime
import subprocess
import sys
from pprint import pprint
import threading
import json
import binascii


try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print("TCDEBUG: on_message starting")
    global currentPid
    global currentFilename
    try:
       ws.send("CLIENT: on_message starting")
       print("TCDEBUG: message length is ", len(message))
       m = json.loads(message)
       print ("TCDEBUG: command is ", m["command"])


       if m["command"] == "KillClient":
           print("TCDEBUG: KillClient received")
           ws.send("CLIENT: KillClient received")
           killFile = open("/home/pi/pframe/killclient", "w")
           killFile.close()
           if (currentPid != -1):
                os.kill(currentPid, signal.SIGTERM)
                os.remove(currentFilename)
           os.kill(os.getpid(), signal.SIGTERM)
       else:
           print("TCDEBUG: Photo received")
           ws.send("CLIENT: photo received with basename " +  m["basename"])
           ws.send("CLIENT: photo received with caption " +  m["caption"])
           filename = "/tmp/" + m["basename"]
           f = open(filename, "wb")
           fileContents = binascii.a2b_base64(m["data"])
           f.write(fileContents)
           f.close()

           p = subprocess.Popen(["feh", "--draw-filename", "--info", 'echo "' + m["caption"] + '"', "--borderless", "--fullscreen", "--auto-rotate", filename], shell=False, stdin=None,stdout=None,stderr=None,close_fds=True)
           if p.returncode is None:
               ws.send("CLIENT: returnCode is None")
           else:
               ws.send("CLIENT: returnCode is " + str(p.returncode))
               os.kill(os.getpid(), signal.SIGTERM)

           # kill the previous feh process
           if (currentPid != -1):
               time.sleep(2)
               try:
                   os.kill(currentPid, signal.SIGTERM)
                   os.remove(currentFilename)
               except OSError:
                   ws.send("CLIENT: unable to kill currentPid: " + str(currentPid))
           currentPid = p.pid
           currentFilename=filename
    except Exception as e:
        print("ERROR: exception : ", e)
        ws.send("CLIENT ERROR, exiting...")
        os.kill(os.getpid(), signal.SIGTERM)

def on_error(ws, error):
    print("CLIENT: on_error", error)

def on_close(ws):
    print("CLIENT: on_close")

if __name__ == "__main__":
    try:
        currentPid = -1
        currentFilename=None
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://192.168.4.99:8000/",
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)

        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()

        conn_timeout = 5
        while not ws.sock.connected and conn_timeout:
            time.sleep(1)
            conn_timeout -= 1

        while ws.sock.connected:
            ws.send("SendPhoto")
            time.sleep(120)

    except Exception as e:
        print("MAIN ERROR: exception: ", e);
        os.kill(os.getpid(), signal.SIGTERM);
    else:
        print("MAIN: ending");
