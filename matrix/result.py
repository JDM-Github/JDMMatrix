import copy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation
from kivy.utils import get_color_from_hex as GetColor

from kivy.metrics import sp
from .matrixHolder import MatrixHolder
from src import setCanvas, CustomWidget, Toast


import numpy as np
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

class LineLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True
        self.halign = "left"
        self.valign = "center"
        self.font_name = "consolas"
        self.bind(size=self.setter("text_size"))
        self.color = GetColor(App.get_running_app().CT.CurrentTheme.NORMAL_COLOR)

class CustomButton(CustomWidget):

    def __init__(self, name: str, radius=[0, 0, 0, 0], **kwargs):
        Rmax = 6
        size = ((Window.width*0.8) / Rmax, ((Window.height*0.2) / 4) if Window.width < Window.height else ((Window.width*0.2) / 4))
        pos = (-200, -200)
        super().__init__(pos, size, name, True, radius, **kwargs)

    def on_touch_down(self, touch):
        if self.parent.parent.disabledResult is False:
            super().on_touch_down(touch)


class MatrixScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resultList = [33, 28, 36, 6, 31, 5, 14, -2, 26]
        self.resultRows = 3 
        self.resultCols = 3 
        self.printResult()

    def printResult(self):
        layout = BoxLayout(orientation='vertical')
        layout.size_hint = (None, None)
        layout.size = Window.size

        flattened_matrix = self.resultList
        rows, cols = self.resultRows, self.resultCols
        matrix = np.array(flattened_matrix).reshape(rows, cols)

        fig = plt.figure(figsize=(Window.width / 100, Window.height / 100)) 
        ax = fig.add_subplot(111, projection='3d')

        x = np.arange(cols)
        y = np.arange(rows)
        x, y = np.meshgrid(x, y)
        z = matrix 

        ax.plot_surface(x, y, z, cmap="coolwarm", edgecolor='k')  # Use 3D surface plot

        ax.set_title('3D Matrix Visualization', fontsize=18, color='white')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Value')

        fig.colorbar(ax.plot_surface(x, y, z, cmap="coolwarm", edgecolor='k'))

        canvas = FigureCanvasAgg(fig)
        canvas.print_figure("matrix_plot_3d.png", dpi=100)

        img = Image(source="matrix_plot_3d.png", size_hint=(None, None), size=(Window.width, Window.height))
        layout.add_widget(img)

        # back_button = Button(text="Back", size_hint=(None, None), size=(100, 50), pos_hint={'top': 1, 'right': 1})
        # back_button.bind(on_press=self.go_back)
        # layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main_screen'




