from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.utils import get_color_from_hex as GetColor

from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from src import CustomWidget, displayTitle, changeWindow, changeSound

class Custom(CustomWidget):

    def __init__(self, name: str, **kwargs):
        super().__init__((0, 0), (100, Window.height*0.05 if Window.width < Window.height else Window.height*0.1), name, True, **kwargs)
        self.size_hint_y = None
        self.bind(size=self.SizebindCanvas)

class MainMenu(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        displayTitle(self, "JDM Matrix")
        self.displayModes()
        self.displayBottomButton()

    def displayModes(self):
        self.grid = GridLayout(size_hint_y=None, cols=1, padding="10dp", spacing="5dp")
        self.scroll = ScrollView(size=(Window.width*0.9, Window.height*0.73),
                                 pos=(Window.width*0.05, Window.height*0.15))
        with self.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.RESULT_BOX), a=0.8)
            RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos, radius=[10, 10, 10, 10])
        
        
        self.matrixMode = Custom("Matrix Mode")
        self.matrixMode.func_binder = lambda : self.changeScreen("Field")
        self.vectorMode = Custom("Vector Mode")
        # self.vectorMode.func_binder = lambda : self.changeScreen("Vector")
        self.graphMode = Custom("Graph Mode")
        self.graphMode.func_binder = lambda : self.changeScreen("Graph")
        
        self.grid.add_widget(self.matrixMode)
        self.grid.add_widget(self.vectorMode)
        self.grid.add_widget(self.graphMode)
        
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)
    
    def displayBottomButton(self):
        self.resetConfig = Custom("Reset Config")
        self.themeMode = Custom("Change Theme")
        self.rotateScreen = Custom("Rotate")
        self.Changesound = Custom("Sound")
        self.Changesound.func_binder = lambda : changeSound()
        self.rotateScreen.func_binder = lambda : changeWindow(self)
        self.themeMode.func_binder = lambda : self.changeScreen("Theme")
        
        self.allBottomButton = GridLayout(
            size=(Window.width, (Window.height*0.05 if Window.width < Window.height else Window.height*0.1)+dp(20)),
            padding=dp(10), spacing=dp(10), rows=1,
        )
        self.allBottomButton.add_widget(self.resetConfig)
        self.allBottomButton.add_widget(self.themeMode)
        self.allBottomButton.add_widget(self.rotateScreen)
        self.allBottomButton.add_widget(self.Changesound)
        self.add_widget(self.allBottomButton)
    
    def changeScreen(self, name: str):
        self.parent.parent.transition.direction = "left"
        self.parent.parent.change_Screen = name
