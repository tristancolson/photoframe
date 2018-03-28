import React, { Component } from 'react';

import Navbar from 'react-bootstrap/lib/Navbar';
import Nav from 'react-bootstrap/lib/Nav';
import NavItem from 'react-bootstrap/lib/NavItem';

var Config = require('Config');

export default function Footer() {
   var appVersion = Config.appversion;
   return (
      <div className="footerDiv" data-test="appVersion">
      PhotoFrame Version {appVersion}
      </div>
   );
}

