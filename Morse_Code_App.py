from random import choice
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.core.clipboard import Clipboard
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivymd.uix.snackbar.snackbar import Snackbar
from kivy.clock import Clock

KV = '''
ScreenManager:
    MainScreen:
<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Morse Code"
            pos_hint: {"top": 1}

        MDFloatLayout:
            MDTextField:
                id: code_label
                mode: "fill"
                fill_color: 0,0,0,0.5
                hint_text: "Type here..."
                font_size: dp(20)
                pos_hint: {"center_x": 0.5, "y": 0.75}
                size_hint_x: 0.9
                multiline: True
                max_text_length: 50
                on_text: app.main()

            MDCard:
                orientation: "horizontal"
                size_hint: 0.9, 0.55
                padding: dp(5)
                pos_hint: {"center_x": 0.5, "center_y": 0.425}

                MDFloatLayout:
                    MDIcon:
                        icon: "format-size"
                        pos_hint: {"x": 0, "top": 0.985}
                        font_size: dp(36)
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                    MDSwitch:
                        pos_hint: {"center_x": 0.25, "top": 1}
                        on_active: app.check(*args)
                    MDIconButton:
                        icon: "content-copy"
                        pos_hint: {"top": 1, "right": 1}
                        theme_icon_color: "Custom"
                        icon_color: app.theme_cls.primary_color
                        on_release: app.copy_clip()
                    MDLabel:
                        id: label_code
                        text: "Translation"
                        font_size: dp(24)
                        font_name: "QuickSand"
                        bold: True
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                        halign: "center"

            MDIconButton:
                icon: "brightness-4"
                pos_hint: {"x": 0}
                theme_icon_color: "Custom"
                icon_color: app.theme_cls.primary_color
                on_release: app.change_themeStyle()

            MDIconButton:
                icon: "palette"
                pos_hint: {"right": 1}
                theme_icon_color: "Custom"
                icon_color: app.theme_cls.primary_color
                on_release: app.change_themeColor()

'''
class MainScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        self.icon = "assets/icon.png"
        self.theme_cls.primary_palette = "DeepOrange"
        screen = Builder.load_string(KV)
        LabelBase.register(name = "QuickSand", fn_regular = "fonts/Quicksand-Regular.ttf", fn_bold = "fonts/Quicksand-SemiBold.ttf")
        self.main_screen = screen.get_screen("main")
        return screen

    error = 0
    alpha = ['A', 'B','C','D','E','F','G','H','I','J',
         'K','L','M','N','O','P','Q','R','S','T',
         'U','V','W','X','Y','Z','1','2','3','4',
         '5','6','7','8','9','0',' ',',','.','?','!']
    char = [',','?','!']
    morse_code = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....',
                  '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.',
                  '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-',
                  '-.--', '--..', '.----', '..---', '...--', '....-', '.....',
                  '-....', '--...', '---..', '----.', '-----', '/', '--..--',
                  '.-.-.-', '..--..', '-.-.--']    
    palette = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue',
             'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
             'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray',
             'BlueGray']

    def check(self, checkbox, value):
        self.main_screen.ids.label_code.font_size = dp(28) if value else dp(24)

    def copy_clip(self):
        text = self.main_screen.ids.label_code.text
        Clipboard.copy(text)
        if len(text) > 0:
            Snackbar(text = "copied", bg_color = self.theme_cls.primary_color, duration = 1.5).open()

    def change_themeColor(self):
        self.theme_cls.primary_palette = choice(self.palette)

    def change_themeStyle(self):
        mode = self.theme_cls.theme_style
        self.theme_cls.theme_style = "Light" if mode != "Light" else "Dark"
        
    def main(self):
        code = self.main_screen.ids.code_label.text
        max_len = self.main_screen.ids.code_label.max_text_length
        if len(code) <= max_len:
            if any(c.isalnum() for c in code) or any(c in self.char for c in code):
                U_code = code.upper()
                T_List = [*U_code]
                enc = ""
                
                try:
                    for x in range(len(T_List)):
                        enc += (self.morse_code[self.alpha.index(T_List[x])] + " ")

                except ValueError:
                    self.error = 1
                    self.show_Label(code)
                    
                if self.error != 1:
                    self.show_Label(enc)
                self.error = 0

            else:
                R_code = code.replace("_","-")
                M_List = R_code.split()
                dec = ""

                try:
                    for x in range(len(M_List)):
                        dec += (self.alpha[self.morse_code.index(M_List[x])] + "")

                except ValueError:
                    self.error = 1
                    self.show_Label(code)
                    
                if self.error != 1:
                    self.show_Label(dec)
                self.error = 0
        else:
            self.main_screen.ids.label_code.text = ""

    def show_Label(self, text):
        text_field = self.main_screen.ids.code_label.text
        label = self.main_screen.ids.label_code
        label.text = text.title() if len(text_field) > 0 else "Translation"
        
if __name__ == "__main__":
    MainApp().run()

"""
errors/look-outs
format size increase icon UI adjustment

"""

    
