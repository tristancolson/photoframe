from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import sys
import datetime
import psycopg2
import random

port = int(sys.argv[1])
photoRootDir = "/Volumes/usbdrive1/photos"



class SendPhoto(WebSocket):

    def handleMessage(self):
        print("SERVER: handleMessage starting")
        try:
            if self.data == "SendPhoto":
                print(str(datetime.datetime.now()), " SERVER: SendPhoto message");
                # generate random number based on total photos
                cur.execute("select count(*) from photos")
                result = cur.fetchone()
                totalPhotos = result[0]
                r = random.randint(1, totalPhotos)
        
                # select that photo from the db
                q = "select * from photos limit 1 offset " + str(r)
    ###            print("SERVER: q is ", q)
                cur.execute(q)
                row = cur.fetchone()
                filename = row[1]
                type = row[2]
                
                print("SERVER: filename is ", filename)
                with open(filename, mode='rb') as photoFile: 
                    fileContent = photoFile.read()
        
                # send to the client
                print("SERVER: before sendMessage")
                self.sendMessage(fileContent)
                print("SERVER: after sendMessage")
            else:
                print(str(datetime.datetime.now()), "CLIENT  message ", self.data)
        except Exception as e:
            print("SERVER: exception: " , e)
            os.kill(os.getPid(), signal.SIGTERM)
        else:
            print("SERVER: completed handleMessage")


    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


try:
    dbConn = psycopg2.connect("dbname=pframedb user=pframe")
except:
    print ("ERROR: unable to connect to database")
    sys.exit()

cur = dbConn.cursor()


server = SimpleWebSocketServer('', port, SendPhoto)
server.serveforever()
