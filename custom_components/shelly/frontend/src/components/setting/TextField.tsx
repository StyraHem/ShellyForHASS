import React, { Component } from "react";
import { Instance, Setting } from "../../data";
import { SendWebSocketAction } from "../../util";

interface Props {
  instance: Instance,
  setting: Setting,
  param: string,
  type: string
}

export default class SettingTextField extends Component<Props> {
  public constructor(props) {
    super(props)
    this.update_setting=this.update_setting.bind(this)
  }

  public update_setting(e) {
    let value = e.target.value;
    const { setting, param, instance } = this.props;
    SendWebSocketAction(instance.hass, "s4h/setting", 
    {
      id : setting.id,
      instanceid : instance.instance_id,
      param : param,
      value : value
    });
  }

  render() {
    const { setting, param, type, instance } = this.props;
    const readonly = instance.yaml;    
    return <div className={param}>
        {setting.has[param] ? 
          <><div className="label">{param}: </div>
          <input type={type} title={setting.title} className={type}
            disabled={readonly}
            value={setting.value[param]} 
            placeholder={"Default: " + setting.default[param]}
            onChange={this.update_setting} /></>
          : ""}
      </div>
  }
}
// import {
//   LitElement,
//   TemplateResult,
//   html,
//   customElement,
//   property
// } from "lit-element";
// //import { HomeAssistant }
// //  from "home-assistant-frontend/src/types"
// import { Instance, Setting } from "../../data";
// import '@material/mwc-textfield';
// import { SendWebSocketAction } from "../../util";

// @customElement("shelly-setting-textfield")
// export class ShellySettingTextfield extends LitElement {
//   @property() public instance!: Instance;
//   @property() public setting!: Setting;
//   @property() public param!: string;
//   @property() public type!: string;

//   public update_setting(e) {
//     let value = e.target.value;
//     SendWebSocketAction(this.instance.hass, "s4h/setting", 
//     {
//       id : this.setting.id,
//       instanceid : this.instance.instance_id,
//       param : this.param,
//       value : value
//     });
//   }

//   protected render(): TemplateResult | void {
//     return html`
//       ${this.setting.has[this.param] ? 
//         html`<mwc-textfield
//           .placeholder=${"Default: " + this.setting.default[this.param]}
//           .value=${this.setting.value[this.param]}
//           @change=${this.update_setting}>
//         >
//         </mwc-textfield>` : ""}
//     `;
//   }
// }

