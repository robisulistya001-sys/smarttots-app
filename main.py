"""
SmartTots App - Final Optimized Version
Perbaikan menyeluruh terhadap bug-bug yang ditemukan:
- Root widget sekarang ScreenManager yang valid.
- Lambda di SplashScreen diganti method terpisah.
- Tidak ada atribut 'source' pada Ellipse, dan penumpukan objek dicegah.
- Unbinding event di TraceLearnGame saat cleanup.
- ParentalGate menggunakan logika urutan yang ketat.
- Font didefinisikan dan digunakan.
- Exception handling diperbaiki.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import random

# ----------------------------------------------------------------------
# Konstanta
# ----------------------------------------------------------------------
FONT_NAME = 'fonts/Nunito-Bold.ttf'

# ----------------------------------------------------------------------
# Sound Manager
# ----------------------------------------------------------------------
class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sounds = {}
        return cls._instance

    def load(self, name, filepath):
        try:
            sound = SoundLoader.load(filepath)
            if sound:
                self.sounds[name] = sound
        except Exception:
            print(f"Could not load sound: {filepath}")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

# ----------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_main, 2)

    def switch_to_main(self, dt):
        self.manager.current = 'main_menu'

class MainMenuScreen(Screen):
    pass

class ParentalGateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target = [1, 2, 3]
        self.sequence = []

    def press_number(self, number):
        if self.sequence == self.target:
            return

        if len(self.sequence) >= len(self.target) or number != self.target[len(self.sequence)]:
            self.sequence = []
            self.ids.status_label.text = "Wrong sequence. Try again."
            return

        self.sequence.append(number)
        self.ids.status_label.text = f"Pressed: {self.sequence}"

        if self.sequence == self.target:
            self.ids.status_label.text = "Access granted!"
            self.manager.current = 'main_menu'

class ColorSplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.circle = None
        self.layout = None

    def on_enter(self):
        if not self.layout:
            self.layout = self.ids.game_layout
            self.draw_initial_circle()

    def draw_initial_circle(self):
        with self.layout.canvas:
            Color(1, 0, 0, 1)
            self.circle = Ellipse(pos=(150, 150), size=(200, 200))

    def on_touch_down(self, touch):
        if not self.circle:
            return super().on_touch_down(touch)

        cx, cy = self.circle.pos
        r = self.circle.size[0] / 2
        dx = touch.x - (cx + r)
        dy = touch.y - (cy + r)
        if dx*dx + dy*dy <= r*r:
            self.layout.canvas.remove(self.circle)
            with self.layout.canvas:
                Color(random.random(), random.random(), random.random(), 1)
                self.circle = Ellipse(pos=(cx, cy), size=(200, 200))
        return super().on_touch_down(touch)

class TraceLearnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = None
        self.bound = False

    def on_enter(self):
        if not self.layout:
            self.layout = self.ids.trace_layout
        if not self.bound:
            self.layout.bind(on_touch_down=self.on_touch_down,
                             on_touch_move=self.on_touch_move,
                             on_touch_up=self.on_touch_up)
            self.bound = True

    def on_touch_down(self, instance, touch):
        if self.layout.collide_point(*touch.pos):
            with self.layout.canvas:
                Color(1, 1, 0)
                d = 10
                Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))
        return True

    def on_touch_move(self, instance, touch):
        if self.layout.collide_point(*touch.pos):
            with self.layout.canvas:
                Color(1, 1, 0)
                d = 10
                Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))
        return True

    def on_touch_up(self, instance, touch):
        pass

    def cleanup(self):
        if self.layout:
            self.layout.unbind(on_touch_down=self.on_touch_down,
                               on_touch_move=self.on_touch_move,
                               on_touch_up=self.on_touch_up)
        self.bound = False
        self.layout.canvas.clear()

# ----------------------------------------------------------------------
# Root ScreenManager & KV
# ----------------------------------------------------------------------
class SmartTotsApp(App):
    def build(self):
        return ScreenManager()

KV = '''
#:import FONT_NAME __main__.FONT_NAME

<ScreenManager>:
    id: sm
    SplashScreen:
        name: 'splash'
    MainMenuScreen:
        name: 'main_menu'
    ParentalGateScreen:
        name: 'parental_gate'
    ColorSplashScreen:
        name: 'color_splash'
    TraceLearnScreen:
        name: 'trace_learn'

<SplashScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'SmartTots'
            font_name: FONT_NAME
            font_size: 48
            halign: 'center'

<MainMenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        Label:
            text: 'Main Menu'
            font_name: FONT_NAME
            font_size: 36
        Button:
            text: 'Color Splash'
            on_release: app.root.current = 'color_splash'
        Button:
            text: 'Trace & Learn'
            on_release: app.root.current = 'trace_learn'
        Button:
            text: 'Parental Gate'
            on_release: app.root.current = 'parental_gate'

<ParentalGateScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: status_label
            text: 'Enter sequence: 1, 2, 3'
            font_name: FONT_NAME
        GridLayout:
            cols: 3
            Button:
                text: '1'
                on_release: root.press_number(1)
            Button:
                text: '2'
                on_release: root.press_number(2)
            Button:
                text: '3'
                on_release: root.press_number(3)
        Button:
            text: 'Back'
            on_release: app.root.current = 'main_menu'

<ColorSplashScreen>:
    FloatLayout:
        id: game_layout
        canvas.before:
            Color:
                rgba: 0.9, 0.9, 0.9, 1
            Rectangle:
                pos: self.pos
                size: self.size

<TraceLearnScreen>:
    FloatLayout:
        id: trace_layout
        canvas.before:
            Color:
                rgba: 0.8, 0.8, 0.8, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            text: 'Clear'
            size_hint: 0.2, 0.1
            pos_hint: {'x': 0.4, 'y': 0.9}
            on_release: root.cleanup()
        Button:
            text: 'Back to Menu'
            size_hint: 0.2, 0.1
            pos_hint: {'x': 0.4, 'y': 0.8}
            on_release: 
                root.cleanup()
                app.root.current = 'main_menu'
'''

if __name__ == '__main__':
    from kivy.lang import Builder
    Builder.load_string(KV)
    SmartTotsApp().run()

