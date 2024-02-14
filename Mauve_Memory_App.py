from random import sample, randint
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.button import ButtonBehavior
from kivy.animation import Animation
from kivymd.uix.widget import MDWidget
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.metrics import dp

KV = """
<MainScreen>:
    MDFloatLayout:
        MDTopAppBar:
            title: "Mauve Memory"
            pos_hint: {"top": 1}
        MDLabel:
            id: countdown_label
            text: "00:00"
            font_style: "H3"
            font_name: "QuickSand"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            halign: "center"
            pos_hint: {"center_x": 0.5, "center_y": 0.825}

        MDGridLayout:
            id: matrix
            cols: root.n
            rows: root.n
            size_hint: None, None
            width: self.minimum_width
            height: self.minimum_height
            spacing: dp(2.5)

        MDIcon:
            id: icon
            opacity: 0
            theme_text_color: "Custom"
            text_color: 134/255, 208/255, 7/255, 255/255
            font_size: dp(72)
            pos_hint: {"center_x": 0.5, "center_y": 0.825}

        MDRaisedButton:
            id: start
            text: "[b]START[/b]"
            disabled: True
            md_bg_color_disabled: app.theme_cls.primary_color
            md_bg_color: app.theme_cls.primary_color
            on_release: root.color_cell()
            pos_hint: {"center_x": 0.5, "center_y": 0.175}

        MDLabel:
            id: level
            text: "EASY"
            font_name: "QuickSand"
            bold: True
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            pos_hint: {"center_y": 0.039}

        MDIconButton:
            id: m_right
            icon: "chevron-right"
            pos_hint: {"y": 0, "center_x": 0.75}
            theme_icon_color: "Custom"
            icon_color: app.theme_cls.primary_color
            disabled: False
            on_release: root.level_UpDown("right")

        MDIconButton:
            id: m_left
            icon: "chevron-left"
            pos_hint: {"y": 0, "center_x": 0.25}
            theme_icon_color: "Custom"
            icon_color: app.theme_cls.primary_color
            disabled: False
            on_release: root.level_UpDown("left")
"""
class Cell(ButtonBehavior, MDWidget):
    global cell_displayed_list, wrong_cell_list
    cell_displayed_list, wrong_cell_list = [], []
    def __init__(self, *args, **kwargs):
        super(Cell, self).__init__(**kwargs)

        self.matrix = args[0]
        self.revert_color = args[1]
        
        self.size_hint = None, None
        self.size = dp(45), dp(45)
        self.md_bg_color = color_list[0]
        self.bind(on_release = self.reveal)

    def reveal(self, instance):
        current_cell_index = self.matrix.children.index(instance)
        if current_cell_index in index_list:
            self.matrix.children[current_cell_index].md_bg_color = color_list[cache_col_index]
            cell_displayed_list.append(current_cell_index)
            
            if sorted(set(cell_displayed_list)) == index_list:
                self.show_icon("check-circle")
                reset_count= False
        else:
            wrong_cell_list.append(current_cell_index)
            if len(wrong_cell_list) > 2:
                self.show_icon("close-circle")

    def show_icon(self, value):
        global pause
        pause = True
        wrong_cell_list.clear()
        cell_displayed_list.clear()
        index_list.clear()
        self.parent.parent.parent.ids.countdown_label.opacity = 0
        self.parent.parent.parent.ids.icon.icon = value
        anim = Animation(opacity = 1, d = 0.5) + Animation(opacity = 0, d = 0.7)
        anim.start(self.parent.parent.parent.ids.icon)
        if value == "close-circle":
           self.parent.parent.parent.ids.icon.theme_text_color = "Error"
        Clock.schedule_once(self.revert_color, 0.5)
        
