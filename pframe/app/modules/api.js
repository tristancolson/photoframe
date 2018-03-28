import openSocket from 'socket.io-client';
const socket = openSocket('http://192.168.4.99:8000');

function subscribeToPhoto(cb) {
    socket.on('photo', photoContents => cb(null, photoContents));
    socket.emit('subscribeToPhoto', 20000);
}


export {subscribeToPhoto};


