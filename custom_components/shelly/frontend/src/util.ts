import { HomeAssistant } from "./hass/types"

export function SendWebSocketAction(
    hass: HomeAssistant,
    Type: string,
    Data: any = undefined
  ): void {
    let message: {
      [x: string]: any;
      type: string;
      action?: string;
      data?: any;
      id?: number;
    };
    message = {
        type: Type,
        data: Data
    };
    hass.connection.sendMessage(message);
  }