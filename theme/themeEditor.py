from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

from src.useFulfunction import setCanvas

class ThemeEditor(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.width*0.95, Window.height*0.95
        self.pos = Window.width*0.025, Window.height*0.025
        self.displayDesign()
    
    def displayDesign(self):
        app = App.get_running_app()
        setCanvas(self, app.CT.CurrentTheme.RESULT_LINE, app.CT.CurrentTheme.RESULT_BOX, [20, 20, 20, 20])

