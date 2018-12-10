from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import sys
import os
import datetime
import psycopg2
import random
import json
import binascii

port = int(sys.argv[1])



class SendPhoto(WebSocket):

    def handleMessage(self):
        global sendKillClient
        try:
            if self.data == "SendPhoto":
                if sendKillClient:
                    print("TCDEBUG: AAA")
                    sendKillClient = False
                    msg = json.dumps({"command": "KillClient"})
                    print("TCDEBUG: msg = ", msg)
                    ###self.sendMessage("Kil +  type(fileContent))lClient")
                    self.sendMessage(msg)
                else:
                    print(str(datetime.datetime.now()), " SERVER: SendPhoto message");

                    # generate random number based on total photos
                    cur.execute("select count(*) from photos")
                    result = cur.fetchone()
                    totalPhotos = result[0]
                    r = random.randint(1, totalPhotos)
        
                    # select that photo from the db
                    q = "select * from photos limit 1 offset " + str(r)
                    cur.execute(q)
                    row = cur.fetchone()
                    filename = row[1]
                    type = row[2]
                    title = row[3]
                    keywords = row[4]
                    description = row[5]
                
                    print("SERVER: filename is ", filename)
                    with open(filename, mode='rb') as photoFile: 
                        fileContent = photoFile.read()
        
                    # send to the client
                    b64Data = binascii.b2a_base64(fileContent)
                    str64Data = b64Data.decode('utf-8')
                    basename = os.path.basename(filename)
                    caption = ""
                    if len(title) > 0:
                        caption = caption + title + " : "
                    if len(description) > 0:
                        caption = caption + description
                    print ("TCDEBUG: caption is ", caption)
                    msg = json.dumps({"command": "DisplayPhoto",
                                      "basename": basename,
                                      "caption": caption,
                                      "data" : str64Data})
                    print("TCDEBUG: msg len is ", len(msg))
                    self.sendMessage(msg)
            elif self.data == "KillClient":
                print(str(datetime.datetime.now()), "KillClient msg received")
                ###self.sendMessage(self.data)
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
try:
    dbConn = psycopg2.connect("dbname=pframedb user=pframe")
except:
    print ("ERROR: unable to connect to database")
    sys.exit()

cur = dbConn.cursor()


server = SimpleWebSocketServer('', port, SendPhoto)
server.serveforever()
