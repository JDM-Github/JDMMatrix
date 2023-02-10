# import copy
# from kivy.app import App
# from kivy.core.window import Window
# from kivy.properties import NumericProperty
# from kivy.uix.widget import Widget
# from kivy.utils import get_color_from_hex as GetColor
# from kivy.uix.label import Label
# from kivy.clock import Clock
# from kivy.uix.textinput import TextInput

# from src import setCanvas, CustomWidget, Toast

# class matrixDirButton(CustomWidget):
    
#     def __init__(self, pos: list[int, int], offset: list[int, int], name: str, **kwargs):
#         size = (
#             ((Window.width * 0.8) / 8, (Window.height*0.2) / 4) if Window.width < Window.height else
#             ((Window.width * 0.4) / 8, (Window.width*0.2) / 5))
#         super().__init__((pos[0], pos[1] - size[1]), size, name, False, **kwargs)
#         self.offset = offset
#         app = App.get_running_app()
#         self.displayDesign(
#             app.CT.CurrentTheme.MATRIX_BUTTON_LINE,
#             app.CT.CurrentTheme.MATRIX_BUTTON_COLOR,
#             app.CT.CurrentTheme.MATRIX_BUTTON_PRESSED,
#             app.CT.CurrentTheme.MATRIX_BUTTON_FG)

#     def functions(self):
#         self.clicked = False
#         if (self.offset[0] == 5): self.nextMatrix()
#         elif (self.offset[0] == 4): self.previousMatrix()
#         elif (self.offset[0] == 3): self.clearEntries()
#         elif (self.offset[0] == 2): self.evaluateEntries()
#         else:
#             self.parent.oldCols = self.parent.cols
#             if self.parent.rows + self.offset[0] > 0 and self.parent.rows + self.offset[0] < 11: self.parent.rows += self.offset[0]
#             if self.parent.cols + self.offset[1] > 0 and self.parent.cols + self.offset[1] < 11: self.parent.cols += self.offset[1]

#             if self.parent.rows == self.parent.cols:
#                 for text in self.parent.parent.allFunctionsWidget.grid.children:
#                     text.changeName(self.parent.parent.firstMatrixHolder.name, self.parent.parent.secondMatrixHolder.name)
#         return super().functions()

#     def previousMatrix(self):
#         if (ord(self.parent.name) - 1) >= 65:
#             self.changematrix(chr(ord(self.parent.name) - 1))
#             return
#         Toast(f"No more previous Matrix").start()

#     def nextMatrix(self):
#         if chr(ord(self.parent.name) + 1) in App.get_running_app().Matrixconfig.get("Allmatrix"):
#             self.changematrix(chr(ord(self.parent.name) + 1))
#             return
#         Toast(f"No more next Matrix").start()

#     def changematrix(self, name: str):
#         if (self.parent.parent.firstMatrixHolder.name == name or self.parent.parent.secondMatrixHolder.name == name):
#             Toast(f"Matrix {name} is already in used").start()
#             return
#         self.parent.name = name
#         for text in self.parent.parent.allFunctionsWidget.grid.children:
#             text.changeName(self.parent.parent.firstMatrixHolder.name, self.parent.parent.secondMatrixHolder.name)
#         self.parent.allEntriesValue = self.parent.MainApp.allMatrixHolder.get(name)[2]
#         self.parent.rows, self.parent.cols = (
#             self.parent.MainApp.allMatrixHolder.get(name)[0],
#             self.parent.MainApp.allMatrixHolder.get(name)[1])
#         self.parent.changeMatrix()

#     def on_touch_down(self, touch):
#         if self.parent.parent.disabledHolder is False:
#             super().on_touch_down(touch)

#     def clearEntries(self):
#         for r in range(10):
#             for c in range(10): self.parent.allEntriesValue[r][c] = "0"
#         self.parent.rows = self.parent.cols = 3
#         self.parent.changeMatrix()

#     def evaluateEntries(self):
#         for entry in self.parent.allEntries:
#             try: answer = eval(entry.textinput.text)
#             except (NameError, SyntaxError): continue
#             answer = round(answer, 3)
#             answer = int(answer) if answer == int(answer) else answer
#             entry.textinput.text = f"{answer}"

# class EntriesTextInput(TextInput):

#     def __init__(self, size, pos, **kwargs):
#         super().__init__(**kwargs)
#         self.getFocused = False
#         self.size = size
#         self.pos = pos
#         self.background_normal = ""
#         self.background_active = ""
#         app = App.get_running_app()
#         self.displayDesign(
#             app.CT.CurrentTheme.MATRIX_ENTRY_SELECTION,
#             app.CT.CurrentTheme.MATRIX_ENTRY_FG,
#             app.CT.CurrentTheme.MATRIX_ENTRY_COLOR,
#             app.CT.CurrentTheme.MATRIX_ENTRY_CURSOR)
#         self.bind(text=self.changeText)

#     def displayDesign(self, Selection: str, ForeGround: str, MColor: str, Cursor: str):
#         self.hint_text_color = GetColor(ForeGround)
#         self.selection_color = GetColor(Selection)
#         self.foreground_color = GetColor(ForeGround)
#         self.background_color = GetColor(MColor)
#         self.cursor_color = GetColor(Cursor)

#     def on_focus(self, _, focus):
#         if focus: Clock.schedule_once(lambda _: self.select_all(), 0.2)

