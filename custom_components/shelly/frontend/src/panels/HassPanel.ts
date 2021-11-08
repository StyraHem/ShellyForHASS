import React from 'react';
import ReactDOM from 'react-dom';
import { HomeAssistant } from "../hass/types"


// Small helper function to generate custom elements that will render the passed
// in React component and forwards the Home Assistant panel properties.
export default HassPanel => class extends HTMLElement {
  private _renderScheduled: any;
  private _hass!: HomeAssistant;
  private _showMenu!: boolean;
  private _narrow!: boolean;
  private _panel: any;
  
  constructor() {
    super();
    this._renderScheduled = null;

    // Initialize properties as `null` and create setters that triggers a render
    const props = {};
    ['hass', 'showMenu', 'narrow', 'panel'].forEach((prop) => {
      const key = `_${prop}`;
      this[key] = null;
      props[prop] = {
        set(value) {
          this[key] = value;
          this._render();
        }
      }
    });
    Object.defineProperties(this, props);
  }

  disconnectedCallback() {
    ReactDOM.unmountComponentAtNode(this);
  }

  _render() {
    if (this._renderScheduled !== null) return;

    this._renderScheduled = Promise.resolve().then(() => {
      this._renderScheduled = null;
      ReactDOM.render(React.createElement(HassPanel, {
        hass: this._hass,
        showMenu: this._showMenu,
        narrow: this._narrow,
        panel: this._panel,
      }), this);
    });
  }
}