from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import sys
import datetime
import psycopg2
import random

port = int(sys.argv[1])



class SendPhoto(WebSocket):

    def handleMessage(self):
        global sendKillClient
        try:
            if self.data == "SendPhoto":
                if sendKillClient:
                    sendKillClient = False
                    print ("TCDEBUG: sending KillClient to client")
                    self.sendMessage("KillClient")
                else:
                    print(str(datetime.datetime.now()), " SERVER: SendPhoto message");
                    # send to the client
                    self.sendMessage("SendPhoto response")
            elif self.data == "KillClient":
                print(str(datetime.datetime.now()), "KillClient msg received")
                sendKillClient = True
            else:
                print(str(datetime.datetime.now()), "CLIENT  message ", self.data)
        except Exception as e:
            print("SERVER: exception: " , e)
            os.kill(os.getPid(), signal.SIGTERM)


    def handleConnected(self):
        print(self.address, ' connected')

    def handleClose(self):
        print(str(datetime.datetime.now()), self.address, 'closed')


sendKillClient = False

server = SimpleWebSocketServer('', port, SendPhoto)
server.serveforever()
