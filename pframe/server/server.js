var Config = require('config-js');
var pframeConfig = new Config('./pframe.config.js');
const { Client } = require('pg');
import path from 'path';
import express from 'express';
import bodyParser from 'body-parser';
var fs = require('fs');
var http = require('http');



const app = express();
const dbConnString = "postgresql://pframe:foobar@localhost:5432/pframedb";
const dbConn = new Client({connectionString: dbConnString});
dbConn.connect();

var io = require('socket.io')();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));


app.use(express.static(path.join(__dirname, 'public')));

import api from './api/';
app.use('/api/', api);

app.get('*', function(request, response) {
    response.sendFile(path.resolve(__dirname, 'public', 'index.html'))
})

var totalPhotos;
dbConn.query('select count(*) from photos', (err, res) => {
    if (err) {
        console.log("TCDEBUG: count err is " + err);
    }
    else {
        totalPhotos = res.rows[0]["count"];
console.log("TCDEBUG: totalPhotos is " + totalPhotos);
    }
});

io.on('connection', (client) => {
    console.log("TCDEBUG: server io.on connection");
    client.on('subscribeToPhoto', (interval) => {
        setInterval(() => {
            const randomNum = Math.floor(Math.random() * Math.floor(totalPhotos));
            console.log("TCDEBUG: randomNum = " + randomNum);
            dbConn.query('select * from photos limit 1 offset ' + randomNum, (err, res) => {
                if (err) {
                    console.log("TCDEBUG: select err is " + err);
                }
                else {
                    const row = res.rows[0];
                    console.log("TCDEBUG: select res " + JSON.stringify(res.rows[0]));

                    const filename = row.filename;
                    const width = row.width;
                    const height = row.height;
                    console.log("TCDEBUG: filename is " + filename);
                    console.log("TCDEBUG: size of file is " + fs.statSync(filename).size);

                    var photoContents = fs.readFileSync(filename);            
                    console.log("TCDEBUG: length of photoContents is " + photoContents.length);
                    var encodedData = new Buffer(photoContents).toString('base64');
                    console.log("TCDEBUG: length of encodedData is " + encodedData.length);
                    var responseData = new Object();
                    responseData.photoData = encodedData;
                    responseData.filename = filename;
                    responseData.width = width;
                    responseData.height = height;
                    responseData.type = 'jpg';
                    // res.json(responseData);
                    // client.emit('photo', responseData);
                }
            });
       //     client.emit('timer', new Date());
        }, interval);
    });
});


const serverPort = pframeConfig.get('server.port');
http.createServer(app).listen(serverPort);
const socketPort = 8000;
io.listen(socketPort);