#     def changeText(self, *_):
#         self.parent.parent.allEntriesValue[self.parent.offset[1]][self.parent.offset[0]] = self.text
#         self.parent.parent.MainApp.allMatrixHolder.get(self.parent.parent.name)[2][self.parent.offset[1]][self.parent.offset[0]] = self.text

# class matrixEntries(Widget):
    
#     def __init__(self, w, h, pos: list[int, int], offset, value, **kwargs):
#         super().__init__(**kwargs)
#         self.size = (
#             (((Window.width * 0.8)*0.8) / w, ((Window.height*0.3) * 0.8) / h) if Window.width < Window.height else
#             (((Window.height * 0.8)*0.8) / w, ((Window.width*0.3) * 0.8) / h))
#         self.offset = offset
#         self.pos = pos
#         setCanvas(self, App.get_running_app().CT.CurrentTheme.WHITE, App.get_running_app().CT.CurrentTheme.MATRIX_ENTRY_COLOR, radius=[0, 0, 0, 0])
#         self.textinput = EntriesTextInput(
#             text=value, size=self.size, pos=self.pos,
#             write_tab=False, multiline=False, halign="center", hint_text="0")
#         self.add_widget(self.textinput)

# class MatrixHolder(Widget):
    
#     rows = NumericProperty(3)
#     cols = NumericProperty(3)
#     def __init__(self, position, name, **kwargs):
#         super().__init__(**kwargs)
#         self.name = name
#         self.position = position
#         self.size = (
#             (Window.width * 0.8, Window.height*0.3) if Window.width < Window.height else
#             (Window.width * 0.4, Window.width*0.3))
#         self.pos = ((Window.width*0.1, (
#             (Window.height - self.height - (((Window.height*0.2) / 4)*1.5)) if not position else 
#             ((Window.height - (self.height*2) - (((Window.height*0.22) / 4)*2.75))))) if Window.width < Window.height else
#             ((Window.width*0.075 if not position else Window.width*0.125+self.width),
#             (Window.height - self.height - (((Window.height*0.2) / 4)*2))))

#         self.MainApp = App.get_running_app()
#         self.allVariables()
#         self.displayDesign(
#             self.MainApp.CT.CurrentTheme.MATRIX_LINE,
#             self.MainApp.CT.CurrentTheme.MATRIX_BOX)
#         self.bind(rows=self.changeMatrix, cols=self.changeMatrix)

#     def allVariables(self):
#         self.allEntries = list()
#         self.rows = self.MainApp.allMatrixHolder.get(self.name)[0]
#         self.cols = self.MainApp.allMatrixHolder.get(self.name)[1]
#         self.allEntriesValue = self.MainApp.allMatrixHolder.get(self.name)[2]

#     def displayDesign(self, ColorLine: str, Color: str):
#         self.clear_widgets()
#         self.canvas.clear()
        
#         setCanvas(self, ColorLine, Color)
#         self.displayButton()
#         self.changeMatrix()

#     def changeMatrix(self, *_):            
#         self.MainApp.allMatrixHolder.get(self.name)[0] = self.rows
#         self.MainApp.allMatrixHolder.get(self.name)[1] = self.cols
#         self.displayMatrixEntries(self.rows, self.cols)
#         self.displayTitle(self.name)

#     def displayTitle(self, matrixName: str = "A"):
#         if not hasattr(self, "title"):
#             self.title = Label(
#                 pos=(self.center_x-(self.width/2), self.top-(self.height*0.1)),
#                 size=(self.width, (self.height*0.1)),
#                 font_name = "consolas",
#                 font_size = "13sp")
#             self.add_widget(self.title)
#         self.title.text= "Matrix " + matrixName + f" : {self.rows} x {self.cols}"

#     def displayButton(self):
#         self.add_widget(matrixDirButton((self.x + 0 * (self.width / 8), self.y), (-1, 0), "UP"))
#         self.add_widget(matrixDirButton((self.x + 1 * (self.width / 8), self.y), (1, 0), "DOWN"))
#         self.add_widget(matrixDirButton((self.x + 2 * (self.width / 8), self.y), (0, -1), "LEFT"))
#         self.add_widget(matrixDirButton((self.x + 3 * (self.width / 8), self.y), (0, 1), "RIGHT"))
#         self.add_widget(matrixDirButton((self.x + 4 * (self.width / 8), self.y), (2, 1), "EVAL"))
#         self.add_widget(matrixDirButton((self.x + 5 * (self.width / 8), self.y), (3, 1), "CLEAR"))
#         self.add_widget(matrixDirButton((self.x + 6 * (self.width / 8), self.y), (4, 1), "<-"))
#         self.add_widget(matrixDirButton((self.x + 7 * (self.width / 8), self.y), (5, 1), "->"))

#     def displayMatrixEntries(self, row, col):
#         for entry in self.allEntries: self.remove_widget(entry)
#         self.allEntries.clear()

#         for j in range(row):
#             for i in range(col):
#                 pos = (self.x + (self.width*0.1) + i * ((self.width*0.8) / (max(5, col))),
#                     self.y + (self.height*0.1) + (((max(4, row-1))-j) * ((self.height*0.8) / (max(5, row)))))
#                 self.allEntries.append(matrixEntries(
#                     max(5, col), max(5, row), pos, (j, i),
#                     self.allEntriesValue[i][j]))
#                 self.add_widget(self.allEntries[-1])
