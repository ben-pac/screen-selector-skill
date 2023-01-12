import json
import os.path

from mycroft import MycroftSkill, intent_file_handler

import epaper_display as epd

DEBUG = True


class ScreenSelector(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self._display = epd.DisplayManager.from_config(
            {
                "debug": True,
                "model": "SevenInchFiveHD",
                "debug_screen_path": "/home/benpac/mycroft_screen.png",
            }
        )
        self._config = {}
        with open(os.path.expanduser("~/.config/epaperdisplay/config.json")) as f:
            self._config = json.load(f)

    @intent_file_handler("selector.screen.intent")
    def handle_selector_screen(self, message):
        screen_name = message.data.get("screen_name")

        if "calendar" in screen_name:
            self._display.display(
                epd.CalendarScreen().create_image(
                    self._display.size,
                    epd.GoogleCalendarService(config=self._config["calendar"]),
                )
            )
        elif "quote" in screen_name:
            self._display.display(
                epd.QuoteScreen().create_image(
                    self._display.size, epd.QuotableService({})
                )
            )
        elif "countdown" in screen_name:
            self._display.display(
                epd.CountdownScreen().create_image(
                    self._display.size,
                    epd.CountdownFromConfigurationService(
                        config=self._config["countdown"]
                    ),
                )
            )
        elif "weather" in screen_name:
            self._display.display(
                epd.WeatherScreen().create_image(
                    self._display.size,
                    epd.SrfWeatherService(config=self._config["weather"]),
                )
            )
        else:
            self.speak_dialog("not.found", data={"screen_name": screen_name})
            return

        self.speak_dialog("selector.screen", data={"screen_name": screen_name})


def create_skill():
    return ScreenSelector()
