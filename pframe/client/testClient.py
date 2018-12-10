#/usr/bin/env python

import os
import signal
import websocket
import datetime
import subprocess
import sys
from pprint import pprint
import threading


try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    global currentPid
    print("TCDEBUG: on_message, type message is ", type(message))
    print("TCDEBUG: on_message starting: ", message)
    if message == "KillClient":
        print("TCDEBUG: A found KC")
    else:
        print("TCDEBUG: B NOT found KC")

    print("TCDEBUG: C")
    try:
        ws.send("CLIENT: on_message starting")
        if message == "KillClient":
            print("TCDEBUG: KillClient received")
            ws.send("CLIENT: KillClient received")
            killFile = open("killclient", "w")
            killFile.close()
            os.kill(currentPid, signal.SIGTERM)
        else:
            print("TCDEBUG: Photo received")
            ws.send("CLIENT: photo received")
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
            time.sleep(20)

    except Exception as e:
        print("MAIN ERROR: exception: ", e);
        os.kill(os.getpid(), signal.SIGTERM);
    else:
        print("MAIN: ending");
