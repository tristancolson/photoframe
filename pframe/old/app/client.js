console.log("TCDEBUG: app/client.js");
import React from 'react';
import { render } from 'react-dom';
import { Router, browserHistory } from 'react-router';
import routes from './routes';
const rootEl = document.getElementById('root');

render(
    <Router history={browserHistory}
      routes={routes}
    />,
  rootEl
);