class MainScreen(MDScreen):
    n, m, = 4, 9
    level = ["EASY", "INTERMEDIATE", "HARD"]
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.matrix = self.ids.matrix
        self.matrix.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.construct_matrix()

    def construct_matrix(self):
       self.ids.start.disabled = True
       self.matrix.clear_widgets()
       self.index = 0
       Clock.schedule_once(self.build_cell, 0.5)

    def build_cell(self, dt = 0):
        try:
            if self.index < (self.n**2):
                row = self.index // (self.n)
                col = self.index % (self.n)
                cell = Cell(self.matrix, self.revert_color)
                cell.opacity = 0
                cell.disabled = True
                self.matrix.add_widget(cell)
                Animation(opacity = 1, d = 0.25).start(cell)
                self.index += 1
                Clock.schedule_once(self.build_cell, 0.1)
                if self.index == (self.n**2 - 1):
                    self.ids.start.disabled = False
        except Exception:
            pass

    def level_UpDown(self, direction):
        level = self.ids.level.text
        if direction == "right":
            if self.level.index(level) == 0:
                self.stop_countdown()
                self.ids.countdown_label.text = f"{0:02}:{0:02}"
                self.ids.icon.opacity = 0
                self.ids.level.text = self.level[1]
                self.n, self.m = 5, 12
                self.matrix.cols, self.matrix.rows = self.n, self.n
                self.construct_matrix()
            elif self.level.index(level) == 1:
                self.stop_countdown()
                self.ids.countdown_label.text = f"{0:02}:{0:02}"
                self.ids.icon.opacity = 0
                self.ids.level.text = self.level[2]
                self.n, self.m = 6, 15
                self.matrix.cols, self.matrix.rows = self.n, self.n
                self.construct_matrix()
            else:
                pass

        elif direction == "left":
            if self.level.index(level) == 2:
                self.stop_countdown()
                self.ids.countdown_label.text = f"{0:02}:{0:02}"
                self.ids.icon.opacity = 0
                self.ids.level.text = self.level[1]
                self.n, self.m = 5, 12
                self.construct_matrix()
                self.matrix.cols, self.matrix.rows = self.n, self.n
            elif self.level.index(level) == 1:
                self.stop_countdown()
                self.ids.countdown_label.text = f"{0:02}:{0:02}"
                self.ids.icon.opacity = 0
                self.ids.level.text = self.level[0]
                self.n, self.m = 4, 9
                self.construct_matrix()
                self.matrix.cols, self.matrix.rows = self.n, self.n
            else:
                pass

    def de_activate_menu(self, value):
        self.ids.m_right.disabled = value
        self.ids.m_left.disabled = value

    def start_countdown(self):
        self.time_left = countdown_list[self.level.index(self.ids.level.text)]
        self.ids.start.disabled = False
        self.stop_countdown()
        self.update_countdown()
        self.timer_event = Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt = None):
        global pause, cell_displayed_list
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.ids.countdown_label.text = f"{minutes:02}:{seconds:02}"

        if self.time_left == 0:
            self.stop_countdown()
            cell_displayed_list.clear()
            index_list.clear()

        elif pause == True:
            self.stop_countdown()
            for ch in range(len(self.matrix.children)): self.matrix.children[ch].disabled = True
            pause = False

        self.time_left -= 1

    def stop_countdown(self):
        if hasattr(self, "timer_event"):
            self.timer_event.cancel()

    def color_cell(self):
        global cache_col_index, cell_displayed_list

        cache_col_index = randint(1, 4)
        random_m = randint(self.m - 3, self.m)
        self.stop_countdown()
        self.ids.countdown_label.text = f"{0:02}:{0:02}"
        self.ids.icon.theme_text_color = "Custom"
        self.ids.countdown_label.opacity = 1
        cell_displayed_list.clear()
        index_list.clear()
        self.revert_color(self)

        for ch in range(len(self.matrix.children)): self.matrix.children[ch].disabled = True

        random_index_list = sample(range(self.n**2), random_m)
        for i in range(random_m):
            self.matrix.children[random_index_list[i]].md_bg_color = color_list[cache_col_index]
            index_list.append(random_index_list[i])
            index_list.sort()

        Clock.schedule_once(self.revert_color, 4.5)
        self.de_activate_menu(True)
        self.ids.start.disabled = True

    def revert_color(self, dt):
        matrix_count = self.n**2
        for ch in range(len(self.matrix.children)): self.matrix.children[ch].disabled = False

        for ch in range(matrix_count): self.matrix.children[ch].md_bg_color = color_list[0]

        if len(index_list) > 0: self.start_countdown()
        self.de_activate_menu(False)
        
class MyGame(MDApp):

    global pause, index_list, countdown_list, color_list
    pause = False
    index_list = []
    countdown_list = [10, 20, 30]
    color_list = ["#8150DE", "#69E2FF", "#FE6694", "#FF9700", "#FFE135"]

    def build(self):
        Builder.load_string(KV)
        self.icon = "icon.png"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.material_style = "M3"
        LabelBase.register(name = "QuickSand", fn_regular = "fonts/Quicksand-SemiBold.ttf", fn_bold = "fonts/Quicksand-Bold.ttf")
        return MainScreen()

if __name__ == "__main__":
    MyGame().run()
