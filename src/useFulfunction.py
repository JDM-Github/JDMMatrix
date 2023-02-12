from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import RoundedRectangle, Color, Rectangle
from kivy.utils import get_color_from_hex as GetColor
from configuration import soundClick
from kivy.uix.label import Label
from kivy.uix.widget import Widget

def setCanvas(widget: Widget, color1: str, color2: str, radius : list = [10, 10, 10, 10], Source: str = ""):
    with widget.canvas:
        thickness : int = 1
        widget.color1 = Color(rgba=GetColor(color1))
        widget.rect1 = RoundedRectangle( radius=radius, size=(widget.width+(thickness*2), widget.height+(thickness*2)),
                      pos=(widget.x-thickness, widget.y-thickness) )
        widget.color2 = Color(rgba=GetColor(color2))
        widget.rect2 = RoundedRectangle( source=Source, radius=radius, size=widget.size, pos=widget.pos )

def setCanvas2(widget: Widget, color1: str, radius : list = [10, 10, 10, 10]):
    with widget.canvas:
        widget.color1 = Color(rgb=GetColor(color1))
        widget.rect1 = RoundedRectangle( radius=radius, size=widget.size, pos=widget.pos )

def displayTitle(widget: Widget, text: str):
    widget.title = Label(
        font_size="32sp", font_name="consolas", color=GetColor(App.get_running_app().CT.CurrentTheme.MENU_BUTTON_COLOR),
        size=(Window.width, Window.height*0.1),
        pos=(0, Window.height*0.9), text=text)
    with widget.canvas:
        Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.MENU_COLOR))
        Rectangle(size=widget.title.size, pos=widget.title.pos)
    widget.add_widget(widget.title)

class CustomLabel(Label):
    
    def __init__(self, name: str, Color: str, size: list[int, int], pos: list[int, int], **kwargs):
        super().__init__(**kwargs)
        self.font_name = "consolas"
        self.font_size = "13sp"
        self.color = GetColor(Color)
        self.size = size
        self.pos = pos
        self.text = name 
        self.markup = True

class CustomWidget(Widget):
    def __init__(self, pos: list[int, int], size: list[int, int], name: str, autoCall: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.selector = False
        self.toggleMode = False
        self.activate = False
        self.func_binder = lambda: None
        self.clicked = False
        self.name = name
        self.size = size
        self.pos = pos
        if autoCall:
            self.displayDesign(
            App.get_running_app().CT.CurrentTheme.BUTTON_LINE,
            App.get_running_app().CT.CurrentTheme.BUTTON_COLOR,
            App.get_running_app().CT.CurrentTheme.BUTTON_PRESSED,
            App.get_running_app().CT.CurrentTheme.BUTTON_FG)
            self.bind(pos=self.bindCanvas)
    
    def displayDesign(self, ColorLine: str, Color: str, ColorPressed: str, ColorForeground: str,
                      Radius: list[int, int, int, int] = [10, 10, 10, 10], Source: str = ""):
        self.clear_widgets()
        self.canvas.clear()

        self.buttonLine = ColorLine
        self.buttonColor = Color
        self.buttonPressed = ColorPressed
        self.buttonFG = ColorForeground
        self.mainLabel = CustomLabel(self.name, self.buttonFG, self.size, self.pos, font_name = "consolas")

        setCanvas(self, self.buttonLine, self.buttonColor, Radius, Source)
        self.add_widget(self.mainLabel)
    
    def cfunctions(self):
        if self.toggleMode:
            if self.activate:
                self.activate = False
                self.color2.rgb = GetColor(self.buttonColor)
                return
            self.activate = True
        self.color2.rgb = GetColor(self.buttonPressed)
    def functions(self): ...

    def bindCanvas(self, *_):
        self.mainLabel.pos = self.pos
        self.rect1.pos     = (self.x-1, self.y-1)
        self.rect2.pos     = self.pos
    
    def SizebindCanvas(self, *_):
        self.mainLabel.size = self.size
        self.rect1.size     = (self.width+2, self.height+2)
        self.rect2.size     = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.cfunctions()
            soundClick.play()
            self.clicked = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.clicked:
            self.functions()
            self.func_binder()
            self.clicked = False
            if self.selector is False and self.toggleMode is False:
                if hasattr(self, "color2"): self.color2.rgb = GetColor(self.buttonColor)
        return super().on_touch_up(touch)