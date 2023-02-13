import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.utils import get_color_from_hex as GetColor
from kivy.metrics import dp
from kivy.graphics import Color, Line

class Nodes(Widget):

    def __init__(self, pos, node, invisible, **kwargs):
        super().__init__(**kwargs)
        self.invisible = invisible
        self.node = node
        self.position = pos
        self.size = (dp(15), dp(15))
        self.displayLabelPos()

    def displayLabelPos(self):
        self.label = Label(
            color=GetColor(App.get_running_app().CT.CurrentTheme.GRAPH_ARROW_TEXT), text=str(self.position),
            pos=(self.x, self.y+dp(10)), size=self.size,
            font_name = "consolas"
        )
        self.bind(pos=self.changePos)

    def changePos(self, *_):
        self.label.pos = self.x, self.y-dp(20)
    
    def setPosition(self):
        parent = self.parent.parent.parent
        if parent:
            self.x = parent.cameraX+parent.pos_[0]+parent.width_/2 + (self.position[0]*parent.blockPadding) - self.width/2
            self.y = parent.cameraY+parent.pos_[1]+parent.height_/2 + (self.position[1]*parent.blockPadding) - self.height/2
            if self.parent.changeMode:
                if parent.line_selected is self.parent:
                    self.label.text = str(f"({round(round(self.position[0]*100, 2)/100, 1)}, {round(round(self.position[1]*100, 2)/100, 1)})")
                self.parent.changeLine()
                self.parent.changeAngleLabel()

    def on_touch_down(self, touch):
        parent = self.parent.parent.parent        
        if self.invisible: return super().on_touch_down(touch)
        if parent.fileChooserOpened: return super().on_touch_down(touch)
        if not self.collide_point(*touch.pos): return super().on_touch_down(touch)
        if parent.grabbing is None:
            parent.grabbing = self
            self.old_X = self.position[0]
            self.old_Y = self.position[1]
            self.grabX = touch.x
            self.grabY = touch.y
            parent.de_Select_line()

            parent.setGridValue(self.parent)
            self.parent.arrow.img.color = GetColor(App.get_running_app().CT.CurrentTheme.GRAPH_ARROW_ACTIVE)
            self.parent.color.rgb = GetColor(App.get_running_app().CT.CurrentTheme.GRAPH_ARROW_ACTIVE)
            if parent.show_Coords is False:
                self.parent.node1.add_widget(self.parent.node1.label)
                self.parent.node2.add_widget(self.parent.node2.label)
            parent.line_selected = self.parent
        return super().on_touch_down(touch)

    def updateBind(self):
        parent = self.parent.parent.parent
        index = parent.all_nodes_line.index(self.parent)
        for i in range(len(parent.binderVec.allBinder)):
            if parent.binderVec.allBinder[i][0] == index or parent.binderVec.allBinder[i][1] == index:
                parent.updateBinderInvisibleFirst(i)
                parent.updateBinderInvisibleSecond(i)
                parent.updateBinderInvisibleThird(i)
                parent.updateBinderInvisibleFouth(i)
                break

    def on_touch_move(self, touch):
        if self.invisible: return super().on_touch_move(touch)
        parent = self.parent.parent.parent
        if parent.grabbing is self:
            self.position = ((self.old_X*parent.blockPadding + (touch.x - self.grabX)) / parent.blockPadding,
                             (self.old_Y*parent.blockPadding + (touch.y - self.grabY)) / parent.blockPadding)
            self.setPosition()
            self.updateBind()
            self.parent.parent.parent.setGridValue(self.parent)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.invisible: return super().on_touch_up(touch)
        if self.parent.parent.parent.grabbing is self:
            self.parent.parent.parent.grabbing = None
            self.position = (round(round(self.position[0]*100, 2)/100, 1),
                             round(round(self.position[1]*100, 2)/100, 1))
            self.setPosition()
            self.updateBind()
            self.parent.parent.parent.setGridValue(self.parent)
        return super().on_touch_up(touch)

class Arrow(Scatter):
    
    def __init__(self, pos, **kwargs):
        super().__init__(**kwargs)
        self.size = (1, 1)
        self.pos = pos
        self.disabled = True
        self.auto_bring_to_front = False
        self.img = Image(
            color=GetColor(App.get_running_app().CT.CurrentTheme.GRAPH_ARROW_NACTIVE),
            size=(dp(25), dp(20)), pos=(dp(18)*-0.04, dp(10)*-0.04),
            source="asset/triangle.png", opacity=1
        )
        self.add_widget(self.img)

class NodeLine(Widget):
    
    def __init__(self, invisible=False, pos1=(1, 1), pos2=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.invisible = invisible
        self.angle : int = 0
        self.changeMode = True
        self.node1 = Nodes(pos1, 1, invisible)
        self.node2 = Nodes(pos2, 2, invisible)
        self.arrow = Arrow(self.node1.pos)
        self.add_widget(self.node1)
        self.add_widget(self.node2)
        self.add_widget(self.arrow)
        self.displayLineName()
        self.displayLine()
        Clock.schedule_once(lambda *_: self.update2NodePosAngle(), 0)
    
    def displayLineName(self):
        if self.invisible is False:
            self.name_Label = Label(
                font_size=dp(20),
                font_name="consolas", size=(dp(30), dp(30)),
                color=GetColor(App.get_running_app().CT.CurrentTheme.GRAPH_ARROW_TEXT))
            self.add_widget(self.name_Label)

    def getSlope(self, x1, x2, y1, y2):
        dx = x2 - x1
        dy = y2 - y1
        theta = math.atan2(dy, dx)
        theta *= 180 / math.pi
        self.angle = theta + 180
        return theta - 29

    def update2Nodeposition(self):
        self.changeMode = False
        self.node1.setPosition()
        self.node2.setPosition()
        self.changeMode = True
        self.changeLine()
    
    def update2NodePosAngle(self):
        self.update2Nodeposition()
        self.changeAngleLabel()

    def displayLine(self):
        with self.canvas:
            self.color = Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.GRAPH_ARROW_NACTIVE), a=0.5)
            self.line = Line(width=dp(2) if self.invisible is False else dp(1.5))

    def changeLine(self):
        self.arrow.pos = self.node1.x+(self.node1.width/2), self.node1.y+(self.node1.height/2)
        self.line.points=[*self.arrow.pos, self.node2.x+(self.node2.width/2), self.node2.y+(self.node2.height/2)]
        if self.invisible is False:
            self.name_Label.pos = ((self.node1.x+self.node2.x)/2 - dp(15), (self.node1.y+self.node2.y)/2 - dp(15))

    def changeAngleLabel(self):
        if self.parent:
            if self.parent.parent.line_selected is self:
                self.parent.parent.updateAllStats()
        self.arrow.rotation = self.getSlope(self.node1.x, self.node2.x, self.node1.y, self.node2.y)