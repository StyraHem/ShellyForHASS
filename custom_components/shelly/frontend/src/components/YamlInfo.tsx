import React, { Component } from 'react';
import { Instance } from '../data';
import { SendWebSocketAction } from "../util";

interface Props {
    instance: Instance
}

export default class YamlInfo extends Component<Props> {
    constructor(props) {
        super(props);
        this.convert_config = this.convert_config.bind(this);
    }
    public convert_config(e) {
        const { instance } = this.props;
        SendWebSocketAction(instance.hass, "s4h/convert", 
        {
          instanceid : instance.instance_id
        });    
    }
    render() {
        const { instance } = this.props;
        const show = instance.yaml;
        if (!show)
            return null;
        return <div className="info">
            <p>
            Your settings for ShellyForHass is stored in config.yaml and can't be changed here.
            </p>
            <p>
            You can convert this instance to an integration stored in the database.
            If you do this you can change the settings here and settings in config.yaml will be ignored and you can remove them.            
            </p>
            <button value="Convert" onClick={this.convert_config}>Convert</button>
        </div>
    }    
}
