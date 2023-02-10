from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, Color

from src import setCanvas, CustomWidget, CustomLabel

class ExitScreen(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isExitScreen = False
        if Window.width < Window.height: self.size = (Window.width*0.8+15, ((Window.height*0.2) / 4)*3+10)
        else: self.size = (Window.height*0.8+15, ((Window.width*0.2) / 4)*3+10)
        self.pos = (0, -Window.height)

        app = App.get_running_app()
        self.displayDesign(
            app.CT.CurrentTheme.EXIT_LINE,
            app.CT.CurrentTheme.EXIT_COLOR,
            app.CT.CurrentTheme.EXIT_FG)
        self.bind(pos=self.bindCanvas)

    def displayDesign(self, ColorLine: str, MainColor: str, ColorForeground: str):
        self.clear_widgets()
        self.canvas.clear()
        
        self.exitLine = ColorLine
        self.exitColor = MainColor
        self.labelFG = ColorForeground
        self.mainLabel = CustomLabel("Are you sure you want to Exit?", self.labelFG, self.size, self.pos)

        with self.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.WINDOW_BACKGROUND), a=0.5)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        setCanvas(self, self.exitLine, self.exitColor)
        self.add_widget(self.mainLabel)
        self.allButton()

    def bindCanvas(self, *_):
        margin = self.width*0.05
        self.rect.pos      = (0, 0) if self.isExitScreen else self.pos
        self.rect1.pos     = (self.x-1, self.y-1)
        self.rect2.pos     = self.pos
        self.mainLabel.pos = (self.x, self.y+margin*2)
        self.Econfirm.pos  = self.x+margin, self.y+5
        self.Ecancel.pos   = self.right-self.Ecancel.width-margin, self.y+5

    def allButton(self):
        self.Econfirm = CustomWidget(
            pos = (-Window.width, -Window.height),
            size = (
                ((Window.width*0.3), ((Window.height*0.2) / 4)) if Window.width < Window.height else
                ((Window.height*0.3), ((Window.width*0.2) / 4))),
            name= "Confirm")
        self.Ecancel = CustomWidget(
            pos = (-Window.width, -Window.height),
            size = (
                ((Window.width*0.3), ((Window.height*0.2) / 4)) if Window.width < Window.height else
                ((Window.height*0.3), ((Window.width*0.2) / 4))),
            name= "Cancel")

        self.Econfirm.func_binder = lambda : App.get_running_app().stop()
        self.Ecancel.func_binder = lambda : self.close()
        self.add_widget(self.Econfirm)
        self.add_widget(self.Ecancel)

    def show(self):
        self.isExitScreen = True
        self.parent.MatrixFunctions.disabledFunction = True
        self.parent.MatrixFunctions.disabledResult = True
        self.parent.MatrixFunctions.disabledMenu = True
        self.pos = Window.width/2-self.width/2, Window.height/2-self.height/2

    def close(self):
        self.isExitScreen = False
        self.parent.MatrixFunctions.disabledMenu = False
        self.parent.MatrixFunctions.disabledFunction = False
        self.parent.MatrixFunctions.disabledResult = False
        self.pos = (0, -Window.height)
