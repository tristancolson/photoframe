console.log(new Date() + "  TCDEBUG: api.js starting");
import openSocket from 'socket.io-client';
const socket = openSocket('http://192.168.4.99:8000');
console.log(new Date() + "  TCDEBUG: socket opened");

function subscribeToPhoto(cb) {
console.log(new Date() + "  TCDEBUG: subscribeToPhoto started");
    socket.on('photo', photoContents => cb(null, photoContents));
    socket.emit('subscribeToPhoto', 20000);
}


export {subscribeToPhoto};


