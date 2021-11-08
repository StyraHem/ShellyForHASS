import { HomeAssistant } from "./hass/types"

export interface Instance {
  name : string,
  hass: HomeAssistant,
  instance_id : string,
  settings : Setting[],
  configs : Config[]
}

export interface Config {
  id : string,
  name : string,
  type : string,
  value : string,
  def : string
}

export interface Setting {
  id : string,
  name : string,
  image : string,
  value : {
    sensor : boolean,
    attrib: boolean,
    unit: string,
    div : Uint16Array,
    decimals: Uint8Array
  },
  has : {
    sensor : boolean,
    attrib : boolean,
    unit : boolean,
    div : boolean,
    decimals : boolean
  }
  default : {
    unit : string
  }
  changed : boolean
}

export interface App {
  hass: HomeAssistant
  instances: Instance[]
}

export const getConfiguration = async (hass: HomeAssistant) => {
  const response = await hass.connection.sendMessagePromise<App>({
    type: "s4h/get_config"
  });
  response.instances.map( i => { i.hass=hass })
  return response;
};
