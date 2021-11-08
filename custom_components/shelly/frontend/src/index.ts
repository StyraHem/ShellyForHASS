//import './index.css';
import Panel from './panels/Panel';
import HassPanel from './panels/HassPanel';

customElements.define('shelly4hass-frontend', HassPanel(Panel));