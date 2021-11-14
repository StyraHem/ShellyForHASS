import { App, Instance } from "../data";
import React, { Component } from 'react';
import Checkbox from '../components/setting/Checkbox'
import TextField from '../components/setting/TextField'
import { Card } from "react-bootstrap";
import Masonry from "react-masonry-component";

interface Props {
  app?: App,
  instance: Instance
}
export default class ShellySettingPanel extends Component<Props> {
 
  render() {
    const { instance } = this.props
    return (<div className="settingpanel">
      <h2>Settings</h2>
      <Masonry
        elementType={'div'}
      >
        {instance.settings.map( setting => (
          <Card key={setting.id}>
            <div className="name">{setting.name}</div>
            Show:&nbsp;
            <Checkbox instance={instance} setting={setting} param="sensor"></Checkbox>
            <Checkbox instance={instance} setting={setting} param="attrib"></Checkbox>
            <TextField instance={instance} setting={setting} param="decimals" type="number"></TextField>
            <TextField instance={instance} setting={setting} param="div" type="number"></TextField>
            <TextField instance={instance} setting={setting} param="unit" type="text"></TextField>
          </Card>
        ))}
      </Masonry>
    </div>
    );
  }
}
