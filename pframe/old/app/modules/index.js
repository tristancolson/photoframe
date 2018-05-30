import React, { Component, cloneElement } from 'react';
import { Provider } from 'mobx-react';
import DevTools from 'mobx-react-devtools';
import Header from './Header';
import Footer from './Footer';
import 'bootstrap/dist/css/bootstrap.css';
import styles from './sharedStyles.css';
import {Grid, Row, Col, PageHeader} from 'react-bootstrap';
import dataStore from './dataStore';
import uiStore from './uiStore';


export default class App extends Component {

componentDidMount() {
    dataStore.initializePframe();
}

render() {
  return (
    <div>
      <Grid fluid={false}>
      <Row>
      <Col xs={12}>
      <Header />
      </Col>
      </Row>
      <Row>
      <Col xs={12}>
      <main role="main" className={styles.main}>
        <Provider {...{ dataStore, uiStore }}>
          {this.props.children}
        </Provider>
      </main>
      </Col>
      </Row>
      <Row>
      <Col xs={12}>
      <Footer />
      </Col>
      </Row>
      </Grid>
    </div>
  );
}

}
