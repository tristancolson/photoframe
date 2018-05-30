from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import sys
import datetime
import psycopg2
import random

port = int(sys.argv[1])
photoRootDir = "/Volumes/usbdrive1/photos"



class SendPhoto(WebSocket):

    def handleMessage(self):
        print (str(datetime.datetime.now()), "TCDEBUG handleMessage: ", self.data)

        # generate random number based on total photos
        cur.execute("select count(*) from photos")
        result = cur.fetchone()
        totalPhotos = result[0]
        print("TCDEBUG: there are ", totalPhotos, " photos")
        r = random.randint(1, totalPhotos)
        print("TCDEBUG: random num is ", r)

        # select that photo from the db
        q = "select * from photos limit 1 offset " + str(r)
        print("TCDEBUG: q is ", q)
        cur.execute(q)
        row = cur.fetchone()
        filename = row[1]
        type = row[2]
        
        print("TCDEBUG: filename is ", filename)
        print("TCDEBUG: type is ", type)
        with open(filename, mode='rb') as photoFile: 
            fileContent = photoFile.read()

        # send to the client
        self.sendMessage(fileContent)

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