class MatrixResultBox(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos = (0, -Window.height)
        self.size = (Window.width, Window.height*0.95)
        self.isColoredText = False
        self.displayDesign(
            App.get_running_app().CT.CurrentTheme.RESULT_LINE,
            App.get_running_app().CT.CurrentTheme.RESULT_BOX)

    def displayDesign(self, ColorLine: str, Color: str):
        self.clear_widgets()
        self.canvas.clear()
        
        setCanvas(self, ColorLine, Color, [20, 20, 20, 20])
        self.displaySomeButton()
        self.allVariables()
        self.displayResult()
        self.bind(pos=self.bindCanvas)

    def bindCanvas(self, *_):
        self.rect1.pos = (self.x-1, self.y-1)
        self.rect2.pos = self.pos
        Rmax = 6
        width = ((Window.width*0.8) / Rmax) + 5
        margin = (Window.width / 2) - ((width * Rmax) / 2) + 2.5
        self.copyClipboard.pos = (self.x+margin, self.y+5)
        self.clearClipboard.pos = (self.x+margin+width, self.y+5)
        self.toMatrixA.pos = (self.x+margin+width*2, self.y+5)
        self.toMatrixB.pos = self.x+margin+width*3, self.y+5
        self.coloredStr.pos = self.x+margin+width*4, self.y+5
        self.resultStr.pos = self.x+margin+width*5, self.y+5
        self.scroller.pos = (self.x+5, self.y+5)

    def showResult(self):
        self.isFullSize = True
        self.parent.disabledFunction = True
        self.parent.disabledHolder = True
        self.parent.openResult.mainLabel.text = "CLOSE RESULT BOX"
        self.parent.colorBg.a = 0.8
        self.displayResult()
        Animation(y = (Window.height*0.08 if Window.width < Window.height else Window.height*0.11), d=0.3).start(self)

    def closeResult(self):
        self.isFullSize = False
        self.parent.disabledFunction = False
        self.parent.disabledHolder = False
        self.parent.colorBg.a = 0
        self.parent.openResult.mainLabel.text = "OPEN RESULT BOX"
        self.scroller.clear_widgets()
        self.remove_widget(self.scroller)
        self.displayResult()
        Animation(y = -Window.height, d=0.3).start(self)

    def allVariables(self):
        config = App.get_running_app().Matrixconfig
        self.scroller = None
        self.allLabel = list()
        self.resultList = config.get("ResultList") if config.get("ResultList") else list()
        self.coloredResultString = config.get("CResultString") if config.get("CResultString") else ""
        self.resultString = config.get("ResultString") if config.get("ResultString") else ""
        self.resultRows = config.get("ResultRows") if config.get("ResultRows") else 0
        self.resultCols = config.get("ResultCols") if config.get("ResultCols") else 0
        self.isFullSize = False
        self.isGraphShowing = False
        self.convertStringtoLabel(self.resultString)

    def turnStringToLabel(self, Coloredstring : str, string: str, result : list, row : int, col : int):
        self.coloredResultString = Coloredstring
        self.resultString = string
        self.resultRows = row
        self.resultCols = col
        self.resultList = copy.deepcopy(result)
        self.convertStringtoLabel(Coloredstring if self.isColoredText else string)
        self.showResult()

    def turnStringToLabelF(self, Coloredstring : str, string: str):
        self.coloredResultString = Coloredstring
        self.resultString = string
        self.resultList.clear()
        self.convertStringtoLabel(Coloredstring if self.isColoredText else string)
        self.showResult()

    def convertStringtoLabel(self, string : str):
        self.allLabel.clear()
        self.allLabel.append(LineLabel())
        self.allLabel.append(LineLabel())
        self.allLabel.append(LineLabel())
        for i in range(len(string)):
            if string[i] == "\n":
                self.allLabel.append(LineLabel())
                continue
            self.allLabel[-1].text += string[i]
            if len(self.allLabel[-1].text) > 80:
                self.allLabel.append(LineLabel())
        self.allLabel.append(LineLabel())
        self.allLabel.append(LineLabel())

    def displayResult(self):
        if self.scroller is not None:
            self.scroller.clear_widgets()
            self.remove_widget(self.scroller)

        self.scroller = ScrollView(size_hint=(None, None), pos=(self.x+5, self.y+5), size=(self.width*5, self.height-10))
        layout = GridLayout(cols=1, padding="5dp", spacing=sp(15) + sp(2), size_hint=(None,None))
        layout.width = (sp(15) * 80)*2.5
        layout.bind(minimum_height=layout.setter('height'))
        layout.bind(minimum_width=layout.setter('height'))
        for label in self.allLabel:
            if label.parent is not None: label.parent.remove_widget(label)
            layout.add_widget(label)

        self.scroller.add_widget(layout)
        self.add_widget(self.scroller)
        self.remove_widget(self.copyClipboard)
        self.remove_widget(self.clearClipboard)
        self.remove_widget(self.toMatrixA)
        self.remove_widget(self.toMatrixB)
        self.remove_widget(self.coloredStr)
        self.remove_widget(self.resultStr)

        self.add_widget(self.copyClipboard)
        self.add_widget(self.clearClipboard)
        self.add_widget(self.toMatrixA)
        self.add_widget(self.toMatrixB)
        self.add_widget(self.coloredStr)
        self.add_widget(self.resultStr)

    def changeMatrixValue(self, matrix : MatrixHolder):
        if self.resultList:
            matrix.cols = self.resultCols
            matrix.rows = self.resultRows
            for j in range(self.resultRows):
                for k in range(self.resultCols):
                    matrix.allEntriesValue[k][j] = f"{self.resultList[k + j * matrix.cols]}"
            matrix.changeMatrix()

    def clearClip(self):
        Toast("Result Box Cleared").start()
        self.coloredResultString = ""
        self.resultString = ""
        self.resultCols = 0
        self.resultRows = 0
        self.resultList.clear()
        self.allLabel.clear()
        self.displayResult()

    def copyClipBoard(self):
        Toast("Clipboard Copied").start()
        Clipboard.copy(self.resultString if self.resultString else "None")

    def changeStrResult(self):
        self.isColoredText = not self.isColoredText
        self.coloredStr.mainLabel.text = "No Color" if self.isColoredText else "Color"
        self.turnStringToLabel(
            self.coloredResultString , self.resultString, self.resultList, self.resultRows, self.resultCols)

    def printResult(self):
        try:
            self.isGraphShowing = True
            self.layout = BoxLayout(orientation='vertical')
            self.layout.size_hint = (None, None)
            self.layout.size = Window.width * 0.9, Window.height * 0.8

            flattened_matrix = self.resultList
            rows, cols = self.resultRows, self.resultCols
            matrix = np.array(flattened_matrix).reshape(rows, cols)

            fig = plt.figure(figsize=(Window.width / 100, Window.height / 100)) 
            ax = fig.add_subplot(111, projection='3d')

            x = np.arange(cols)
            y = np.arange(rows)
            x, y = np.meshgrid(x, y)
            z = matrix 

            ax.plot_surface(x, y, z, cmap="coolwarm", edgecolor='k')
            ax.set_title('3D Matrix Visualization', fontsize=18, color='white')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Value')

            fig.colorbar(ax.plot_surface(x, y, z, cmap="coolwarm", edgecolor='k'))

            canvas = FigureCanvasAgg(fig)
            canvas.print_figure("matrix_plot_3d.png", dpi=100)
            img = Image(source="matrix_plot_3d.png", size_hint=(None, None), size=(Window.width, Window.height))
            self.layout.add_widget(img)

            self.add_widget(self.layout)
        except:
            pass

    def close_plot(self):
        self.isGraphShowing = False
        self.remove_widget(self.layout)




    def displaySomeButton(self):
        self.copyClipboard = CustomButton("Copy")
        self.copyClipboard.func_binder = lambda : self.copyClipBoard()
        self.clearClipboard = CustomButton("Clear")
        self.clearClipboard.func_binder = lambda : self.clearClip()
        self.toMatrixA = CustomButton("ToFirst")
        self.toMatrixA.func_binder = lambda : self.changeMatrixValue(self.parent.firstMatrixHolder)
        self.toMatrixB = CustomButton("ToSecond")
        self.toMatrixB.func_binder = lambda : self.changeMatrixValue(self.parent.secondMatrixHolder)
        self.coloredStr = CustomButton("No Color" if self.isColoredText else "Color")
        self.coloredStr.func_binder = lambda : self.changeStrResult()

        self.resultStr = CustomButton("GRAPH")
        self.resultStr.func_binder = lambda : self.printResult()
        self.add_widget(self.copyClipboard)
        self.add_widget(self.clearClipboard)
        self.add_widget(self.toMatrixA)
        self.add_widget(self.toMatrixB)
        self.add_widget(self.coloredStr)
        self.add_widget(self.resultStr)

