import os
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from gesture_processor import GestureCameraProcessor

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
kv_path = os.path.join(ROOT_DIR, '..', 'ui', 'mainscreen.kv')

Builder.load_file(kv_path)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.processor = GestureCameraProcessor()

        self.gesture_replies = {
            "Gesture 0": "",
            "Gesture 1": "",
            "Gesture 2": "",
            "Gesture 3": "",
            "Gesture 4": "",
            "Gesture 5": "",
        }

        self.import_config_from_json()

        self.current_text = ""
        self.copied_text = []

    def on_enter(self, *args):
        """Triggered automatically when entering the MainScreen."""
        self.import_config_from_json()

        self.processor.start_camera(0)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

    def on_leave(self, *args):
        """Triggered when leaving the screen to free up the webcam."""
        self.processor.stop_camera()
        Clock.unschedule(self.update_frame)

    def update_frame(self, dt):
        """Delegates frame processing and updates UI texture."""
        texture, detected = self.processor.process_frame(
            callback_on_gesture=self.handle_detected_gesture)
        if texture:
            self.ids.cam_image.texture = texture

    def handle_detected_gesture(self, gesture_name):
        """Callback triggered when a gesture is recognized."""
        key_mapping = {
            "gest_0": "Gesture 0",
            "gest_1": "Gesture 1",
            "gest_2": "Gesture 2",
            "gest_3": "Gesture 3",
            "gest_4": "Gesture 4",
            "gest_5": "Gesture 5",
        }

        dict_key = key_mapping.get(gesture_name, gesture_name)
        reply_message = self.gesture_replies.get(dict_key, "")

        print(
            f"Gesture Detected: {gesture_name} (Mapped to: {dict_key}) -> Reply: {reply_message}")

        self.ids.gesture_label.text = f"{dict_key}: {reply_message}"
        self.current_text = reply_message

    def import_config_from_json(self, filepath="config.json"):
        """Imports gesture replies from the local JSON config file."""
        if not os.path.exists(filepath):
            print(f"Config file {filepath} not found. Using default replies.")
            return False

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

                if isinstance(loaded_data, dict):
                    self.gesture_replies.update(loaded_data)
                    print(
                        f"Successfully imported configuration from {filepath}")
                    return True
                else:
                    print(
                        "Error: Invalid JSON format (root element must be a dictionary).")
                    return False
        except Exception as e:
            print(f"Failed to import config: {e}")
            return False

    def go_back(self, instance):
        print("Going back to MainScreen!")
        self.manager.current = 'main_screen'

    def on_button_click(self, instance):
        print("Button was pressed!")
        self.manager.current = 'reply_screen'

    def copy_text(self):
        if self.current_text:
            self.copied_text.append(self.current_text)
            print(self.copied_text)
            self.ids.reply_display_box.text = "\n".join(self.copied_text)

    def del_prev_text(self):
        if self.copied_text:
            self.copied_text.pop()
            print(self.copied_text)
            self.ids.reply_display_box.text = "\n".join(self.copied_text)

    def clear_text(self):
        self.copied_text = []
        print(self.copied_text)
        self.ids.reply_display_box.text = ""


class MainScreenApp(App):
    def build(self):
        self.title = "Gesture Reply"
        return MainScreen()


if __name__ == "__main__":
    MainScreenApp().run()
