from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

Window.clearcolor = (0.16, 0.17, 0.2)


class FirstPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation="vertical",
                                padding=15,
                                spacing=15
                                )

        self.label_1 = Label(text='Введите название города или региона',
                             size_hint=(1, 1),
                             pos_hint={'center_x': .5, 'center_y': .5},
                             outline_color=[0, 0, 0],
                             outline_width=0.5,
                             )

        self.input_1 = TextInput(
            size_hint=(1, 1),
            multiline=False,
            halign="right",
            font_size=14,
        )

        self.label_2 = Label(text='Введите названия профессий,\n    должностей через пробел',
                             size_hint=(1, 1),
                             pos_hint={'center_x': .5, 'center_y': .5},
                             outline_color=[0, 0, 0],
                             outline_width=0.5
                             )

        self.input_2 = TextInput(
            size_hint=(1, 1),
            multiline=False,
            halign="right",
            font_size=14
        )

        self.label_3 = Label(text='',
                             size_hint=(1, 1),
                             pos_hint={'center_x': .5, 'center_y': .5}
                             )

        self.button = Button(
            size_hint=(.5, 1),
            text='Поиск',
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_normal='',
            background_color=[0.18, 0.18, 0.2],
            on_press=self.click
        )

        self.label_4 = Label(text='',
                             size_hint=(1, 1),
                             pos_hint={'center_x': .5, 'center_y': .5}
                             )

        main_layout.add_widget(self.label_1)
        main_layout.add_widget(self.input_1)
        main_layout.add_widget(self.label_2)
        main_layout.add_widget(self.input_2)
        main_layout.add_widget(self.label_3)
        main_layout.add_widget(self.button)
        main_layout.add_widget(self.label_4)
        self.add_widget(main_layout)

    def click(self, event):
        a = self.input_1.text
        b = self.input_2.text
        set_screen('Two_page')
        print(type(a), len(b))


class TwoPage(Screen):
    def __int__(self):


def set_screen(name_screen):
    sm.current = name_screen

sm = ScreenManager()
sm.add_widget(FirstPage(name='First_page'))
class JobsSkilApp(App):
    def build(self):

        return sm


if __name__ == "__main__":
    app = JobsSkilApp()
    app.run()
