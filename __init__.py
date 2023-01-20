import json
import os.path
import time

from mycroft import MycroftSkill, intent_handler

import epaper_display as epd

DEBUG = True


class ScreenSelector(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self._config = {}
        with open(os.path.expanduser("~/.config/epaperdisplay/config.json")) as f:
            self._config = json.load(f)
        self._display = epd.DisplayManager.from_config(
            self._config.get(
                "display",
                {
                    "model": "SevenInchFiveHD",
                },
            )
        )

    @intent_handler("new.quote.intent")
    def handle_new_quote(self, message):
        service = epd.QuotableService({})
        service.get_quote(force_new=True)
        self._display.display(
            epd.QuoteScreen().create_image(self._display.size, service)
        )

    @intent_handler("read.quote.intent")
    def handle_read_quote(self, message):
        service = epd.QuotableService({})
        quote = service.get_quote()
        self.speak(quote.text)
        time.sleep(0.5)
        self.speak(quote.author)

    @intent_handler("selector.screen.intent")
    def handle_selector_screen(self, message):
        screen_name = message.data.get("screen_name")
        if "calendar" in screen_name:
            screen = epd.CalendarScreen()
            service = epd.GoogleCalendarService(config=self._config["calendar"])
        elif "quote" in screen_name:
            screen = epd.QuoteScreen()
            service = epd.QuotableService({})
        elif "countdown" in screen_name:
            screen = epd.CountdownScreen()
            service = epd.CountdownFromConfigurationService(
                config=self._config["countdown"]
            )
        elif "weather" in screen_name:
            screen = epd.WeatherScreen()
            service = epd.SrfWeatherService(config=self._config["weather"])
        else:
            self.speak_dialog("not.found", data={"screen_name": screen_name})
            return
        self.speak_dialog("selector.screen", data={"screen_name": screen_name})
        screen.create_image(self._display.size, service)


def create_skill():
    return ScreenSelector()
