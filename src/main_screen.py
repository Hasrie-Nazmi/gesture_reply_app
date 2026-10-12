import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
kv_path = os.path.join(ROOT_DIR, '..', 'ui', 'mainscreen.kv')

Builder.load_file(kv_path)


class MainScreen(Screen):

    def on_button_click(self, instance):
        print("Button was pressed!")
        self.manager.current = 'reply_screen'


class MainScreenApp(App):

    def build(self):
        self.title = "Gesture Reply"
        return MainScreen()


if __name__ == "__main__":
    MainScreenApp().run()
