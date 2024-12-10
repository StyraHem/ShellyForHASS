import { HomeAssistant } from "./hass/types"

export interface Instance {
  name : string,
  yaml: boolean,
  hass: HomeAssistant,
  instance_id : string,
  settings : Setting[],
  configs : Config[],
  blocks : Blocks[]
}

export interface Blocks {
  id : string,
  name : string
  room: string,
  type: string,
  img: string,
  devices : Device[]
}

export interface Device {
  id : string,
  name : string,
  state: string
}

export interface Config {
  id : string,
  title : string,
  desc: string,
  group: string,
  type : string,
  value : string,
  def : string
}

export interface Setting {
  id : string,
  title : string,
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
    type: "s4h/get_config",
    language: hass.language
  });
  response.instances.map( i => { i.hass=hass })
  return response;
};
