from kivy.app import runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex as GetColor

LabelBase.register(
    fn_regular="asset/consolas.ttf",
    name="consolas")

Window.size = (200, 200)

class IconWidget(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.setup_window()
        self.createCanvas()
    
    def createCanvas(self): ...
        # with self.canvas:
            
        #     Color(rgb=GetColor("0098f9"))
        #     Ellipse(size=self.size)
        #     Color(rgba=GetColor("FFFFFF66"))
        #     Rectangle(size=(Window.width*0.6, Window.height*0.6),
        #               pos=(Window.width*0.5-(Window.width*0.3), Window.width*0.5-(Window.width*0.3)+10),
        #               source="asset/iconInverted.png")
        
        # self.add_widget(Label (
        #     text="[color=cccccc]JDM[/color][color=333333]M[/color]",
        #     markup=True,
        #     font_size="64sp",
        #     font_name="consolas",
        #     size=(Window.width, Window.height*0.1),
        #     pos=(0, self.center_y-Window.width*0.1-45)
        # ))
        # self.add_widget(Label (
        #     text="[color=ffffff]JDM[/color][color=777777]M[/color]",
        #     markup=True,
        #     font_size="64sp",
        #     font_name="consolas",
        #     size=(Window.width, Window.height*0.1),
        #     pos=(-3, self.center_y-Window.width*0.1-43)
        # ))

    def setup_window(self):
        self._keyboard = Window.request_keyboard(self._keyboard_close, self)
        self._keyboard.bind(on_key_down=self._keyboard_down_key)

    def _keyboard_close(self):
        self._keyboard.unbind(on_key_down=self._keyboard_down_key)
        self._keyboard = None

    def _keyboard_down_key(self, _, key, *__):
        if key[1] == "s":
            self.export_to_png("asset/mainBg.png", 5)
    

if __name__ == "__main__":
    runTouchApp(IconWidget())