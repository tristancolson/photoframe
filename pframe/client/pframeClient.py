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
    try:
        print ("TCDEBUG: A on_message starting")
        ws.send("CLIENT: on_message starting")
        filename = "/tmp/photofoo"
        f = open(filename, "wb")
        f.write(message)
        f.close()

        p = subprocess.Popen(["feh", "--borderless", "--fullscreen", "--auto-rotate", filename], shell=False, stdin=None,stdout=None,stderr=None,close_fds=True)
        print ("TCDEBUG: B")
        print(str(datetime.datetime.now()) + " TCDEBUG C: pid from subprocess is " +  str(p.pid))
        ws.send("CLIENT C: pid from subprocess is " +  str(p.pid))
        if p.returncode is None:
            print(str(datetime.datetime.now()) + " TCDEBUG D: returnCode is None")
            ws.send("CLIENT D: returnCode is None")
        else:
            print(str(datetime.datetime.now()) + " TCDEBUG E: returnCode is " + str(p.returncode))
            ws.send("CLIENT E: returnCode is " + str(p.returncode))
            os.kill(os.getpid(), signal.SIGTERM)
            
        
        # kill the previous feh process
        print(str(datetime.datetime.now()) + " TCDEBUG F: currentPid is " + str(currentPid))
        ws.send("CLIENT F: currentPid is " + str(currentPid))
        if (currentPid != -1):
            print(str(datetime.datetime.now()) + " TCDEBUG G: killing currentPid: " + str(currentPid))
            ws.send("CLIENT G: killing currentPid: " + str(currentPid))
            time.sleep(2)
            try:
                os.kill(currentPid, signal.SIGTERM)
            except OSError:
                print(str(datetime.datetime.now()) + " TCDEBUG G1: unable to kill currentPid: " + str(currentPid))
                ws.send("CLIENT G1: unable to kill currentPid: " + str(currentPid))
            else:
                print(str(datetime.datetime.now()) + " TCDEBUG G2: killed currentPid: " + str(currentPid))
                ws.send("CLIENT G2: killed currentPid: " + str(currentPid))
        currentPid = p.pid
        ws.send("CLIENT: bottom of try")
        print("CLIENT: bottom of try")
    except Exception as e:
        print("ERROR: exception : ", e)
        ws.send("CLIENT ERROR, exiting...")
        os.kill(os.getpid(), signal.SIGTERM)
    else:
        ws.send("CLIENT: completed on_message")
        print("CLIENT: completed on_message")

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

        print("===========")
        for attr in dir(ws):
            print("obj.%s = %r" % (attr, getattr(ws, attr)))
        print("===========")

        i = 0
        while ws.sock.connected:
            if ws.sock.connected:
                print(str(datetime.datetime.now()) + " TCDEBUG: a ws.sock.connected is " + str(ws.sock.connected));
            else:
                print(str(datetime.datetime.now()) + " TCDEBUG: a ws.sock.connected is GONE");

            i = i + 1
            ws.send("CLIENT: start loop: " + str(i))
            if ws.sock.connected:
                print(str(datetime.datetime.now()) + " TCDEBUG: b ws.sock.connected is " + str(ws.sock.connected));
            else:
                print(str(datetime.datetime.now()) + " TCDEBUG: b ws.sock.connected is GONE");

            print(str(datetime.datetime.now()) + " TCDEBUG: before SendPhoto " + str(i))
            ws.send("SendPhoto")
            if ws.sock.connected:
                print(str(datetime.datetime.now()) + " TCDEBUG: c ws.sock.connected is " + str(ws.sock.connected));
            else:
                print(str(datetime.datetime.now()) + " TCDEBUG: c ws.sock.connected is GONE");

            print(str(datetime.datetime.now()) + " TCDEBUG: after SendPhoto")
            time.sleep(120)
            if ws.sock.connected:
                print(str(datetime.datetime.now()) + " TCDEBUG: d ws.sock.connected is " + str(ws.sock.connected));
            else:
                print(str(datetime.datetime.now()) + " TCDEBUG: d ws.sock.connected is GONE");
            ws.send("CLIENT: end loop: " + str(i))
            print("CLIENT: end loop: " + str(i))
            if ws.sock.connected:
                print(str(datetime.datetime.now()) + " TCDEBUG: e ws.sock.connected is " + str(ws.sock.connected));
            else:
                print(str(datetime.datetime.now()) + " TCDEBUG: e ws.sock.connected is GONE");

        if ws.sock.connected:
            print(str(datetime.datetime.now()) + " TCDEBUG: f ws.sock.connected is " + str(ws.sock.connected));
        else:
            print(str(datetime.datetime.now()) + " TCDEBUG: f ws.sock.connected is GONE");
        print("CLIENT: ws.sock.connected LOOP ENDS")

    except Exception as e:
        print("MAIN ERROR: exception: ", e);
        os.kill(os.getpid(), signal.SIGTERM);
    else:
        print("MAIN: ending");
