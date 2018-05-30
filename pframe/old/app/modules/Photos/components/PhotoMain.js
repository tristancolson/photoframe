import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';
import styles from '../../sharedStyles.css';
import { subscribeToPhoto } from '../../api';
import windowSize from 'react-window-size';
var Link = require('react-router').Link;
var _ = require('lodash');

@inject('dataStore', 'uiStore') @observer
export default class PhotoMain extends Component {

constructor(props) {
console.log(new Date() + "  TCDEBUG: PhotoMain constructor starting");
    super(props);
    console.log(new Date() + "  TCDEBUG: before subscribeToPhoto");
    subscribeToPhoto((err, photoContents) => this.setState({photoContents}));
} // constructor

state = {
    photoContents: 'no photo yet'
};

render() {
console.log(new Date() + " TCDEBUG: PhotoMain render:  " + JSON.stringify(this.state.photoContents.filename));

//console.log("TCDEBUG: photo width is " + this.state.photoContents.width);
//console.log("TCDEBUG: photo height is " + this.state.photoContents.height);
//console.log("TCDEBUG: window innerWidth is " + window.innerWidth);
//console.log("TCDEBUG: window innerHeight is " + window.innerHeight);
//    if (this.state.photoContents.width / window.innerWidth > this.state.photoContents.height / window.innerHeight) {
//    }
//    else {
//
//    }


    return (
        <div>
        <img id="photo" src={"data:image/jpeg;base64," + this.state.photoContents.photoData}/>
        </div>
    );

} // render


}
