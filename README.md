
# Xiaomi Custom Doorbell 

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![homeassistant_community](https://img.shields.io/badge/HA%20community-forum-brightgreen)](https://community.home-assistant.io/) 

<a href="https://www.buymeacoffee.com/so3n" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

Turn a xiaomi smart button into a smart doorbell  🚪🔔

## Features
* Play one of the built in alerts on the xiaomi gateway or [customize your own](https://www.home-assistant.io/integrations/xiaomi_aqara/#services) when doorbell is pressed
* Supports sending a notification to your phone when doorbell is pressed
* Supports turning on a courtesy light (eg. porch light) when doorbell is pressed
* Supports flashing lights in your house to visually alert you when doorbell is pressed
* Supports Google Home voice prompt to alert you with a custom text-to-speech message

## Components Needed
* [Xiaomi Gateway](https://www.gearbest.com/living-appliances/pp_344667.html)
* [Xiaomi Wireless Button](https://www.gearbest.com/smart-home-controls/pp_009395405312.html?wid=1349303)

_Setting up in Home Assistant: [https://www.home-assistant.io/integrations/xiaomi_aqara/](https://www.home-assistant.io/integrations/xiaomi_aqara/)_

## Installing

Install via [HACS](https://hacs.xyz/). Alternatively, place the apps folder and its contents in your appdaemon folder.

## Configuration

### Configuration Values

| Variable       | Type       | Required | Default                       | Description                                                                                                                                                                                                                |
| -------------- | ---------- | -------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| module         | string     | True     |                               | Set to `xiaomi_doorbell`                                                                                                                                                                                                   |
| class          | string     | True     |                               | Set to `Doorbell`                                                                                                                                                                                                          |
| button         | string     | True     |                               | `entity_id` of the xiaomi button                                                                                                                                                                                           |
| gw_mac         | string     | True     |                               | The MAC address of your xiaomi gateway. Needs to be formatted without `:` eg. `34ce00880088`                                                                                                                               |
| click_type     | string     | False    | single                        | For buttons that support multiple click types (eg. single click, double click and long press) specify which one to trigger the doorbell. Valid options are `single`, `double` and `long_click_press`                       |
| ringtone_id    | integer    | False    | 10                            | The alert tone the gateway will play when button is pressed. Refer [here](https://www.home-assistant.io/integrations/xiaomi_aqara/#services) for valid values                                                              |
| volume         | integer    | False    | 10                            | Volume of the alert (0 - 100). Not needed if `volume_slider` option is used                                                                                                                                                |
| volume_slider  | string     | False    |                               | `entity_id` of an `input_number` component in home assistant to use as alert volume control                                                                                                                                |
| notify_html5   | boolean    | False    | `False`                       | Set to `True` for html5 push notifications to be received on chrome, firefox or android device. Requires `html5` component in home assistant. Refer [here](https://www.home-assistant.io/integrations/html5/) for details. |
| courtesy_light | dictionary | False    |                               | Use if you want a light to turn on when doorbell is pressed (eg. a porch light). In which, case specify an `entity_id` for the light and `timer` for duration of light to remain on in seconds. Refer to example above.    |
| flash          | list       | False    |                               | List of lights to flash to alert you that doorbell was pressed                                                                                                                                                             |
| gh_devices     | list       | False    |                               | List of google home entity id's to alert you with a voice prompt when doorbell is pressed                                                                                                                                  |
| gh_tts         | string     | False    | "There's someone at the door" | Text to speech message required for google home voice prompt                                                                                                                                                               |


### Example Usage

```yaml
Any_Description_You_Want:
  module: xiaomi_doorbell
  class: Doorbell
  button: binary_sensor.xiaomi_switch_3
  gw_mac: 34ce00880088
  ringtone_id: 10001
  volume_slider: input_number.doorbell_volume 
  notify_html5: True
  courtesy_light: 
    entity_id: light.front_porch
    timer: 180
  flash:
    - light.study
    - light.play_room
    - light.kitchen
    - light.dining
    - light.living_room
  gh_devices:
    - media_player.google_home_livingroom
    - media_player.google_home_bedroom
  gh_tts: "Doorbell pressed"
```

<hr/>

<a href="https://www.buymeacoffee.com/so3n" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
