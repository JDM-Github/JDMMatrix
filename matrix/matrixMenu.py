from kivy.app import App
from plyer import orientation
from kivy.utils import platform
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from configuration import soundClick
from src import setCanvas2, CustomWidget, CustomLabel, Toast
from theme import ThemeEditor

class MenuButton(CustomWidget):

    def __init__(self, num: int, name: str, screen: str = "Field", **kwargs):
        size = (((((Window.width*0.9)/5), ((Window.height*0.2) / 4))) if Window.width < Window.height else
                ((((Window.width*0.9)/8), ((Window.width*0.2) / 6))))
        pos= (Window.width*0.05 + size[0] * (num-1), Window.height - size[1])
        super().__init__(pos, size, name, False, **kwargs)
        self.screen = screen
        self.displayDesign(
            App.get_running_app().CT.CurrentTheme.MENU_BUTTON_COLOR,
            App.get_running_app().CT.CurrentTheme.MENU_BUTTON_PRESSED)

    def displayDesign(self, Color: str, ColorPressed: str):
        self.buttonColor = Color
        self.buttonPressed = ColorPressed
        self.mainLabel = CustomLabel(self.name, Color, self.size, self.pos)
        self.add_widget(self.mainLabel)
    
    def functions(self): self.mainLabel.color = GetColor(self.buttonColor)
    def cfunctions(self): self.mainLabel.color = GetColor(self.buttonPressed)
    
    def on_touch_down(self, touch):
        if self.screen == "Field":
            if self.parent.parent.disabledMenu is False:
                super().on_touch_down(touch)
        else:
            if self.parent.parent.inEditor is False:
                super().on_touch_down(touch)

class MatrixMenu(Widget):

    def __init__(self, name: str = "Field", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.size = (Window.width, ((Window.height*0.2) / 4) if Window.width < Window.height else ((Window.width*0.2) / 6))
        self.pos = (0, Window.height - self.height)
        self.isMenuOpen = False
        setCanvas2(self, App.get_running_app().CT.CurrentTheme.MENU_COLOR, [0, 0, 0, 0])
        self.allButton()
        self.allWidgets()

    def allWidgets(self):
        self.themeEditor = ThemeEditor()

    def allButton(self):
        Rmax = 5 if Window.width < Window.height else 8
        if self.name == "Field":
            self.menuBtn = MenuButton(1, "Menu", self.name)
            self.rotateBtn = MenuButton(2, "Rotate", self.name)
            self.changeTheme = MenuButton(Rmax-1, "Theme", self.name)
            self.soundBtn = MenuButton(Rmax, "Sound", self.name)
            self.menuBtn.func_binder = lambda : setattr(self.parent.parent.parent, "change_Screen", "Main")
            self.rotateBtn.func_binder = lambda : self.changeWindow()
            self.changeTheme.func_binder = lambda : self.changeThemeFunc()
            self.soundBtn.func_binder = lambda : self.changeSound()
            self.add_widget(self.menuBtn)
            self.add_widget(self.rotateBtn)
            self.add_widget(self.changeTheme)
            self.add_widget(self.soundBtn)
        else:
            self.changeTheme = MenuButton(Rmax, "Back", self.name)
            self.EditCurrent = MenuButton(Rmax - 1, "Edit", self.name)
            self.changeTheme.func_binder = lambda : self.changeThemeFunc()
            self.EditCurrent.func_binder = lambda : self.showThemeEditor()
            self.add_widget(self.changeTheme)
            self.add_widget(self.EditCurrent)

    def showThemeEditor(self):
        Toast("Not implemented yet.").start()
        return
        self.parent.inEditor = True
        with self.canvas:
            self.editorCol = Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.WINDOW_BACKGROUND), a=0.8)
            self.editorBG = Rectangle(size=Window.size)
        self.add_widget(self.themeEditor)

    def changeWindow(self):
        if platform == "android":
            self.oldWidth = Window.width
            App.get_running_app().realWidget.clear_widgets()
            if Window.width < Window.height:
                orientation.set_landscape()
                self.clockM = Clock.schedule_interval(lambda _: self.checkLandscape(), 1/60)
            else:
                orientation.set_portrait()
                self.clockM = Clock.schedule_interval(lambda _: self.checkPortrait(), 1/60)
        else:
            Window.size = (Window.height, Window.width)
            App.get_running_app().restart(App.get_running_app().Matrixconfig.get("CurrentTheme"))

    def checkPortrait(self):
        if Window.width < self.oldWidth:
            self.clockM.cancel()
            App.get_running_app().restart(App.get_running_app().Matrixconfig.get("CurrentTheme"))

    def checkLandscape(self):
        if Window.width > self.oldWidth:
            self.clockM.cancel()
            App.get_running_app().restart(App.get_running_app().Matrixconfig.get("CurrentTheme"))

    def changeSound(self): soundClick.volume = int(not soundClick.volume)
    def changeThemeFunc(self): 
        self.parent.parent.manager.transition.direction = "left" if self.name == "Field" else "right"
        self.parent.parent.manager.change_Screen = "Theme" if self.name == "Field" else self.parent.parent.parent.old_Screen
