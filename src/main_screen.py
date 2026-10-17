import os
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
        # Instantiate the shared processor helper
        self.processor = GestureCameraProcessor()

        self.gesture_reply_test = {
            "gest_0": "This is a reply from Gesture 0",
            "gest_1": "This is a reply from Gesture 1",
            "gest_2": "This is a reply from Gesture 2",
            "gest_3": "This is a reply from Gesture 3",
            "gest_4": "This is a reply from Gesture 4",
            "gest_5": "This is a reply from Gesture 5",
            "Thumbs Up": "This is a reply from Thumbs Up"
        }

        self.current_text = ""
        self.copied_text = []

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

        print(self.gesture_reply_test[gesture_name])
        self.ids.gesture_label.text = self.gesture_reply_test[gesture_name]
        self.current_text = self.gesture_reply_test[gesture_name]

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
