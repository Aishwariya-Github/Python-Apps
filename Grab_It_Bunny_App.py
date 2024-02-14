from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.lang import Builder
from kivymd.app import MDApp
from random import randint, uniform, choice
from kivy.animation import Animation
from kivy.core.text import LabelBase
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.metrics import dp
from math import dist
from time import time

Config.set('kivy', 'exit_on_escape', '0')

KV = '''
#: import sm kivy.uix.screenmanager
#: import Window kivy.core.window.Window

ScreenManager:
    transition: sm.NoTransition()
    MenuScreen:
    MainScreen:

<MenuScreen>:
    name: "menu"
    MDFloatLayout:

##        Image:
##            source: "assets/woods.png"
##            fit_mode: "fill"
            
        MDFloatLayout:
            id: star_jar
            
        MDLabel:
            text: "Grab it, Bunny!"
            font_style: "H3"
            font_name: "QuickSand"
            theme_text_color: "Custom"
            text_color: 192/255, 64/255, 0/255, 1
            bold: True
            halign: "center"
            pos_hint: {"center_y": 0.9}
            
        MDFillRoundFlatButton:
            text: "START"
            font_name: "QuickSand"
            bold: True
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {"center_x": 0.5, "center_y": 0.15}
            on_release: app.GameStart()

        MDFillRoundFlatButton:
            text: "QUIT"
            font_name: "QuickSand"
            bold: True
            md_bg_color: app.theme_cls.primary_color
            on_release: app.stop()
            pos_hint: {"center_x": 0.5, "center_y": 0.05}

        

<MainScreen>:
    name: "main"
    MDFloatLayout:
        id: main_container

        MDFloatLayout:

            id: playground
            size_hint: None, None
            size: Window.size[0] * 0.9, Window.size[1] * 0.75
            center: Window.size[0] * 0.5, Window.size[1] * 0.5
            
##            Image:
##                source: "assets/grass.png"
##                fit_mode: "fill"
##                pos: playground.pos
                
            Container:
                id: env
                orientation: "horizontal"            
                md_bg_color: 1, 1, 1, 0
                padding: dp(5), dp(5)
                size_hint: None, None
                size: playground.size
                pos: playground.pos
                
                
                Image:
                    id: basket
                    source: "assets/basket.png"
                    size_hint: None, None
                    size: self.texture_size[0], self.texture_size[1]

                MDFloatLayout:
                    id: veggie_space
                    md_bg_color: 1, 1, 1, 0
                
                Image:
                    id: bunny
                    source: "assets/bunny.png"
                    size_hint: None, None
                    size: self.texture_size[0], self.texture_size[1]


        MDFloatLayout:
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
                pos_hint: {"top": 0.975, "right": 0.975}

            MDIcon:
                id: updown
                icon: "menu-up"
                font_size: dp(100)
                opacity: 0
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                

            MDIconButton:
                id: home_menu
                icon: "home"
                icon_size: dp(35)
                theme_icon_color: "Custom"
                icon_color: 1, 0, 0, 0.5
                pos_hint: {"x": 0}
                on_release: app.home()
                
            MDIconButton:
                id: play_pause
                icon: "pause"
                icon_size: dp(35)
                theme_icon_color: "Custom"
                icon_color: 1, 0, 0, 0.5
                pos_hint: {"right": 1}
                on_press: self.icon = "play" if self.icon != "play" else "pause"
                on_release: app.isPause = True if app.isPause != True else False

            Label:
                id: timer
                text: "TIME 0:00"
                font_size: dp(18)
                font_name: "QuickSand"
                bold: True
                padding: dp(5), dp(5)
                size_hint: None, None
                size: dp(100), self.texture_size[1] 
                halign: "center"
                background_color: 1, 0, 0, 0.5
                pos_hint: {"top": 0.95, "x": 0.05}
                canvas.before:
                    Color: 
                        rgba: self.background_color
                    Rectangle:
                        pos: self.pos
                        size: self.size
                   
<Container>:
'''     

        
class Container(MDCard):
    def INIT(self, dt = None) -> None:
        self.VELOCITY = Vector(0, 0)
        self.STEP = dp(300)
        self.last_time = time()
        self.del_time_motion = Clock.schedule_interval(self.update, 1.0 / 60.0)

        self.screen = MDApp.get_running_app().root.get_screen("main")
        
    def on_touch_up(self, touch) -> None:
        self.VELOCITY = Vector(0, 0)

    def on_touch_down(self, touch) -> None:
        if MDApp.get_running_app().touch_enabled:
            displacement = Vector(touch.x - self.screen.ids.bunny.center_x, touch.y - self.screen.ids.bunny.center_y)

            if displacement.length() > 0:
                direction = displacement.normalize()
                
                if self.screen.ids.updown.icon == "menu-down":
                    direction *= -1
                    
                self.VELOCITY = direction * self.STEP

            
    def update(self, dt) -> None:
        if not MDApp.get_running_app().isPause:
            current_time = time()
            dt = current_time - self.last_time
            self.last_time = current_time
                
            NEW_POS = [self.screen.ids.bunny.center_x, self.screen.ids.bunny.center_y]
            NEW_POS[0] += self.VELOCITY.x * dt
            NEW_POS[1] += self.VELOCITY.y * dt
            
            new_x = max(self.screen.ids.env.pos[0] + self.screen.ids.bunny.size[0]/2, min(NEW_POS[0], self.screen.ids.env.pos[0] + self.screen.ids.env.size[0] - self.screen.ids.bunny.size[0]/2))
            new_y = max(self.screen.ids.env.pos[1] + self.screen.ids.bunny.size[1]/2, min(NEW_POS[1], self.screen.ids.env.pos[1] + self.screen.ids.env.size[1] - self.screen.ids.bunny.size[1]/2))

            self.screen.ids.bunny.center = (new_x, new_y)            
            self.screen.is_collision()
                                  

