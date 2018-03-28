import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';
import PhotoMain from './components/PhotoMain';

@inject("dataStore") @observer
export default class Photos extends Component {
  render() {
    return (
      <div>
       <PhotoMain />
     </div>
    );
  }
}

