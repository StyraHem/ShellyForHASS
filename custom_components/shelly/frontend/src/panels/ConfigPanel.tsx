import { App, Instance } from "../data";
import React, { Component } from 'react';
import ShellyConfigEntry from '../components/ConfigEntry'
import { Card, Col, Row } from "react-bootstrap";
import Masonry from "react-masonry-component";
import YamlInfo from "../components/YamlInfo"

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
    const groups = [...new Set(configs.map( config => config.group ))];
 
    return (<>
      <div className="configpanel">
        <h2>Config</h2>
        <YamlInfo instance={instance} />
        <Masonry
          elementType={'div'}
        >
        {groups.map( group => (
          <div className="group">
              <div className="title">{group}</div>
              {configs.filter( config => config.group==group).map( config => (                
                <Card key={config.id}>
                  <Card.Title>{config.title}</Card.Title>
                  <div className="desc">{config.desc}</div>
                  <div className="value">
                    <ShellyConfigEntry instance={instance} config={config} />
                  </div>
                </Card>
              ))}
            </div>
          ))}
        </Masonry>
      </div>
    </>);   
  }
}