class MenuScreen(Screen):
    pass
           
class MainScreen(Screen):        

    def on_enter(self, *args):
        Window.bind(on_keyboard = self.back_click)
        
    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.back_click)
        
    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            MDApp.get_running_app().home()    
                
    def setup(self) -> None:       
        bunny = self.ids.bunny        
        while True:
            sx_pos = uniform(self.ids.env.pos[0] + bunny.size[0], self.ids.env.pos[0] + self.ids.env.size[0] - bunny.size[0])
            sy_pos = uniform(self.ids.env.pos[1] + bunny.size[1], self.ids.env.pos[1] + self.ids.env.size[1] - bunny.size[1])
            spos = sx_pos, sy_pos
            
            hx_pos = uniform(self.ids.env.pos[0] + bunny.size[0], self.ids.env.pos[0] + self.ids.env.size[0] - bunny.size[0])
            hy_pos = uniform(self.ids.env.pos[1] + bunny.size[1], self.ids.env.pos[1] + self.ids.env.size[1] - bunny.size[1])
            hpos = hx_pos, hy_pos

            if dist(spos, hpos) > dp(250):
                break

        bunny.center = spos
        self.ids.basket.center = hpos
        self.pos_list = [hpos, spos]

    
    def veggie_factory(self) -> None:
        Clock.schedule_once(self.veggie_opacity, -1)
        space = self.ids.veggie_space
        if space.children: space.clear_widgets()
        
        index, MDApp.get_running_app().veggies = 0, randint(2, 4)
        del self.pos_list[2:]

        while index < MDApp.get_running_app().veggies:
            angle = randint(0, 360)
            veggie = Image(source = choice(["assets/carrot.png", "assets/turnip.png"]),
                        size_hint = (None, None))
            veggie.size = veggie.texture_size[0], veggie.texture_size[1]          
            while True:
                new_pos = (uniform(space.pos[0] + veggie.size[0], space.pos[0] + space.size[0] - veggie.size[0]),
                           uniform(space.pos[1] + veggie.size[1], space.pos[1] + space.size[1] - veggie.size[1]))

                valid = all(dist(new_pos, existing_pos) > dp(75) for existing_pos in self.pos_list)
                if valid:
                    self.pos_list.append(new_pos)
                    break
            veggie.center = new_pos

            veggie.canvas.before.add(PushMatrix())
            veggie.canvas.before.add(Rotate(angle = angle, axis = (0, 0, 1), origin = veggie.center))
            veggie.canvas.after.add(PopMatrix())
            
            space.add_widget(veggie)
            index += 1
        Clock.schedule_once(self.veggie_opacity, 0.5)

    def veggie_opacity(self, dt = None) -> None:
        self.ids.veggie_space.opacity = 1 if self.ids.veggie_space.opacity != 1 else 0
            
    def reverse(self, dt = None) -> None:
        if not MDApp.get_running_app().isPause:
            self.ids.updown.icon = "menu-down" if self.ids.updown.icon != "menu-down" else "menu-up"
            self.ids.updown.pos_hint = {"center_x": 0.5, "top": 1} if self.ids.updown.icon == "menu-up" else {"center_x": 0.5, "top": 0.2}

            anim = Animation(opacity = 1, d = 0.5) + Animation(opacity = 0, d = 0.5)
            anim.start(self.ids.updown)

    def is_collision(self):
        poz_x, poz_y = 0.35, 0.5
        sx1, sy1 =  self.ids.bunny.pos
        sw1, sh1 = self.ids.bunny.size

        if "Veggie":
            try:
                for veggie in range(len(self.ids.veggie_space.children)):
                    gx2, gy2 = self.ids.veggie_space.children[veggie].center
                    gw2, gh2 = self.ids.veggie_space.children[veggie].size
                    if (sx1 < gx2 + gw2*0.75 and sx1 + sw1 > gx2 + gw2*0.25
                        and sy1 < gy2 + gh2*0.75 and sy1 + sh1 > gy2 + gh2*0.25):
                    
                        self.ids.veggie_space.remove_widget(self.ids.veggie_space.children[veggie])
                        MDApp.get_running_app().collectibles += 1
                        
            except Exception:
                pass

                    
        if "Basket":
            gx2, gy2 = self.ids.basket.pos
            gw2, gh2 = self.ids.basket.size

            if (sx1 < gx2 + gw2*0.75 and sx1 + sw1 > gx2 + gw2*0.25
                and sy1 < gy2 + gh2*0.75 and sy1 + sh1 > gy2 + gh2*0.25):
                if MDApp.get_running_app().collectibles == MDApp.get_running_app().veggies:
                    if MDApp.get_running_app()._sec >= 22:

                        self.ids.star.text = str(int(self.ids.star.text) + 3)
                        for image in range(3):
                            img = Image(source = "assets/blue_star.png",
                                        size_hint = (None, None))
                            img.size = img.texture_size[0]/2, img.texture_size[1]/2
                            img.pos_hint = {"center_x": poz_x, "center_y": poz_y}
                            if image == 1: img.pos_hint = {"center_x": poz_x, "center_y": 0.6}
                            MDApp.get_running_app().root.get_screen('menu').ids.star_jar.add_widget(img)
                            poz_x = poz_x + 0.15

                    elif MDApp.get_running_app()._sec >= 15:

                        self.ids.star.text = str(int(self.ids.star.text) + 2)
                        for image in range(2):
                            img = Image(source = "assets/blue_star.png",
                                        size_hint = (None, None))
                            img.size = img.texture_size[0]/2, img.texture_size[1]/2
                            img.pos_hint = {"center_x": poz_x, "center_y": poz_y}
                            if image == 1: img.pos_hint = {"center_x": poz_x, "center_y": 0.6}
                            MDApp.get_running_app().root.get_screen('menu').ids.star_jar.add_widget(img)
                            poz_x = poz_x + 0.15

                    elif MDApp.get_running_app()._sec >= 10:

                        self.ids.star.text = str(int(self.ids.star.text) + 1)
                        img = Image(source = "assets/blue_star.png",
                                    size_hint = (None, None))
                        img.size = img.texture_size[0]/2, img.texture_size[1]/2
                        img.pos_hint = {"center_x": poz_x, "center_y": poz_y}
                        MDApp.get_running_app().root.get_screen('menu').ids.star_jar.add_widget(img)

                else:
                    lbl = MDLabel(text = "Keep it up!",
                                  font_style = "H4",
                                  font_name = "QuickSand",
                                  halign = "center",
                                  theme_text_color = "Custom",
                                  text_color = (192/255, 64/255, 0/255, 1),
                                  pos_hint = {"center_x": 0.5, "center_y": 0.5})
                    MDApp.get_running_app().root.get_screen('menu').ids.star_jar.add_widget(lbl)
                    
                

                MDApp.get_running_app().home()
    

