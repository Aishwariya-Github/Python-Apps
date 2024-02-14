from random import randint
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.button import ButtonBehavior
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivymd.uix.widget import MDWidget
from kivy.clock import Clock
from kivy.metrics import dp

KV = """
<MainScreen>:
    MDFloatLayout:
        MDTopAppBar:
            title: "Hue Math"
            pos_hint: {"top": 1}

        MDGridLayout:
            id: Hue
            cols: 2
            rows: 1
            size_hint: None, None
            width: self.minimum_width
            height: self.minimum_height
            spacing: dp(50)

        MDIconButton:
            id: music
            icon: "music"
            icon_size: dp(38)
            _no_ripple_effect: True
            pos_hint: {"top": 0.9}
            theme_icon_color: "Custom"
            icon_color: app.theme_cls.primary_color
            on_release: self.icon = "music-off" if self.icon != "music-off" else "music"

        MDRectangleFlatIconButton:
            id: star
            icon: "star"
            text: "0"
            font_size: dp(30)
            font_name: "QuickSand"
            line_color_disabled: 1, 1, 1, 0
            theme_icon_color: "Custom"
            icon_color: app.theme_cls.primary_color
            disabled: True
            disabled_color: app.theme_cls.primary_color
            pos_hint: {"top": 0.9, "right": 1}

        MDLabel:
            id: bonus
            text: "+2"
            font_name: "QuickSand"
            bold: True
            opacity: 0
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color

        MDGridLayout:
            id: hue
            cols: 3
            rows: 1
            size_hint: None, None
            width: self.minimum_width
            height: self.minimum_height
            spacing: dp(25)

        MDIcon:
            id: add
            icon: "gamepad-round"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            font_size: dp(30)
            pos_hint: {"center_x": 0.5, "center_y": 0.6}

"""

class Cell(ButtonBehavior, MDWidget):
    def __init__(self, *args, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.size_hint = None, None
        self.size = dp(args[0]), dp(args[0])
        self.line_color = 64/255, 64/255, 64/255, 255/255
        self.line_width = 2.5
        self.hue = args[1]
        self.construct = args[2]
        self.bind(on_release = self.check)

    def check(self, instance):
        if instance in self.hue.children:
            for ch in range(3):
                if self.hue.children[ch].md_bg_color != list(fusion_tuple):
                    self.hue.children[ch].opacity = 0
                else:
                    if MDApp.get_running_app().root.ids.music.icon == "music": MDApp.get_running_app().pop.play()
                    value = True if instance == self.hue.children[ch] else False
                    MDApp.get_running_app().update_score([value, ch])
                    Animation(size = (dp(100), dp(100)), d = 1.5, t = "out_elastic").start(self.hue.children[ch])
                    Clock.schedule_once(self.construct, 2)
        

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.Hue = self.ids.Hue
        self.Hue.pos_hint = {"center_x": 0.5, "center_y": 0.6}
        self.hue = self.ids.hue
        self.hue.pos_hint = {"center_x": 0.5, "center_y": 0.2}
        self.construct(self)

    def construct(self, dt):
        self.Hue.clear_widgets()
        self.hue.clear_widgets()
        Clock.schedule_once(self.build_cell, 0.5)

    def fuse(self, Hue_list):
        r = (Hue_list[0][0] + Hue_list[1][0]) if (Hue_list[0][0] + Hue_list[1][0]) <= 255 else 255
        g = (Hue_list[0][1] + Hue_list[1][1]) if (Hue_list[0][1] + Hue_list[1][1]) <= 255 else 255
        b = (Hue_list[0][2] + Hue_list[1][2]) if (Hue_list[0][2] + Hue_list[1][2]) <= 255 else 255
        fusion = r/255, g/255, b/255, 255/255
        return fusion

    def build_cell(self, dt):
        global fusion_tuple
        Hue_list = []
        try:
            for row in range(1):
                for col in range(2):
                    hue_p = Cell(125, self.hue, self.construct)
                    hue_p.opacity = 0
                    Hue_tuple = randint(0, 255), randint(0, 255), randint(0, 255), 255
                    Hue_list.append((Hue_tuple))
                    hue_p.md_bg_color = tuple(H/255 for H in Hue_tuple)
                    self.Hue.add_widget(hue_p)
                    anim = Animation(opacity = 1, d = 1)
                    anim.start(hue_p)
            for row in range(1):
                for col in range(3):
                    hue_c = Cell(75, self.hue, self.construct)
                    hue_c.disabled = True
                    hue_tuple = randint(0, 255), randint(0, 255), randint(0, 255), 255
                    hue_c.md_bg_color = tuple(h/255 for h in hue_tuple)
                    self.hue.add_widget(hue_c)
            fusion_tuple = self.fuse(Hue_list)
            self.hue.children[randint(0, 2)].md_bg_color = fusion_tuple
            MDApp.get_running_app().start_timer()
        except Exception:
            pass

class MyGame(MDApp):
    def disable_hue_child(self, value):
        for ch in range(3): self.root.ids.hue.children[ch].disabled = value
        
    def stop_timer(self, value):
        if hasattr(self, "timer_event"): self.timer_event.cancel()
        if value == 1: self.disable_hue_child(True)
        
    def re_set(self, value):
        self.root.ids.star.text = str((int(self.root.ids.star.text)) + value)
        self.stop_timer(1)
        
    def start_timer(self):
        self.disable_hue_child(False)
        self.timer = 0
        self.stop_timer(0)
        self.update_timer()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        
    def update_timer(self, dt = None):
        self.timer += 1

    def update_score(self, value): 
        if value[0] == True:
            if self.timer < 5:
                self.root.ids.bonus.opacity = 0.7
                self.root.ids.bonus.font_size = dp(24)
                self.root.ids.bonus.pos_hint = {"center_x": self.poz[value[1]], "center_y": 0.375}
                anim = Animation(opacity = 0, d = 0.5) & Animation(font_size = dp(54), d = 0.5, t = "out_sine")
                anim.start(self.root.ids.bonus)
                self.re_set(2)
            else: self.re_set(1)
        elif value[0] == False:
            if int(self.root.ids.star.text) != 0: self.re_set(-1)

    def build(self):
        Builder.load_string(KV)
        self.poz = [0.8, 0.5, 0.2]
        self.icon = "assets/icon.png"
        self.pop = SoundLoader.load("assets/pop.wav")
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.material_style = "M3"
        LabelBase.register(name = "QuickSand", fn_regular = "fonts/Quicksand-SemiBold.ttf", fn_bold = "fonts/Quicksand-Bold.ttf")
        return MainScreen()

if __name__ == "__main__":
    MyGame().run()

'''
error/look-outs
no ripple effect or set it to square shape.
'''
