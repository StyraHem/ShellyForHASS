import React, { Component } from 'react';
import { HomeAssistant } from "../hass/types"
import ShellyConfigPanel from './ConfigPanel'
import ShellySettingPanel from './SettingPanel'
//import ShellyDocPanel from './DocPanel'
import ShellyNavbar from '../components/Navbar'
import {App, getConfiguration} from '../data'
import { Navigate } from 'react-router-dom';
import './Panel.scss';
import {
  BrowserRouter as Router,
  Route,
  Routes,
  RouteMatch
} from 'react-router-dom';

interface Props {
  hass: HomeAssistant,
  showMenu: boolean,
  narrow: boolean,
  panel: any
}

interface State {
  app?: App;
} 

class Panel extends Component<Props, State> {
  private async updateConfiguration() {
    const { hass } = this.props;
    getConfiguration(hass)
      .then( (resp) => {
        this.setState(
          {app: {instances: resp.instances, hass:hass}}
        )
      })
  }
  componentDidMount () {
    const { hass } = this.props;
    hass.connection.subscribeEvents(
      () => this.updateConfiguration(),
      "s4h/config_updated"
    );

    getConfiguration(this.props.hass).then( resp => {
      this.setState({app: {instances: resp.instances, hass:this.props.hass}});
    })
  }
  render() {
    /* eslint-disable no-unused-vars */
    const { hass, panel, showMenu, narrow } = this.props;
    /* eslint-enable no-unused-vars */    
    if (!this.state?.app)
      return <div>Loading...</div>;
    var instance = this.state.app?.instances[0];
    return (<Router basename="/shelly">
      <div className="Panel">
        <ShellyNavbar narrow={narrow}></ShellyNavbar>
        <div className="Container">
          <Routes>
            {/* <Route index element={<div>Comming soon!</div>} /> */}
            <Route path="*" element={<Navigate to="/config" />} />
            <Route path="/config" element={<ShellyConfigPanel app={this.state.app} instance={instance}></ShellyConfigPanel> } />
            <Route path="/settings" element={<ShellySettingPanel app={this.state.app} instance={instance}></ShellySettingPanel> } />
            {/* <Route path="/readme" element={<ShellyDocPanel></ShellyDocPanel> } /> */}
          </Routes>
        </div>
      </div>
      </Router>
    );
  }
}

export default Panel;