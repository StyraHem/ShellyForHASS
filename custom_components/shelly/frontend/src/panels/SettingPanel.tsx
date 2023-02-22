import { App, Instance } from "../data";
import React, { Component } from 'react';
import Checkbox from '../components/setting/Checkbox'
import TextField from '../components/setting/TextField'
import { Card } from "react-bootstrap";
//import Masonry from "react-masonry-component";
import YamlInfo from "../components/YamlInfo"
interface Props {
  app?: App,
  instance: Instance
}
export default class ShellySettingPanel extends Component<Props> {
 
  render() {
    const { instance } = this.props
    return (<div className="settingpanel">
      <h2>Settings</h2>
        <YamlInfo instance={instance}/>
        {instance.settings.map( setting => (
          <Card key={setting.id}>
            <Card.Title>{setting.title}</Card.Title>
            <div className="label">show:</div>
            <Checkbox instance={instance} setting={setting} param="sensor"></Checkbox>
            <Checkbox instance={instance} setting={setting} param="attrib"></Checkbox>
            <TextField instance={instance} setting={setting} param="decimals" type="number"></TextField>
            <TextField instance={instance} setting={setting} param="div" type="number"></TextField>
            <TextField instance={instance} setting={setting} param="unit" type="text"></TextField>
          </Card>
        ))}
    </div>
    );
  }
}
