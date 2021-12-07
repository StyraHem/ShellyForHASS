import { Instance, Config } from "../data";
import { SendWebSocketAction } from "../util";
import React, { Component } from 'react';

interface Props {
  instance: Instance,
  config: Config
}

export default class ShellyConfigEntry extends Component<Props> {
  constructor(props) {
    super(props);
    this.update_config = this.update_config.bind(this);
  }
  public update_config(e) {
    const { config, instance } = this.props;
    let value = e?.target.type=="checkbox" ? 
        e?.target.checked : e?.target.value;
    SendWebSocketAction(instance.hass, "s4h/config", 
    {
      id : config.id,
      instanceid : instance.instance_id,
      value : value
    });
  }

  render_ctrl(config:Config) {

    if (config.type=="bool") {
      const val = config.value.toString().toLowerCase()=="true";
      return <input title={config.name} type="checkbox" checked={val} onChange={this.update_config}></input>
    }
    if (config.type=="str")
      return <input type="text" title={config.name}
        value={config.value}
        onChange={this.update_config}
      ></input>

    if (config.type=="txt")
      return <textarea title={config.name} rows={6}
              value={config.value}
              onChange={this.update_config}></textarea>

    if (config.type=="int")
      return <input type="number" title={config.name} 
        value={config.value}
        onChange={this.update_config}
      ></input>
     
      return <div>-</div>
    }

    render() {
      const { config, instance } = this.props;
      return <div className={config.type}>{this.render_ctrl(config)}</div>
    }
    
}
