from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.app import runTouchApp

import back

Window.clearcolor = (0.16, 0.17, 0.2)


class FirstScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'First'
        main_layout = BoxLayout(orientation="vertical",
                                padding=15,
                                spacing=15
                                )

        self.label_1 = Label(text='Введите название региона, например: Омская область',
                             size_hint=(1, 1),
                             pos_hint={'center_x': .5, 'center_y': .5},
                             outline_color=[0, 0, 0],
                             outline_width=0.5,
                             )

        self.input_1 = TextInput(
            size_hint=(1, 1),
            multiline=False,
            halign="right",
            font_size=14
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
            on_press=self.to_second_scrn
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

    def to_second_scrn(self, *args):
        # получаем id региона
        area, area_id = back.count_validation(self.input_1.text)
        jobs_string = back.job_processing(self.input_2.text)
        print(area, area_id)
        print(jobs_string)

        if area_id:
            self.manager.current = 'Two'
        else:
            self.label_1.text = area


class TwoScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = 'Two'
        self.size_hint = (1, None)
        self.size = (Window.width, Window.height)


        main_layout = GridLayout(
            padding=dp(15),
            size_hint_y=None,
            spacing=dp(10),
            cols=1,
            # height=dp(1150),
            # row_default_height=dp(15)

        )

        main_layout.bind(minimum_height=main_layout.setter('height'))
        for i in range(50):
            main_layout.add_widget(Label(text=f'Введите названия профессий {i}',
                                         size_hint_y=None,
                                         height=dp(15),
                                         ))
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(main_layout)
        self.add_widget(root)

    def to_second_screen(self, *args):
        self.manager.current = 'First'


sm = ScreenManager()


# def set_screen(name_screen):
#   sm.current = name_screen

class JobsSkilApp(App):
    def build(self):
        sm.add_widget(FirstScreen())
        sm.add_widget(TwoScreen())
        return sm


if __name__ == "__main__":
    app = JobsSkilApp()
    app.run()
