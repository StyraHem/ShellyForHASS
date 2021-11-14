import { App, Instance } from "../data";
import React, { Component } from 'react';
import ShellyConfigEntry from '../components/ConfigEntry'
import { Card, Col, Row } from "react-bootstrap";
import Masonry from "react-masonry-component";

interface Props {
  app?: App,
  instance?: Instance
}

export default class ShellyConfigPanel extends Component<Props> {
  render() {
    if (!this.props.instance) 
      return <div>Loading!!!!!!</div>;
    const { app, instance } = this.props;
    const { configs } = instance;
    return (<>
      <div className="configpanel">
        <h2>Config</h2>
        <Masonry
          elementType={'div'}
        >
          {configs.map( config => (
            <Card key={config.id}>
              <div className="name">{config.name}</div>
              <div className="value">
                <ShellyConfigEntry instance={instance} config={config} />
              </div>
            </Card>
          ))}
        </Masonry>
      </div>
    </>);   
  }
}
