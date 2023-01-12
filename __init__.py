import json

from mycroft import MycroftSkill, intent_file_handler

import epaper_display as epd

DEBUG = True


class ScreenSelector(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self._display = epd.DisplayManager(
            epd.DisplaySizes.SevenInchFiveHD, debug_mode=DEBUG
        )
        self._config = {}
        with open("/home/benpac/epaperdisplay/config/config.json") as f:
            self._config = json.load(f)

    @intent_file_handler("selector.screen.intent")
    def handle_selector_screen(self, message):
        screen_name = message.data.get("screen_name")

        self.speak_dialog("selector.screen", data={"screen_name": screen_name})

        if "calendar" in screen_name:
            self._display.display(
                epd.CalendarScreen().create_image(
                    self._display.size,
                    epd.GoogleCalendarService(config=self._config["calendar"]),
                )
            )

        if "quote" in screen_name:
            self._display.display(
                epd.QuoteScreen().create_image(
                    self._display.size, epd.QuotableService({})
                )
            )


def create_skill():
    return ScreenSelector()