class hour_glass(Image):
    f, i = 0, 1
    def __init__(self, **kwargs):
        super(hour_glass, self).__init__(**kwargs)

        self.frames = [f"assets/hg_{i}.png" for i in range(1, 9)]
        self.source = self.frames[self.f]
        self.update = Clock.schedule_interval(self.animate_time, 0.2)

    def animate_time(self, dt):
        self.f =  (self.f + self.i) % 8
        self.source = self.frames[self.f]
        if self.f == 7:
            self.update.cancel()
        
class MyGame(MDApp):
    veggies, collectibles = 0, 0
    touch_enabled = False
    isPause = False
    _sec = 0

    def GameStart(self):
        self.veggies = 0
        self.collectibles = 0
        self.root.get_screen("main").ids.main_container.opacity = 0.5
        self.root.get_screen("main").ids.timer.text = f"TIME 0:00"
        self.root.get_screen("main").ids.updown.icon = "menu-up"
        self.root.get_screen("main").ids.play_pause.icon = "pause"
        
        self.root.get_screen('menu').ids.star_jar.clear_widgets()
        self.isPause = False

        self.root.get_screen("main").setup()
        self.root.get_screen("main").veggie_factory()
        
        self.root.current = "main"

        self.count_down_label = MDLabel(halign = "center",
                                        font_style = "H3",
                                        font_name = "QuickSand",
                                        theme_text_color = "Custom",
                                        text_color = MDApp.get_running_app().theme_cls.primary_color)
        
        self.root.get_screen("main").add_widget(self.count_down_label)
        self.time_left = 3
        
        self.count_down_to_game()
        self.countdown = Clock.schedule_interval(self.count_down_to_game, 0.75)


    def count_down_to_game(self, dt = None):
        
        s = self.time_left % 60
        self.count_down_label.text = f"{s}" if s != 0 else f"GO!"
        if s == 0:
            self.countdown.cancel()
            Clock.schedule_once(self.commence, 0.5)
        self.time_left -= 1

    def commence(self, dt = None):
        self.touch_enabled = True
        self.root.get_screen("main").ids.main_container.opacity = 1
        self.root.get_screen("main").remove_widget(self.count_down_label)
        self.start_timer()
            
    def home(self):
        self.stop_clocks(["del_time_motion", "timer_event", "sense_of_direction"])
        self.root.current = "menu"

    def start_timer(self):        
        self.time_left = 30
        self.stop_clocks(["timer_event"])

        func_del_trigger = self.root.get_screen('main').ids.env.INIT
        Clock.schedule_once(func_del_trigger, -1)

        func_sense = self.root.get_screen('main').reverse
        self.sense_of_direction = Clock.schedule_interval(func_sense, 5)       

        self.update_countdown()
        self.timer_event = Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt = None):
        
        if not self.isPause:
            _min = self.time_left // 60
            self._sec = self.time_left % 60
            self.root.get_screen("main").ids.timer.text = f"TIME {_min}:{self._sec:02}"

            if self.time_left == -1:

                img = hour_glass()
                img.size_hint = (None, None)
                img.size = img.texture_size[0], img.texture_size[1]
                img.pos_hint = {"center_x": 0.5, "center_y": 0.5}

                self.root.get_screen('menu').ids.star_jar.add_widget(img)
                self.home()

            self.time_left -= 1

    def stop_clocks(self, events):
        for e in events:
            if hasattr(self, e):  getattr(self, e).cancel()
            elif hasattr(self.root.get_screen('main'), e):
                getattr(self.root.get_screen('main'), e).cancel()
            elif hasattr(self.root.get_screen('main').ids.env, e):
                getattr(self.root.get_screen('main').ids.env, e).cancel()

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        LabelBase.register(name = "QuickSand", fn_regular = "fonts/Quicksand-SemiBold.ttf", fn_bold = "fonts/Quicksand-Bold.ttf")
        return Builder.load_string(KV)

if __name__ == "__main__":
    MyGame().run()

'''
LOOK-OUTS:-

: time's up case
: Game Assets Integration...UI clean-up

LIMITATIONS ->>
: Upper bound on the amount of spacing between carrots??
: delta time physics - during continuous del motion, the direction doesn't change
even after reversal in the sense??

GAME-DEV-CONCEPTS:-
: howto default parameters??
: time complexity??
: framerate independent physics??
'''
