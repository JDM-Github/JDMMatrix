from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.graphics import RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from src import CustomWidget, displayTitle

class BindInterfaceButton(CustomWidget):
    
    def __init__(self, name: str, index : int, **kwargs):
        self.index = index
        super().__init__((0, 0), (100, Window.height*0.05 if Window.width < Window.height else Window.height*0.1), name, True, **kwargs)
        self.selector = True
        self.size_hint_y = None
        self.bind(size=self.SizebindCanvas)

    def functions(self):
        wid = self.parent.parent.parent.parent.selected
        if wid is self:
            wid.color2.rgb = GetColor(wid.buttonColor)
            self.parent.parent.parent.parent.selectVector()
        else:
            if wid: wid.color2.rgb = GetColor(wid.buttonColor)
            self.parent.parent.parent.parent.selected = self

class BindInterface(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = ((Window.width*0.9, Window.height*0.3) if Window.width < Window.height else 
                     (Window.height*0.9, Window.width*0.3))
        self.pos = (Window.width*0.5-self.width/2,
                    Window.height*0.88-self.height)
        self.selected = None
        self.AccessingVec = None
        self.gridChooser = False
        self.allCustomButt = Widget()
        self.gridWidget = Widget()
        self.currentAccess = 0
        self.allBinder = [(None, None)]
        with self.allCustomButt.canvas:
            Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.RESULT_BOX), a=0.8)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[10, 10, 10, 10])
        displayTitle(self, "JDM Binder")
        self.allButtons()

    def allButtons(self):
        self.first = CustomWidget(
            (self.x + dp(10), self.top-(self.height/4)+dp(5)),
            (self.width*0.6, self.height/4-(dp(10))),
            "Select First Vector", True)
        self.nextVec = CustomWidget(
            (self.x + dp(20)+self.width*0.6, self.top-(self.height/4)+dp(5)),
            (self.width*0.4-dp(30), self.height/4-(dp(10))),
            "Next", True)
        self.second = CustomWidget(
            (self.x + dp(10), self.top-(self.height/4*2)+dp(5)),
            (self.width*0.6, self.height/4-(dp(10))),
            "Select Second Vector", True)
        self.prevVec = CustomWidget(
            (self.x + dp(20)+self.width*0.6, self.top-(self.height/4*2)+dp(5)),
            (self.width*0.4-dp(30), self.height/4-(dp(10))),
            "Previous", True)
        self.addition = CustomWidget(
            (self.x + dp(10), self.top-(self.height/4*3)+dp(5)),
            (self.width-dp(20), self.height/4-(dp(10))),
            "Addition", True)
        self.subtraction = CustomWidget(
            (self.x + dp(10), self.top-(self.height/4*4)+dp(5)),
            (self.width-dp(20), self.height/4-(dp(10))),
            "Subtraction", True)

        self.allCustomButt.add_widget(self.first)
        self.first.func_binder = lambda *_: self.displayGrid("F")
        self.allCustomButt.add_widget(self.nextVec)

        self.allCustomButt.add_widget(self.second)
        self.second.func_binder = lambda *_: self.displayGrid("S")
        self.allCustomButt.add_widget(self.prevVec)

        self.addition.toggleMode = True
        self.allCustomButt.add_widget(self.addition)
        self.subtraction.toggleMode = True
        self.allCustomButt.add_widget(self.subtraction)
        self.add_widget(self.allCustomButt)

    def displayGrid(self, access):
        self.AccessingVec = access
        self.remove_widget(self.allCustomButt)
        self.remove_widget(self.gridWidget)
        self.gridChooser = True

        if not hasattr(self, "grid"):
            self.allButtons = list()
            self.grid = GridLayout(size_hint_y=None, cols=1, padding="10dp", spacing="5dp")
            self.scroll = ScrollView(size=(Window.width*0.9, Window.height*0.76),
                                     pos=(Window.width*0.05, Window.height*0.12))
            self.grid.bind(minimum_height=self.grid.setter('height'))
            with self.gridWidget.canvas:
                Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.RESULT_BOX), a=0.8)
                RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos, radius=[10, 10, 10, 10])
            self.submitButton = CustomWidget(
                size=((Window.width * 0.4, Window.height*0.05) if Window.width < Window.height else
                    (Window.width * 0.38, Window.height*0.08)),
                pos=(Window.width*0.09, ((Window.height - ((Window.height*0.2)*3)) - (Window.height*0.01) - ((((Window.height*0.2) / 4) * 1.5) * (4+1)) )),
                name="Select Vector", autoCall=True
            )
            self.submitButton.func_binder = lambda *_: self.selectVector()
            self.closeButton = CustomWidget(
                size=((Window.width * 0.4, Window.height*0.05) if Window.width < Window.height else
                    (Window.width * 0.38, Window.height*0.08)),
                pos=(Window.width*0.51, ((Window.height - ((Window.height*0.2)*3)) - (Window.height*0.01) - ((((Window.height*0.2) / 4) * 1.5) * (4+1)) )),
                name="Close", autoCall=True
            )
            self.closeButton.func_binder = lambda *_: self.closeVectorList()

            self.gridWidget.add_widget(self.submitButton)
            self.gridWidget.add_widget(self.closeButton)        
            self.scroll.add_widget(self.grid)
            self.gridWidget.add_widget(self.scroll)
        self.grid.clear_widgets()
        self.displayAllButton()
        self.add_widget(self.gridWidget)

    def displayAllButton(self):
        for i, node in enumerate(self.parent.all_nodes_line):
            self.grid.add_widget(BindInterfaceButton(node.name_Label.text, i))

    def selectVector(self):
        if self.selected:
            if self.AccessingVec == 'F':
                if self.selected.name == self.second.mainLabel.text: return
                self.first.mainLabel.text = self.selected.name
                self.allBinder[self.currentAccess] = (self.selected.index, self.allBinder[self.currentAccess][1])
            elif self.AccessingVec == 'S':
                if self.selected.name == self.first.mainLabel.text: return
                self.second.mainLabel.text = self.selected.name
                self.allBinder[self.currentAccess] = (self.allBinder[self.currentAccess][0], self.selected.index)
            self.closeVectorList()

    def closeVectorList(self):
        self.selected = None
        self.gridChooser = False
        self.AccessingVec = None
        self.remove_widget(self.gridWidget)
        self.add_widget(self.allCustomButt)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos) and self.gridChooser is False:
            self.parent.openBinder()
        return super().on_touch_down(touch)