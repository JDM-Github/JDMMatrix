from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from kivy.metrics import sp
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock

class Toast(Widget):

    def __init__(self, message: str, duration: float = 1.5, gravity: float = (Window.height*0.1 if Window.width < Window.height else Window.height*0.05), 
                 textColor: str = "FFFFFF", Color: str = None, opacity: float = 1, **kwargs):
        super().__init__(**kwargs)
        self.fSize = sp(15)
        self.textColor = textColor
        self.Tcolor = Color if Color else App.get_running_app().CT.CurrentTheme.RESULT_BOX
        self.Topacity = opacity
        self.message = message
        self.duration = duration
        self.gravity = gravity

    def start(self, widget: Widget = None):
        widget = widget if widget else App.get_running_app().realWidget
        widget.add_widget(self)
        with self.canvas:
            size = (self.fSize*(len(self.message)/2)+(self.fSize*2), self.fSize*1.3)
            pos = Window.width / 2 - size[0] / 2, self.gravity-(self.fSize*0.3/2)
            Color(rgb=GetColor("FFFFFF"))
            RoundedRectangle(radius=[10, 10, 10, 10],size=(size[0]+2, size[1]+2), pos=(pos[0]-1, pos[1]-1))
            Color(rgb=GetColor(self.Tcolor), a=self.Topacity)
            RoundedRectangle(radius=[10, 10, 10, 10],size=size, pos=pos)
        self.add_widget(Label(text=self.message, font_size=self.fSize, size=(Window.width, self.fSize), pos=(0, self.gravity)))
        
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *_: self.stop(widget))
        Clock.schedule_once(lambda _: anim.start(self), self.duration)

    def stop(self, widget: Widget):
        self.clear_widgets()
        widget.remove_widget(self)
