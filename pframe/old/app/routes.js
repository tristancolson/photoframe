import React from 'react';
import { Route, IndexRoute, IndexRedirect } from 'react-router';

import App from './modules';
import Photos from './modules/Photos';

export default (
  <Route path="/" component={App}>
    <IndexRedirect to='Photos' />
    <Route path="photos" component={Photos} />
  </Route>
);
