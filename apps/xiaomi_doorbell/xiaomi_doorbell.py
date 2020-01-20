"""
Turn a xiaomi smart button into a smart doorbell 🚪🔔
https://github.com/so3n/Appdaemon-Xiaomi-Doorbell
"""

import appdaemon.plugins.hass.hassapi as hass
import time

# default values
DEFAULT_CLICK_TYPE = "single"
DEFAULT_RINGTONE_ID = 10
DEFAULT_COURTESY_LIGHT_TIMER = 60
DEFAULT_NOTIFY_HTML5 = False
DEFUALT_DOORBELL_VOLUME = 10
DEFAULT_GH_TTS = "There's someone at the door"

class Doorbell(hass.Hass):

    def initialize(self):
        self.button = self.args.get("button")
        self.click_type = self.args.get("click_type", DEFAULT_CLICK_TYPE)
        self.gw_mac = self.args.get("gw_mac")
        self.ringtone_id = self.args.get("ringtone_id", DEFAULT_RINGTONE_ID)
        self.volume = self.args.get("volume", DEFUALT_DOORBELL_VOLUME)
        self.volume_slider = self.args.get("volume_slider")
        self.flash = self.args.get("flash")
        self.courtesy_light = self.args.get("courtesy_light")
        self.gh_devices = self.args.get("gh_devices")
        self.notify_html5 = self.args.get("notify_html5", DEFAULT_NOTIFY_HTML5)
        self.gh_tts = self.args.get("gh_tts", DEFAULT_GH_TTS)

        # listener for when doorbell is pressed
        self.listen_event(self.cb_doorbell, "xiaomi_aqara.click",
                        entity_id = self.button)
        
        # listener for when volume slider changes
        if self.volume_slider:
            self.listen_state(self.doorbell_slider_change, self.volume_slider)

    def cb_doorbell(self, event_name, data, kwargs):
        """ Callback function when doorbell button is pressed"""

        event_click = data["click_type"]
        button = kwargs["entity_id"]
        
        self.log(f"Xiaomi Button {button} pressed") 

        if event_click != self.click_type:
            return   

        # Turn on courtesy light if enabled and after sunset
        if self.courtesy_light and self.sun_down():
            light = self.courtesy_light.get("entity_id")
            timer = self.courtesy_light.get("timer")

            self.turn_on(light)
            self.run_in(self.cb_delayed_off, timer, 
                        device = light)

        # Play alert if someone is home
        if self.anyone_home():
            if self.volume_slider:
                vol = float(self.get_state(self.volume_slider))
            else:
                vol = self.volume

            if vol > 0:
                self.call_service("xiaomi_aqara/play_ringtone", 
                                gw_mac = self.gw_mac,
                                ringtone_id = self.ringtone_id,
                                ringtone_vol = vol)
        
        # Flash lights if enabled
        if self.flash:
            if type(self.flash) is list:
                lights = self.flash
            else:
                lights = [self.flash]

            for x in lights: 
                self.flash_bulb(x, 3)

        # Google Home voice prompt if enabled
        if self.gh_devices and self.anyone_home():
            if type(self.gh_devices) is list:
                ggl_homes = self.gh_devices
            else:
                ggl_homes = [self.gh_devices]

            for gh in ggl_homes:
                if self.get_state(gh) == "off": 
                    self.call_service("tts/google_say", entity_id = gh,
                                      message = self.gh_tts)

        # Send notification if enabled
        if self.notify_html5:
            t = time.strftime("%d-%b-%Y %H:%M:%S")
            message = f"{t}: Doorbell pressed"
            self.log(message)
            self.notify(message, name = "html5")
    
    def doorbell_slider_change(self, entity, attribute, old, new, kwargs):
        """ Callback function for when volume slider changes value """

        vol = float(new)
        if vol > 0:
            self.call_service("xiaomi_aqara/play_ringtone", 
                                gw_mac = self.gw_mac,
                                ringtone_id = self.ringtone_id, 
                                ringtone_vol = vol)
    
    def cb_delayed_off(self, kwargs):
        """ Callback function to use with self.run_in() to turn off a device """

        device = kwargs["device"]
        self.turn_off(device)

    def flash_bulb(self, light, seconds):
        """ Flash light for given number of seconds """
        
        self.turn_on(light, flash = "long")
        self.run_in(self.cb_delayed_off, seconds, device = light)
        