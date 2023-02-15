import os
from kivy.app import App
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import RoundedRectangle, Color
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex as GetColor, platform
from src import CustomWidget, displayTitle

class MainFileChooser(FileChooserListView):
    
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.rparent = parent
        self.font_name = "consolas"
        self.dirselect = True
        self.filters = [lambda _, filename: not filename.endswith('')]
    
    def _show_progress(self):
        self.rparent.show = False
        return super()._show_progress()

    def _hide_progress(self):
        self.rparent.show = True
        return super()._hide_progress()

class CustomFolderButton(CustomWidget):
    
    def __init__(self, name: str, newName: str, **kwargs):
        self.path = name
        newName = newName
        super().__init__((0, 0), (100, Window.height*0.05 if Window.width < Window.height else Window.height*0.1), newName, True, **kwargs)
        self.selector = True
        self.size_hint_y = None
        self.bind(size=self.SizebindCanvas)

    def functions(self):
        wid = self.parent.parent.parent.selected
        if wid is self:
            if platform == "android":
                if not self.path.endswith(self.parent.cusPath):
                    self.path = self.parent.cusPath
            wid.color2.rgb = GetColor(wid.buttonColor)
            self.parent.parent.parent.fileChooser.path = self.path
            self.parent.parent.parent.selected = None            
        else:
            if wid: wid.color2.rgb = GetColor(wid.buttonColor)
            self.parent.parent.parent.selected = self

class CustomFileChooser(Widget):
    
    def __init__(self, cusPath=None, **kwargs):
        super().__init__(**kwargs)
        self.cusPath = cusPath
        self.selected : CustomFolderButton = None
        self.size = Window.size
        self.pos = (0, 0)
        self.show = True
        self.navFileChooser()
    
    def navFileChooser(self):
        displayTitle(self, "JDM FileChooser")
        self.allButtons : list[CustomFolderButton] = list()
        self.grid = GridLayout(size_hint_y=None, cols=1, padding="10dp", spacing="5dp")
        self.scroll = ScrollView(size=(Window.width*0.9, Window.height*0.76),
                                 pos=(Window.width*0.05, Window.height*0.12))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        with self.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.RESULT_BOX), a=0.8)
            RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos, radius=[10, 10, 10, 10])
        self.submitButton = CustomWidget(
            size=((Window.width * 0.4, Window.height*0.05) if Window.width < Window.height else
                (Window.width * 0.38, Window.height*0.08)),
            pos=(Window.width*0.09, ((Window.height - ((Window.height*0.2)*3)) - (Window.height*0.01) - ((((Window.height*0.2) / 4) * 1.5) * (4+1)) )),
            name="Select Folder", autoCall=True
        )
        self.submitButton.func_binder = lambda *_: self.submitLocation()
        self.add_widget(self.submitButton)
        self.closeButton = CustomWidget(
            size=((Window.width * 0.4, Window.height*0.05) if Window.width < Window.height else
                (Window.width * 0.38, Window.height*0.08)),
            pos=(Window.width*0.51, ((Window.height - ((Window.height*0.2)*3)) - (Window.height*0.01) - ((((Window.height*0.2) / 4) * 1.5) * (4+1)) )),
            name="Close", autoCall=True
        )
        self.closeButton.func_binder = lambda *_: self.closeFileChoooser()
        self.add_widget(self.closeButton)
        
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

        self.fileChooser = MainFileChooser(self)
        if self.cusPath: self.fileChooser.path = self.cusPath
        self.fileChooser.bind(files=self.displayAllButtonFiles)
    
    def closeFileChoooser(self):
        parent = self.parent
        self.parent.remove_widget(self)
        parent.re_addAll()

    def submitLocation(self):
        parent = self.parent
        self.parent.mainPath = self.fileChooser.path if not self.selected else self.selected.path 
        self.parent.remove_widget(self)
        parent.saveGraph()

    def on_touch_down(self, touch):
        if self.fileChooser._progress: return False
        return super().on_touch_down(touch)

    def displayAllButtonFiles(self, _, allPath):
        self.grid.clear_widgets()
        self.allButtons.clear()

        if self.show is False:
            for path in allPath:
                newName = os.path.split(path)[1]
                newName = newName if newName else ("./" + newName)
                self.allButtons.append(CustomFolderButton(path, newName))
                self.grid.add_widget(self.allButtons[-1])
        else: self.show = False