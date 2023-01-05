from mycroft import MycroftSkill, intent_file_handler


class ScreenSelector(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('selector.screen.intent')
    def handle_selector_screen(self, message):
        screen_name = message.data.get('screen_name')

        self.speak_dialog('selector.screen', data={
            'screen_name': screen_name
        })


def create_skill():
    return ScreenSelector()

