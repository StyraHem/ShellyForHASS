import { App, Instance } from "../data";
import React, { Component } from 'react';
import Checkbox from '../components/setting/Checkbox'
import TextField from '../components/setting/TextField'
import { Card } from "react-bootstrap";
//import Masonry from "react-masonry-component";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPowerOff, faToggleOn, faToggleOff } from '@fortawesome/free-solid-svg-icons'

import YamlInfo from "../components/YamlInfo"
interface Props {
  app?: App,
  instance: Instance
}
export default class ShellyBlockPanel extends Component<Props> { 
  render() {
    const { instance } = this.props
    return (<div className="devicepanel">
      <h2>Devices</h2>
        <YamlInfo instance={instance}/>
        {instance.blocks.map( block => (
          <Card key={block.id}>
            <Card.Title>{block.name}
              <Card.Img src={"https://control.shelly.cloud/images/device_images/" + block.img + ".png"} className="img" />
            
            </Card.Title>
            <Card.Subtitle>
              {block.id}
            </Card.Subtitle>
            <div>Room: {block.room}</div>
            <div>Type: {block.type} {block.img}</div>
            <div>
            {block.devices.map( device => {
              var cls = "device " + device.name.toLowerCase();
              if (device.name=="RELAY") {
                cls += " " + (device.state ? "on" : "off");
                return <div className={cls}>
                  <FontAwesomeIcon icon={faPowerOff}></FontAwesomeIcon>
                </div>
              }
              else if (device.name=="SWITCH") {
                cls += " " + (device.state ? "on" : "off");
                return <div className={cls}>                  
                  <FontAwesomeIcon icon={device.state ? faToggleOn : faToggleOff}></FontAwesomeIcon>
                </div>
              }
              else if (device.name=="POWERMETER") {
                cls += " " + (device.state!="0" ? "on" : "off");
                return <div className={cls}>
                  {device.state}W
                </div>
              }
              else if (device.name=="SENSOR") {
                cls += " " + (device.state!="0" ? "on" : "off");
                return <div className={cls}>
                  {device.state}
                </div>
              } else {
                return <div className="device" title={device.name}>{device.state}</div>
              }
            })}
            </div>
          </Card>
        ))
      }
    </div>
    );
  }
}
