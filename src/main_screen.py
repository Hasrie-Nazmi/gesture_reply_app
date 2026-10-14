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
        print(f"Gesture Detected in ReplyEntry: {gesture_name}!")

    def go_back(self, instance):
        print("Going back to MainScreen!")
        self.manager.current = 'main_screen'

    def on_button_click(self, instance):
        print("Button was pressed!")
        self.manager.current = 'reply_screen'


class MainScreenApp(App):

    def build(self):
        self.title = "Gesture Reply"
        return MainScreen()


if __name__ == "__main__":
    MainScreenApp().run()
