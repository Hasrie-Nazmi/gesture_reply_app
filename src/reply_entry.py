import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
kv_path = os.path.join(ROOT_DIR, '..', 'ui', 'replyentry.kv')

Builder.load_file(kv_path)


class ReplyEntry(Screen):
    def go_back(self, instance):
        print("Going back to MainScreen!")
        self.manager.current = 'main_screen'

    def on_spinner_select(self, selected_text):
        """Triggered whenever a new option is chosen in the Spinner."""
        print(f"Selected gesture: {selected_text}")

        ASSETS_DIR = os.path.join(ROOT_DIR, '..', 'assets')
        gesture_map = {
            "Gesture 1": os.path.join(ASSETS_DIR, "gesture_one.jpg"),
            "Gesture 2": os.path.join(ASSETS_DIR, "gesture_two.jpg"),
            "Gesture 3": os.path.join(ASSETS_DIR, "gesture_three.jpg"),
            "Gesture 4": os.path.join(ASSETS_DIR, "gesture_four.jpg"),
            "Gesture 5": os.path.join(ASSETS_DIR, "gesture_five.jpg"),
            "Thumbs Up": os.path.join(ASSETS_DIR, "gesture_thumbs_up.jpg"),
            "Peace Sign": os.path.join(ASSETS_DIR, "gesture_peace_sign.jpg"),
            "Heart": os.path.join(ASSETS_DIR, "gesture_heart.jpg")
        }

        if selected_text in gesture_map:
            self.ids.gesture_img.source = gesture_map[selected_text]

    def on_button_click(self, instance):
        print("Button was pressed!")


class ReplyEntryApp(App):

    def build(self):
        self.title = "Gesture Reply"
        return ReplyEntry()


if __name__ == "__main__":
    ReplyEntryApp().run()
