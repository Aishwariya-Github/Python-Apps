import requests
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivymd.toast import toast
##from kivymd.toast.androidtoast.androidtoast import toast

KV = """
MDFloatLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Quote Generator"
        pos_hint: {"top": 1}

    MDTextField:
        id: keyword_input
        mode: "fill"
        fill_color: 0,0,0,0.5
        hint_text: "type your keyword here..."
        helper_text: "e.g., love, success, motivation"
        font_size: dp(20)
        pos_hint: {"center_x": 0.5, "y": 0.775}
        size_hint_x: 0.75
        
    MDCard:
        orientation: "horizontal"
        size_hint: 0.85, 0.625
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"center_x": 0.5, "center_y": 0.425}

        MDLabel:
            id: quote_space
            text: "fetching your quote..."
            font_size: dp(24)
            font_name: "QuickSand"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            halign: "center"

            
    MDFillRoundFlatButton:
        text: "Generate Quote"
        pos_hint: {"center_x": 0.5, "center_y": 0.05}
        on_press: app.get_quote()

"""


class QuoteGeneratorApp(MDApp):
    max_cards_stack = 3
    quote_stack = []
    quote_number = 0
    def build(self):
        
        self.theme_cls.primary_palette = "Teal"
        
        self.theme_cls.material_style = "M3"
        LabelBase.register(name = "QuickSand", fn_regular = "fonts/Quicksand-SemiBold.ttf", fn_bold = "fonts/Quicksand-Bold.ttf")
        return Builder.load_string(KV)

    def reset_quote_space(self, dt = None):
        self.root.ids.quote_space.text = "fetching your quote..."
        self.quote_stack = []
        self.quote_number = 0

    def display_quote(self, dt = None):
        self.root.ids.quote_space.text = self.quote_stack[self.quote_number]
        self.quote_number += 1
        if self.quote_number == self.max_cards_stack:
            self.display_quote_update.cancel()
            Clock.schedule_once(self.reset_quote_space, 10)

    def response(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            quote_data = response.json()
            quote = quote_data["content"]
            self.quote_stack.append(quote)
        else:
            self.quote_stack.append("Failed to fetch quote")

        if len(self.quote_stack) == self.max_cards_stack:
            self.display_quote_update = Clock.schedule_interval(self.display_quote, 10)


    def get_quote(self):
        
        try:

            full_text = self.root.ids.keyword_input.text.strip()

            for _ in range(self.max_cards_stack):
                if full_text:
                    words = full_text.split()
                    keyword = words[0]
                    url = f"https://api.quotable.io/random?tags={keyword}"
                    self.response(url)
                else:
                    url = "https://api.quotable.io/random"
                    self.response(url)
                
        except Exception:
            toast("check your internet connection")
##            toast("check your internet connection", True, 80, 200, 0)
            

if __name__ == "__main__":
    QuoteGeneratorApp().run()

"""
look-outs:
keep android toast during final build.
"""
