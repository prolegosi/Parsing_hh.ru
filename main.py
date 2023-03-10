from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")

        self.label = Label(text='Hello from Kivy',
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})


        self.input = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        self.button = Button(
                text= 'button',
                pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        main_layout.add_widget(self.input)
        main_layout.add_widget(self.label)
        main_layout.add_widget(self.button)

        return main_layout

if __name__ == "__main__":
    app = MainApp()
    app.run()