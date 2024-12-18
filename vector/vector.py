# from kivy.app import App
# from kivy.core.window import Window
# from kivy.uix.widget import Widget
# from kivy.utils import get_color_from_hex as GetColor
# from kivy.graphics import Color, Rectangle
# from .matrixHolder import MatrixHolder
# from .matrixFunction import (
#     MatrixFunctionMenu,
#     OpenResultBox,
# )
# from .matrixMenu import MatrixMenu
# from .result import MatrixResultBox

# class Matrix(Widget):

#     def __init__(self, **kwargs): 
#         super().__init__(**kwargs)
#         self.allBooleanDisabler()
#         self.displayMatrixHolder()
#         self.displayMatrixFunction()
#         self.higherWidget()

#     def allBooleanDisabler(self):
#         self.disabledFunction = False
#         self.disabledHolder = False
#         self.disabledMenu = False
#         self.disabledResult = False

#     def displayMatrixHolder(self):
#         config = App.get_running_app().Matrixconfig
#         self.firstMatrixHolder = MatrixHolder(0, config.get("CurrentFirst") if config.get("CurrentFirst") else "A")
#         self.secondMatrixHolder = MatrixHolder(1, config.get("CurrentSecond") if config.get("CurrentSecond") else "B")
#         self.add_widget(self.firstMatrixHolder)
#         self.add_widget(self.secondMatrixHolder)

#     def higherWidget(self):
#         self.matrixMenu = MatrixMenu()
#         self.MatrixResult = MatrixResultBox()
#         self.openResult = OpenResultBox("OPEN RESULT BOX")
#         with self.canvas:
#             self.colorBg = Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.WINDOW_BACKGROUND), a=0)
#             self.rect = Rectangle(size=Window.size, pos=(0, 0))

#         self.add_widget(self.openResult)
#         self.add_widget(self.matrixMenu)
#         self.add_widget(self.MatrixResult)

#     def displayMatrixFunction(self):
#         self.allFunctionsWidget = MatrixFunctionMenu()
#         self.add_widget(self.allFunctionsWidget)
