var Config = require('config-js');
var pframeConfig = new Config('./pframe.config.js');
if (pframeConfig.get('auth.develmode')) {
   process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';  // REMOVE THIS
}
import express from 'express';
const router = express.Router();
var request = require('request');
var passport = require('passport');
var _ = require('lodash');
const auditLogOpts = {
                       logFilePath: pframeConfig.get('server.logname'),
                       timestampFormat: 'YYYY-MM-DD HH:mm:ss'
                     };
const auditLog = require('simple-node-logger').createSimpleFileLogger(auditLogOpts);

var bbm360apiUrl = pframeConfig.get('apis.bbm360apiurl');
var bbm360apiRequestKey = pframeConfig.get('apis.bbm360apirequestkey');

/**
  * testWebsocket
  */ 
router.get('/testWebsocket/', function(req, res) {
    console.log("TCDEBUG: server testWebsocket starting");
    res.json({status: "response from testWebsocket"});

}); // testWebsocket


/**
  * getRandomPhoto
  */ 
router.get('/getRandomPhoto/', function(req, res) {
    console.log("TCDEBUG: server getRandomPhoto starting");
    res.json({status: "response from getRandomPhoto"});

// res.json({status: "success", message: "All good from getInitialData", "syncServers": body.result.syncServers, "regions": body.result.regions, "clients": body.result.clients, "clientIndex": body.result.clientIndex});
}); // getRandomPhoto





export default router;
