#!/usr/bin/env python

import websocket
from PIL import Image
import datetime

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print("TCDEBUG: received message from server")
###    print(message)
###    filename = '/Users/tristan/data/images/penguins/penguin1.jpg'
    filename = "/tmp/photofoo"
    f = open(filename, "wb")
    f.write(message)
    f.close()
###    try:
###        im = Image.open(filename)
###        im.show()
###        im.close()
###    except:
###        print("ERROR: unable to load image ", filename)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
###        for i in range(1):
        while True:
            print (str(datetime.datetime.now()), "TCDEBUG: Sending message to server...")
            ws.send("SendPhoto")
            time.sleep(20)

        time.sleep(1)
        print("TCDEBUG: closing ...")
        ws.close()
        print("thread terminating...")


    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.4.99:8000/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

