import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from gesture_processor import GestureCameraProcessor

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
kv_path = os.path.join(ROOT_DIR, '..', 'ui', 'replyentry.kv')

Builder.load_file(kv_path)


class ReplyEntry(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.processor = GestureCameraProcessor()

    def on_enter(self, *args):
        """Triggered automatically when entering the ReplyEntry screen."""
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
        gesture_reply_test = {
            "gest_0": "This is a reply from Gesture 0",
            "gest_1": "This is a reply from Gesture 1",
            "gest_2": "This is a reply from Gesture 2",
            "gest_3": "This is a reply from Gesture 3",
            "gest_4": "This is a reply from Gesture 4",
            "gest_5": "This is a reply from Gesture 5",
            "Thumbs Up": "This is a reply from Thumbs Up"
        }
        print(
            f"Gesture Detected in ReplyEntry: {gesture_reply_test[gesture_name]}!")

    def go_back(self, instance):
        print("Going back to MainScreen!")
        self.manager.current = 'main_screen'

    def on_spinner_select(self, selected_text):
        print(f"Selected gesture: {selected_text}")
        ASSETS_DIR = os.path.join(ROOT_DIR, '..', 'assets')
        gesture_map = {
            "Gesture 0": os.path.join(ASSETS_DIR, "gesture_zero.jpg"),
            "Gesture 1": os.path.join(ASSETS_DIR, "gesture_one.jpg"),
            "Gesture 2": os.path.join(ASSETS_DIR, "gesture_two.jpg"),
            "Gesture 3": os.path.join(ASSETS_DIR, "gesture_three.jpg"),
            "Gesture 4": os.path.join(ASSETS_DIR, "gesture_four.jpg"),
            "Gesture 5": os.path.join(ASSETS_DIR, "gesture_five.jpg"),
            "Thumbs Up": os.path.join(ASSETS_DIR, "gesture_thumbs_up.jpg"),
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
