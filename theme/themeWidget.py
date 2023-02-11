from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import RoundedRectangle, Color
from matrix import MatrixMenu

from .theme import Theme
from configuration import soundClick
from src.useFulfunction import setCanvas, CustomLabel

class CustomTheme(Widget):
    
    def __init__(self, name:str, source:str, MColor: str, ForeGround: str, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.clicked = False
        self.mColor = MColor
        self.CTheme = name
        self.mainLabel = CustomLabel(name, ForeGround, self.size, self.pos, valign="bottom", halign="center")
        self.mainLabel.bind(size=self.mainLabel.setter("text_size"))
        setCanvas(self, App.get_running_app().CT.CurrentTheme.WHITE + ("" if name != "BLANK" else "44"), MColor)
        with self.canvas:
            self.color = Color(rgb=GetColor("FFFFFF"))
            self.rect3 = RoundedRectangle( source=source, radius=[10, 10, 10, 10])

        self.add_widget(self.mainLabel)
        self.bind(pos=self.change, size=self.change)

    def change(self, *_):
        self.height = self.width
        self.mainLabel.size = self.size
        self.rect1.size = (self.width+(1*2), self.height+(1*2))
        self.rect2.size = self.size
        self.rect3.size = self.size
        self.mainLabel.pos = self.x, self.y - self.mainLabel.font_size
        self.rect1.pos  = (self.x-1, self.y-1)
        self.rect2.pos  = self.pos
        self.rect3.pos  = self.pos
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.parent.parent.parent.inEditor is False:
            self.clicked = True
            soundClick.play()
            self.color2.a = 0.5
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked:
            self.clicked = False
            self.color2.a = 1
            App.get_running_app().restart(self.CTheme)
        return super().on_touch_up(touch)

class ThemeWidget(Widget):
    
    def __init__(self, MatA, MatB, **kwargs):
        super().__init__(**kwargs)
        self.inEditor = False
        self.MatA = MatA
        self.MatB = MatB
        self.allTheme()
        self.displayDesign()
        self.add_widget(MatrixMenu("Theme"))

    def displayDesign(self):
        with self.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.THEME_COLOR), a=0.5)
            RoundedRectangle(
                radius=[10, 10, 10, 10],
                size=(Window.width*0.9, Window.height*0.85),
                pos=(Window.width*0.05, Window.height*0.05))

        self.scroller = ScrollView(
            size_hint=(None, None),
            pos=(Window.width*0.05, Window.height*0.05),
            size=(Window.width*0.9, Window.height*0.85))
        layout = GridLayout(cols=4, padding="10dp", spacing="20dp", size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for t in self.allThemeList:
            layout.add_widget(CustomTheme(*t))

        self.scroller.add_widget(layout)
        self.add_widget(self.scroller)

    def allTheme(self):
        app = App.get_running_app().CT.CurrentTheme
        self.allThemeList = [
            ["ORIGINAL", Theme.ORIGINAL.MAIN_BG_SOURCE, Theme.ORIGINAL.MAIN_BACKGROUND, app.THEME_FG],
            ["HELLOKITTY", Theme.HELLOKITTY.MAIN_BG_SOURCE, Theme.HELLOKITTY.MAIN_BACKGROUND, app.THEME_FG],
            ["JDM", Theme.JDM.MAIN_BG_SOURCE, Theme.JDM.MAIN_BACKGROUND, app.THEME_FG],
            ["GALAXY", Theme.GALAXY.MAIN_BG_SOURCE, Theme.GALAXY.MAIN_BACKGROUND, app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
            ["BLANK", "asset/transparent.png", "00000000", app.THEME_FG],
        ]
