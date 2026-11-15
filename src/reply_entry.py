import os
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
kv_path = os.path.join(ROOT_DIR, '..', 'ui', 'replyentry.kv')

Builder.load_file(kv_path)


class ReplyEntry(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.gesture_replies = {
            "Gesture 0": "",
            "Gesture 1": "",
            "Gesture 2": "",
            "Gesture 3": "",
            "Gesture 4": "",
            "Gesture 5": "",
        }

    def on_enter(self, *args):
        """Triggered automatically when entering the ReplyEntry screen."""

        self.import_config_from_json()

    def go_back(self, instance):
        print("Going back to MainScreen!")
        self.manager.current = 'main_screen'

    def on_spinner_select(self, selected_text):
        """Triggered when the user changes the spinner selection."""
        print(f"Selected gesture: {selected_text}")
        ASSETS_DIR = os.path.join(ROOT_DIR, '..', 'assets')

        gesture_map = {
            "Gesture 0": os.path.join(ASSETS_DIR, "gesture_zero.jpg"),
            "Gesture 1": os.path.join(ASSETS_DIR, "gesture_one.jpg"),
            "Gesture 2": os.path.join(ASSETS_DIR, "gesture_two.jpg"),
            "Gesture 3": os.path.join(ASSETS_DIR, "gesture_three.jpg"),
            "Gesture 4": os.path.join(ASSETS_DIR, "gesture_four.jpg"),
            "Gesture 5": os.path.join(ASSETS_DIR, "gesture_five.jpg"),
        }

        if selected_text in gesture_map and os.path.exists(gesture_map[selected_text]):
            self.ids.gesture_img.source = gesture_map[selected_text]

        if selected_text in self.gesture_replies:
            self.ids.reply_input.text = self.gesture_replies[selected_text]

    def set_reply(self):
        """Saves the current text input into the dictionary and exports to JSON."""
        gest = self.ids.spinner_gestures.text
        reply = self.ids.reply_input.text

        if gest in self.gesture_replies:
            self.gesture_replies[gest] = reply
            print(f"Updated {gest} -> {reply}")
            self.export_config_to_json()
        else:
            print(
                f"Error: Selected gesture '{gest}' not found in dictionary keys.")

    def export_config_to_json(self, filepath="config.json"):
        """Exports the current gesture replies dictionary to a local JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.gesture_replies, f,
                          indent=4, ensure_ascii=False)
            print(f"Successfully exported configuration to {filepath}")
            return True
        except Exception as e:
            print(f"Failed to export config: {e}")
            return False

    def import_config_from_json(self, filepath="config.json"):
        """Imports gesture replies from a local JSON file and updates the current configuration."""
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

                    if hasattr(self, 'ids') and 'spinner_gestures' in self.ids:
                        current_gest = self.ids.spinner_gestures.text
                        if current_gest in self.gesture_replies:
                            self.ids.reply_input.text = self.gesture_replies[current_gest]

                    return True
                else:
                    print(
                        "Error: Invalid JSON format (root element must be a dictionary).")
                    return False
        except Exception as e:
            print(f"Failed to import config: {e}")
            return False


class ReplyEntryApp(App):
    def build(self):
        self.title = "Gesture Reply"
        return ReplyEntry()


if __name__ == "__main__":
    ReplyEntryApp().run()
