from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.utils import get_color_from_hex as GetColor

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from src import CustomWidget

class Custom(CustomWidget):

    def __init__(self, name: str, **kwargs):
        super().__init__((0, 0), (100, Window.height*0.05 if Window.width < Window.height else Window.height*0.1), name, True, **kwargs)
        self.size_hint_y = None
        self.bind(size=self.SizebindCanvas)

class MainMenu(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.displayTitle()
        self.displayModes()
    
    def displayTitle(self):
        self.title = Label(
            font_size="32sp", font_name="consolas", color=GetColor(App.get_running_app().CT.CurrentTheme.MENU_BUTTON_COLOR),
            size=(Window.width, Window.height*0.1),
            pos=(0, Window.height*0.9), text="JDM Matrix")
        
        with self.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.MENU_COLOR))
            Rectangle(size=self.title.size, pos=self.title.pos)
        self.add_widget(self.title)

    def displayModes(self):
        self.grid = GridLayout(size_hint_y=None, cols=1, padding="10dp", spacing="5dp")
        self.scroll = ScrollView(size=(Window.width*0.9, Window.height*0.83),
                                 pos=(Window.width*0.05, Window.height*0.05))
        with self.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.RESULT_BOX), a=0.8)
            RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos, radius=[10, 10, 10, 10])
        
        self.matrixMode = Custom("Matrix Mode")
        self.matrixMode.func_binder = lambda : self.changeScreen("Field")
        self.themeMode = Custom("Change Theme")
        self.themeMode.func_binder = lambda : self.changeScreen("Theme")
        self.vectorMode = Custom("Vector Mode")
        # self.vectorMode.func_binder = lambda : self.changeScreen("Vector")
        self.graphMode = Custom("Graph Mode")
        self.graphMode.func_binder = lambda : self.changeScreen("Graph")
        
        self.grid.add_widget(self.themeMode)
        self.grid.add_widget(self.matrixMode)
        self.grid.add_widget(self.vectorMode)
        self.grid.add_widget(self.graphMode)
        
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)
    
    def changeScreen(self, name: str):
        self.parent.parent.transition.direction = "left"
        self.parent.parent.change_Screen = name
