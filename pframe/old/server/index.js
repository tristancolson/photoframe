console.log(new Date() + "  TCDEBUG: server/index.js");
var path = require('path');
var babelConfig = require('../package').babelConfig.server;

require('babel-register')(babelConfig);
require('babel-polyfill');
require('./server.js');
