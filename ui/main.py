from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class ReplyEntry(BoxLayout):

    def on_button_click(self, instance):
        print("Button was pressed!")


class ReplyEntryApp(App):

    def build(self):
        self.title = "Gesture Reply"
        return ReplyEntry()


if __name__ == "__main__":
    ReplyEntryApp().run()
