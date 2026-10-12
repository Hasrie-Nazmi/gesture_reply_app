import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from main_screen import MainScreen
from reply_entry import ReplyEntry

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(ROOT_DIR, '..', 'ui')

Builder.load_file(os.path.join(UI_DIR, 'mainscreen.kv'))
Builder.load_file(os.path.join(UI_DIR, 'replyentry.kv'))


class MainApp(App):
    def build(self):
        self.title = "Gesture Reply"

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(ReplyEntry(name='reply_screen'))

        return sm


if __name__ == "__main__":
    MainApp().run()
