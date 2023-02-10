from kivy.app import App
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, ScreenManagerException, NoTransition, SlideTransition

from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty

from .mainMenu import MainMenu
from graph import Graph
from matrix import Matrix
from theme import ThemeWidget

from .exitScreen import ExitScreen

class SM(ScreenManager):
    
    change_Screen = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.old_Screen = "Main"
        self.bind(change_Screen=self.changeScreen)
        self.bind(current=self.checkScreen)

    def checkScreen(self, *_):
        if self.current == "Graph":
            self.parent.graph.setAllCanvas()

    def changeScreen(self, *_):
        self.old_Screen = self.current
        self.transition = SlideTransition()
        if self.change_Screen == "Main":
            self.transition.direction = "right"
        elif self.change_Screen == "Field": self.parent.addField()
        elif self.change_Screen == "Theme": self.parent.addTheme()
        elif self.change_Screen == "Graph":
            self.transition = NoTransition()
            self.parent.addGraph()
        self.current = self.change_Screen

class MainScreenWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        with self.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.MAIN_BACKGROUND))
            Rectangle(size=self.size)
            self.CmainBg = Color(rgba=GetColor("ffffff66"))
            self.mainBg = Rectangle(size=self.size, source=App.get_running_app().CT.CurrentTheme.MAIN_BG_SOURCE)
        self.allScreen()
        self.exitScreen = ExitScreen()
        self.add_widget(self.exitScreen)

    def addField(self, theme: bool = False):
        if not hasattr(self, "ScreenMatrixFunctions"):
            self.ScreenMatrixFunctions = Screen(name="Field")
            self.MatrixFunctions = Matrix()
            self.ScreenMatrixFunctions.add_widget(self.MatrixFunctions)
            if theme is False: self.sm.add_widget(self.ScreenMatrixFunctions)

    def addTheme(self):
        if not hasattr(self, "ScreenMatrixTheme"):
            self.addField(True)    
            self.ScreenMatrixTheme = Screen(name="Theme")
            self.MatrixTheme = ThemeWidget(
                self.MatrixFunctions.firstMatrixHolder,
                self.MatrixFunctions.secondMatrixHolder)
            self.ScreenMatrixTheme.add_widget(self.MatrixTheme)
            self.sm.add_widget(self.ScreenMatrixTheme)
            try: self.sm.add_widget(self.ScreenMatrixFunctions)
            except ScreenManagerException: pass

    def addGraph(self):
        if not hasattr(self, "ScreenGraph"):
            self.ScreenGraph = Screen(name="Graph")
            self.graph = Graph()
            self.ScreenGraph.add_widget(self.graph)
            self.sm.add_widget(self.ScreenGraph)

    def allScreen(self):
        config = App.get_running_app().Matrixconfig
        current_Screen = config.get("CurrentScreen")

        self.sm = SM(size=Window.size)
        self.ScreenMainMenu = Screen(name="Main")
        self.MainMenu = MainMenu()
        self.ScreenMainMenu.add_widget(self.MainMenu)
        self.add_widget(self.sm)
        
        if current_Screen == "Main" or current_Screen is None: self.sm.add_widget(self.ScreenMainMenu)

        self.sm.change_Screen = current_Screen if current_Screen else "Main"
        self.sm.old_Screen = config.get("LastScreen") if config.get("LastScreen") else "Main"

        if current_Screen != "Main" and current_Screen is not None: self.sm.add_widget(self.ScreenMainMenu)
