from kivy.app import runTouchApp
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex as GetColor

LabelBase.register(
    fn_regular="asset/consolas.ttf",
    name="consolas")

Window.size = (700*0.5, 1400*0.5)
Window.clearcolor = GetColor("333333")
class MainSplash(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.setup_window()
        self.createCanvas()
    
    def createCanvas(self):
        self.add_widget(Label (
            text="JDM Matrix",
            font_size="32sp",
            color=GetColor("888888"),
            font_name="consolas",
            size=(Window.width, Window.height*0.1),
            pos=(0, self.center_y-Window.width*0.6)
        ))

    def setup_window(self):
        self._keyboard = Window.request_keyboard(self._keyboard_close, self)
        self._keyboard.bind(on_key_down=self._keyboard_down_key)

    def _keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._keyboard_down_key)
        self._keyboard = None

    def _keyboard_down_key(self, _, key, *__):
        if key[1] == "s":
            self.export_to_png("presplash.png", 5)

runTouchApp(MainSplash())