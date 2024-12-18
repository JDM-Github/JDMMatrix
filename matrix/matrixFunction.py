import copy
import string
from kivy.app import App
from fractions import Fraction
from kivy.core.window import Window
from kivy.metrics import dp

from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.graphics import RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from .matrixHolder import MatrixHolder
from src import setCanvas, CustomWidget

class MatrixFunctionMenu(CustomWidget):

    def __init__(self, **kwargs):
        size = ((Window.width * 0.8, Window.height*0.05) if Window.width < Window.height else
                (Window.width * 0.8, Window.height*0.08))
        pos = (Window.width*0.1, ((Window.height - ((Window.height*0.2)*3)) - (Window.height*0.01) - ((((Window.height*0.2) / 4) * 1.5) * (4+1)) ))
        super().__init__((pos[0], pos[1]+size[1]*1.2), size, "Matrix Functions", False, **kwargs)
        self.opened = False
        self.grid = GridLayout(size_hint_y=None, cols=2, padding="10dp", spacing="5dp")
        app = App.get_running_app()
        self.displayDesign(
            app.CT.CurrentTheme.FUNC_BUTTON_LINE,
            app.CT.CurrentTheme.FUNC_BUTTON_COLOR,
            app.CT.CurrentTheme.FUNC_BUTTON_PRESSED,
            app.CT.CurrentTheme.FUNC_BUTTON_FG)

    def setfunctionWidget(self):
        self.allfunctionList = [
            [ChangeButton, [self.parent.firstMatrixHolder, self.parent.secondMatrixHolder, f"{self.parent.firstMatrixHolder.name} <-> {self.parent.secondMatrixHolder.name}"]],
            [MatrixAtoB, [self.parent.firstMatrixHolder, self.parent.secondMatrixHolder, f"{self.parent.firstMatrixHolder.name} -> {self.parent.secondMatrixHolder.name}"]],
            [MatrixBtoA, [self.parent.firstMatrixHolder, self.parent.secondMatrixHolder, f"{self.parent.firstMatrixHolder.name} <- {self.parent.secondMatrixHolder.name}"]],
            [AddMatrixFunction, [self.parent.firstMatrixHolder, self.parent.secondMatrixHolder, f"{self.parent.firstMatrixHolder.name} + {self.parent.secondMatrixHolder.name}"]],
            [MinMatrixFunction, [self.parent.firstMatrixHolder, self.parent.secondMatrixHolder, f"{self.parent.firstMatrixHolder.name} - {self.parent.secondMatrixHolder.name}"]],
            [MulMatrixFunction, [self.parent.firstMatrixHolder, self.parent.secondMatrixHolder, f"{self.parent.firstMatrixHolder.name}{self.parent.secondMatrixHolder.name}"]],
            [SquareMatrixFunction, [self.parent.firstMatrixHolder, f"{self.parent.firstMatrixHolder.name}[sup]2[/sup]"]],
            [CramersRuleMatrixFunction, [self.parent.firstMatrixHolder, f"Cramers({self.parent.firstMatrixHolder.name})"]],
            [TransposeMatrixFunction, [self.parent.firstMatrixHolder, f"Trans({self.parent.firstMatrixHolder.name})"]],
            [DeterminantMatrixFunction, [self.parent.firstMatrixHolder, f"Det({self.parent.firstMatrixHolder.name})"]],
            [BasketWeaveMatrixFunction, [self.parent.firstMatrixHolder, f"B-Weave({self.parent.firstMatrixHolder.name})"]],
            [InverseMatrixFunction, [self.parent.firstMatrixHolder, f"Inv({self.parent.firstMatrixHolder.name})"]],
            [MinorsMatrixFunction, [self.parent.firstMatrixHolder, f"Minors({self.parent.firstMatrixHolder.name})"]],
            [CofactorMatrixFunction, [self.parent.firstMatrixHolder, f"Cofactor({self.parent.firstMatrixHolder.name})"]],
            [AdjugateMatrixFunction, [self.parent.firstMatrixHolder, f"Adjugate({self.parent.firstMatrixHolder.name})"]],
            # [ScalarMatrixFunction, [self.parent.firstMatrixHolder, f"Scalar({self.parent.firstMatrixHolder.name})"]],
            [AreaTriangleMatrixFunction, [self.parent.firstMatrixHolder ,f"Area-T({self.parent.firstMatrixHolder.name})"]],
            [PointMatrixFunction, [self.parent.firstMatrixHolder, f"{self.parent.firstMatrixHolder.cols}-Point({self.parent.firstMatrixHolder.name})"]],
            [TetrahedronMatrixFunction, [self.parent.firstMatrixHolder ,f"Tetra({self.parent.firstMatrixHolder.name})"]],
        ]

    def on_touch_down(self, touch):
        if self.parent.disabledFunction is False:
            super().on_touch_down(touch)
        
    def open(self):
        if not hasattr(self, "scroll"):
            self.initiateWidget()
        self.parent.disabledHolder = True
        self.opened = True
        self.canvas.add(self.col)
        self.canvas.add(self.rec)
        self.add_widget(self.scroll)
    
    def close(self):
        if hasattr(self, "col"):
            self.parent.disabledHolder = False
            self.opened = False
            self.canvas.remove(self.col)
            self.canvas.remove(self.rec)
            self.remove_widget(self.scroll)
    
    def functions(self):
        if self.opened is False: self.open()
        else: self.close()

    def initiateWidget(self):
        self.scroll = ScrollView(size=(Window.width*0.9, Window.height*0.78 if Window.width < Window.height else Window.height*0.7),
                                 pos=(Window.width*0.05, Window.height*0.15 if Window.width < Window.height else Window.height*0.22))
        self.col = Color(rgb=GetColor(App.get_running_app().CT.CurrentTheme.RESULT_BOX), a=0.9)
        self.rec = RoundedRectangle(size=self.scroll.size, pos=self.scroll.pos, radius=[10, 10, 10, 10])
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.setfunctionWidget()
        for i in range(len(self.allfunctionList)):
            w = self.allfunctionList[i]
            widget = w[0](*w[1])
            widget.size_hint_y = None
            widget.height = Window.height*0.04 if Window.width < Window.height else Window.width *0.04
            widget.bind(size=widget.SizebindCanvas)
            widget.bind(pos=widget.bindCanvas)
            self.grid.add_widget(widget)
        self.scroll.add_widget(self.grid)

class MatrixFunction(CustomWidget):

    def __init__(self, name: str, **kwargs):
        super().__init__((0, 0), (100 , Window.height*0.05), name, False, **kwargs)
        self.MainApp = App.get_running_app()
        self.displayDesign(
            self.MainApp.CT.CurrentTheme.FUNC_BUTTON_LINE,
            self.MainApp.CT.CurrentTheme.FUNC_BUTTON_COLOR,
            self.MainApp.CT.CurrentTheme.FUNC_BUTTON_PRESSED,
            self.MainApp.CT.CurrentTheme.FUNC_BUTTON_FG)
        self.func_binder = lambda : self.parent.parent.parent.close()
    
    def changeName(self, *_): ...
    def on_touch_down(self, touch):
        if self.parent.parent.parent.parent.disabledFunction is False:
            super().on_touch_down(touch)

    def getMatrixGiven(self, MatA: MatrixHolder):
        newString: str = str()
        for r in range(MatA.rows):
            newString += "| "
            for c in range(MatA.cols):
                newString += f"{self.checkEntry(MatA.allEntries[c + r * MatA.cols].textinput.text)} | "
            newString += "\n"
        return f"Matrix {MatA.name}\n{newString}\n"

    def listToString(self, newList: list, cols: int):
        newText = str()
        for r in range(cols):
            newText += "| "
            for c in range(cols):
                newText += f"{newList[c+r*cols]} | "
            newText += "\n"
        return newText

    def TgetMatrixGiven(self, MatA: MatrixHolder, MatB: MatrixHolder):
        newList: list[str] = list()
        lastlen: int = 0
        for r in range(MatA.rows):
            newList.append("| ")
            lastlen = 2
            for c in range(MatA.cols):
                string: str = f"{self.checkEntry(MatA.allEntries[c + r * MatA.cols].textinput.text)} | "
                newList[r] += string
                lastlen += len(string)
            if (r >= MatB.rows): newList[r] += "\n"

        for r in range(MatB.rows):
            try:
                newList[r] += "<-> | "
            except IndexError:
                newList.append(" " * lastlen)
                newList[r] += "<-> | "
            for c in range(MatB.cols):
                newList[r] += f"{self.checkEntry(MatB.allEntries[c + r * MatB.cols].textinput.text)} | "
            newList[r] += "\n"
        return f"Matrix {MatA.name}" + " "*(lastlen-len(f"Matrix {MatA.name}")) + f"    Matrix {MatB.name}\n" + "".join(newList) + "\n"

    def isSquaredMatrix(self, MatA : MatrixHolder):
        return MatA.rows == MatA.cols

    def isEqualMatrix(self, MatA : MatrixHolder, MatB : MatrixHolder):
        return MatA.rows == MatB.rows and MatA.cols == MatB.cols

    def isAugmentedMatrix(self, MatA : MatrixHolder):
        return MatA.rows == MatA.cols - 1

    def checkEntry(self, str1: str):
        try: first = float(str1)
        except ValueError: first = 1 if str1 != "" else 0
        first = round(first, 3)
        result = int(first) if first == int(first) else first
        return result
    
    def turnMatrixEntriesNewList(self, MatA : MatrixHolder):
        newList = list()
        for r in range(MatA.rows):
            for c in range(MatA.cols):
                newList.append(self.checkEntry(MatA.allEntries[c + r * MatA.cols].textinput.text))
        return newList

    def getAnswerFromResult(self, Title : str, row : int, col : int, resultAnswer : list) -> str:
        newText = f"{Title}\n"
        for r in range(row):
            newText += "| "
            for c in range(col): newText += f"{round(resultAnswer[c + r * col], 3)} | "
            newText += "\n"
        return newText

    def find_determinant(self, matrixList: list, colSize: int, firstBool: bool):
        textResult = ""
        if colSize == 1:
            textResult += f"({round(matrixList[0], 3)})"
            return matrixList[0], textResult
        if colSize <= 2:
            if firstBool is False: textResult += "("
            textResult += f"({round(matrixList[0], 3)} * {round(matrixList[3], 3)}) - ({round(matrixList[1], 3)} * {round(matrixList[2], 3)}))"
            return (matrixList[0]*matrixList[3]) - (matrixList[1]*matrixList[2]), textResult

        result = 0
        new_matrix = [0 for _ in range((colSize-1)*(colSize-1))]
        for i in range(colSize):
            index = 0
            for j in range(i):
                for k in range(colSize-1): new_matrix[index + ((colSize-1)*k)] = matrixList[j + (colSize * (k+1))]
                index += 1
            for j in range((colSize-1)-i):
                for k in range(colSize-1): new_matrix[index+((colSize-1)*k)] = matrixList[(i + j + 1) + (colSize * (k + 1))]
                index += 1

            if i % 2 == 0:
                if (i != 0): textResult += " + \n"
                textResult += f"({round(matrixList[i], 3)} * ("
                r1, r2 = self.find_determinant(new_matrix, colSize-1, True)
                result += matrixList[i] * r1
                textResult += r2 + (")" * min(colSize - 2, 2))
            else:
                textResult += f" - \n({round(matrixList[i], 3)} * ("
                r1, r2 = self.find_determinant(new_matrix, colSize-1, True)
                result -= matrixList[i] * r1
                textResult += r2 + (")" * min(colSize - 2, 2))
        
        return result, textResult

    def determinant_in_weave(self, matrixList: list, colSize: int, firstBool: bool):
        textResult = ""
        if colSize == 1:
            textResult += f"({round(matrixList[0], 3)})"
            return matrixList[0], textResult
        if colSize <= 2:
            if firstBool is False: textResult += "("
            textResult += f"({round(matrixList[0], 3)} * {round(matrixList[3], 3)}) - ({round(matrixList[1], 3)} * {round(matrixList[2], 3)}))"
            return (matrixList[0]*matrixList[3]) - (matrixList[1]*matrixList[2]), textResult

        result1 = 0
        textResult += "["
        firstAnswer = []
        for r in range(colSize):
            answer = 1
            textResult += "("
            for c in range(colSize):
                answer *= matrixList[((r+c)%colSize) + colSize * c]
                textResult += str(self.checkEntry(matrixList[((r+c)%colSize) + colSize * c])) + (" * " if c + 1 < colSize else "")
            firstAnswer.append(answer)
            textResult += ")" + (" + " if r + 1 < colSize else "")
            result1 += answer
        textResult += "] - \n["
        result2 = 0
        secondAnswer = []
        for r in range(colSize):
            answer = 1
            textResult += "("
            for c in range(colSize):
                answer *= matrixList[((((colSize-1)*2-r)-c)%colSize) + colSize * c]
                textResult += str(self.checkEntry(matrixList[((((colSize-1)*2-r)-c)%colSize) + colSize * c])) + (" * " if c + 1 < colSize else "")
            secondAnswer.append(answer)
            textResult += ")" + (" + " if r + 1 < colSize else "")
            result2 += answer
        textResult += "]\n["
        for ind, i in enumerate(firstAnswer): textResult += f"{i} + " if ind+1 < len(firstAnswer) else f"{i}] - ["
        for ind, i in enumerate(secondAnswer): textResult += f"{i} + " if ind+1 < len(secondAnswer) else f"{i}]"
        return result1 - result2, textResult + f"\n{result1} - {result2}"

    def makeWhileif(self, value : float):
        return int(value) if value == int(value) else value
    
    def find_minors_matrix(self, MatA : MatrixHolder, isCofactor : bool = False):
        matrix = list()
        resultAnswer = list()
        for rows in range(MatA.rows):
            matr2 = list()
            for cols in range(MatA.cols):
                matr2.insert(0, self.checkEntry(MatA.allEntries[(rows*MatA.cols)+cols].textinput.text))
            matrix.insert(0, matr2)

        textResult = ""
        textResultPlain = list()
        for rows in range(MatA.rows):
            textResult += "| "
            for cols in range(MatA.cols):
                matr2 = list()
                for j in range(rows):
                    for k in range(cols): matr2.append(matrix[j][k])
                for j in range(rows):
                    for k in range((MatA.cols-1) - cols): matr2.append(matrix[j][cols+k+1])
                for j in range((MatA.rows-1)-rows):
                    for k in range(cols): matr2.append(matrix[rows+1+j][k])
                for j in range((MatA.rows-1)-rows):
                    for k in range((MatA.cols-1)-cols): matr2.append(matrix[rows+1+j][cols+1+k])
                
                r1, r2 = self.find_determinant(matr2, MatA.cols-1, False)
                resultAnswer.insert(0, (r1 * (-1 if (isCofactor and (rows + cols) % 2) else 1)))
                textResult += r2 + " | "
                textResultPlain.insert(0, round(eval(r2), 3))

            textResult += "\n"
        if isCofactor: return resultAnswer, textResult, textResultPlain
        return resultAnswer, textResult

class AddMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, MatB: MatrixHolder, name: str="Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
        self.MatB = MatB

    def changeName(self, name1: str, name2: str):
        self.name = f"{name1} + {name2}"
        self.mainLabel.text = self.name

    def addTwoString(self, str1: str, str2: str):
        try: first = float(str1)
        except ValueError: first = 1 if str1 != "" else 0
        try: second = float(str2)
        except ValueError: second = 1 if str2 != "" else 0
        result = int(first + second) if first + second == int(first + second) else first + second
        return result

    def functions(self):
        givenAB = self.TgetMatrixGiven(self.MatA, self.MatB)
        if not self.isEqualMatrix(self.MatA, self.MatB):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenAB +
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} Size and Matrix {self.MatB.name} Size is not Equals",
                givenAB + f"The Matrix {self.MatA.name} Size and Matrix {self.MatB.name} Size is not Equals.")
            return

        resultAnswer = list()
        textResult = ""
        for j in range(min(self.MatA.rows, 5)):
            textResult += "| "
            for i in range(min(self.MatB.cols, 5)):
                result = self.addTwoString(self.MatA.allEntriesValue[i][j], self.MatB.allEntriesValue[i][j])
                textResult += f"{self.checkEntry(self.MatA.allEntriesValue[i][j])} + {self.checkEntry(self.MatB.allEntriesValue[i][j])} | "
                resultAnswer.append(result)
            textResult += "\n"

        ColoredtextResult = (givenAB +
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Add Matrix {self.MatA.name} and Matrix {self.MatB.name}", self.MatA.rows, self.MatA.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n" + textResult)
        textResult = givenAB + self.getAnswerFromResult(f"Answer: Add Matrix {self.MatA.name} and Matrix {self.MatB.name}", self.MatA.rows, self.MatA.cols, resultAnswer) + "\nStep By Step:\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColoredtextResult, textResult, resultAnswer, self.MatA.rows, self.MatB.cols)

class MinMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, MatB: MatrixHolder, name: str="Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
        self.MatB = MatB
    
    def changeName(self, name1: str, name2: str):
        self.name = f"{name1} - {name2}"
        self.mainLabel.text = self.name

    def minTwoString(self, str1: str, str2: str):
        try: first = float(str1)
        except ValueError: first = 1 if str1 != "" else 0
        try: second = float(str2)
        except ValueError: second = 1 if str2 != "" else 0
        result = int(first - second) if first - second == int(first - second) else first - second
        return result

    def functions(self):
        givenAB = self.TgetMatrixGiven(self.MatA, self.MatB)
        if not self.isEqualMatrix(self.MatA, self.MatB):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenAB +
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} Size and Matrix {self.MatB.name} Size is not Equals",
                givenAB + f"The Matrix {self.MatA.name} Size and Matrix {self.MatB.name} Size is not Equals.")
            return
        resultAnswer = list()
        textResult = ""
        for j in range(min(self.MatA.rows, 5)):
            textResult += "| "
            for i in range(min(self.MatB.cols, 5)):
                result = self.minTwoString(self.MatA.allEntriesValue[i][j], self.MatB.allEntriesValue[i][j])
                textResult += f"{self.checkEntry(self.MatA.allEntriesValue[i][j])} - {self.checkEntry(self.MatB.allEntriesValue[i][j])} | "
                resultAnswer.append(result)
            textResult += "\n"

        ColortextResult = (givenAB +
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Subtract Matrix {self.MatA.name} and Matrix {self.MatB.name}", self.MatA.rows, self.MatA.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n" + textResult)
        textResult = givenAB + self.getAnswerFromResult(f"Answer: Subtract Matrix {self.MatA.name} and Matrix {self.MatB.name}", self.MatA.rows, self.MatA.cols, resultAnswer) + "\nStep By Step:\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.rows, self.MatB.cols)

class MulMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, MatB: MatrixHolder, name: str="Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
        self.MatB = MatB

    def changeName(self, name1: str, name2: str):
        self.name = f"{name1}{name2}"
        self.mainLabel.text = self.name

    def mulTwoString(self, str1: str, str2: str):
        try: first = float(str1)
        except ValueError: first = 1 if str1 != "" else 0
        try: second = float(str2)
        except ValueError: second = 1 if str2 != "" else 0
        result = int(first * second) if first * second == int(first * second) else first * second
        return result

    def functions(self):
        givenAB = self.TgetMatrixGiven(self.MatA, self.MatB)
        if self.MatA.cols != self.MatB.rows:
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenAB +
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} Cols is not Equal to Matrix {self.MatB.name} Rows",
                givenAB + f"The Matrix {self.MatA.name} Cols is not Equal to Matrix {self.MatB.name} Rows.")
            return
        textResult = ""
        resultAnswer = list()
        for j in range(min(self.MatA.rows, 5)):
            textResult += "| "
            for k in range(min(self.MatB.cols, 5)):
                result = 0
                textResult += "("
                for i in range(min(self.MatB.cols, 5)):
                    result += self.mulTwoString(self.MatA.allEntriesValue[i][j], self.MatB.allEntriesValue[k][i])
                    textResult += f"({self.checkEntry(self.MatA.allEntriesValue[i][j])} * {self.checkEntry(self.MatB.allEntriesValue[k][i])})"
                    if i+1 != min(self.MatB.cols, 5): textResult += " + "
                textResult += ") | "
                resultAnswer.append(result)
            textResult += "\n"
        
        ColortextResult = (givenAB +
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Multiplication of Matrix {self.MatA.name} and Matrix {self.MatB.name}", self.MatA.rows, self.MatB.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n" + textResult)
        textResult = givenAB + self.getAnswerFromResult(f"Answer: Multiplication of Matrix {self.MatA.name} and Matrix {self.MatB.name}", self.MatA.rows, self.MatB.cols, resultAnswer) + "\nStep By Step:\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.rows, self.MatB.cols)

class SquareMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"{name1}[sup]2[/sup]"
        self.mainLabel.text = self.name

    def mulTwoString(self, str1: str, str2: str):
        try: first = float(str1)
        except ValueError: first = 1 if str1 != "" else 0
        try: second = float(str2)
        except ValueError: second = 1 if str2 != "" else 0
        result = int(first * second) if first * second == int(first * second) else first * second
        return result

    def functions(self):
        givenAB = self.TgetMatrixGiven(self.MatA, self.MatA)
        if not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenAB +
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not a Squared Matrix",
                givenAB + f"The Matrix {self.MatA.name} is not a Squared Matrix.")
            return
        textResult = ""
        resultAnswer = list()
        for j in range(min(self.MatA.rows, 5)):
            textResult += "| "
            for k in range(min(self.MatA.cols, 5)):
                result = 0
                textResult += "("
                for i in range(min(self.MatA.cols, 5)):
                    result += self.mulTwoString(self.MatA.allEntriesValue[i][j], self.MatA.allEntriesValue[k][i])
                    textResult += f"({self.checkEntry(self.MatA.allEntriesValue[i][j])} * {self.checkEntry(self.MatA.allEntriesValue[k][i])})"
                    if i+1 != min(self.MatA.cols, 5): textResult += " + "
                textResult += ") | "
                resultAnswer.append(result)
            textResult += "\n"

        ColortextResult = (givenAB +
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Squared Matrix {self.MatA.name}", self.MatA.rows, self.MatA.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n" + textResult)
        textResult = givenAB + self.getAnswerFromResult(f"Answer: Squared Matrix {self.MatA.name}", self.MatA.rows, self.MatA.cols, resultAnswer) + "\nStep By Step:\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.rows, self.MatA.cols)

class ScalarTextInput(TextInput):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_active=""
        self.halign = "center"
        self.write_tab = False
        self.multiline = False
        self.font_size = "13sp"
        self.font_name = "consolas"
        MainApp = App.get_running_app()
        self.displayDesign(
            MainApp.CT.CurrentTheme.FUNC_ENTRY_SELECTION,
            MainApp.CT.CurrentTheme.FUNC_ENTRY_FG,
            MainApp.CT.CurrentTheme.FUNC_ENTRY_CURSOR)
        self.bind(on_text_validate=self.on_enter)
    
    def displayDesign(self, Selection: str, ForeGround: str, Cursor: str):
        self.hint_text_color = GetColor(ForeGround)
        self.selection_color = GetColor(Selection)
        self.foreground_color = GetColor(ForeGround)
        self.cursor_color = GetColor(Cursor)
        self.background_color=GetColor("00000000")

    def on_focus(self, *_):
        self.parent.mainLabel.text = "" if self.focus or self.text != "" else self.parent.name
        self.hint_text = "Scalar" if self.focus else ""
    def on_enter(self, *_): self.parent.functions()

class ScalarMatrixFunction(Widget):

    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(**kwargs)
        padding = dp(10) if Window.width < Window.height else dp(15)
        self.name = name
        self.MatA = MatA
        self.width -= padding
        self.height -= padding
        self.MainApp = App.get_running_app()
        self.displayDesign(
            self.MainApp.CT.CurrentTheme.FUNC_BUTTON_LINE,
            self.MainApp.CT.CurrentTheme.FUNC_BUTTON_COLOR)
    
    def changeName(self, name1: str, ____: str):
        self.name = f"Scalar({name1})"
        self.mainLabel.text = self.name
    
    def displayDesign(self, ColorLine: str, Color: str):
        self.clear_widgets()
        self.canvas.clear()

        setCanvas(self, ColorLine, Color)
        self.textinput = ScalarTextInput(size=self.size, pos=self.pos)
        self.mainLabel = Label( markup=True, font_name = "consolas", font_size="13sp", size=self.size, pos=self.pos, text=self.name )
        self.add_widget(self.textinput)
        self.add_widget(self.mainLabel)

    def getMatrixGiven(self, MatA: MatrixHolder):
        newString: str = str()
        for r in range(MatA.rows):
            newString += "| "
            for c in range(MatA.cols):
                newString += f"{self.checkEntry(MatA.allEntries[c + r * MatA.cols].textinput.text)} | "
            newString += "\n"
        return f"Matrix {self.MatA.name}\n" + newString + "\n"

    def checkEntry(self, str1: str):
        try: first = float(str1)
        except ValueError: first = 1 if str1 != "" else 0
        first = round(first, 3)
        result = int(first) if first == int(first) else first
        return result

    def getAnswerFromResult(self, Title : str, row : int, col : int, resultAnswer : list) -> str:
        newText = f"{Title}:\n"
        for r in range(row):
            newText += "| "
            for c in range(col): newText += f"{round(resultAnswer[c + r * col], 3)} | "
            newText += "\n"
        return newText

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        resultAnswer = list()
        textResult = ""
        for j in range(min(self.MatA.rows, 5)):
            textResult += "| "
            for i in range(min(self.MatA.cols, 5)):
                result = self.checkEntry(self.MatA.allEntriesValue[i][j]) * self.checkEntry(self.textinput.text)
                textResult += f"( {self.checkEntry(self.MatA.allEntriesValue[i][j])} * {self.checkEntry(self.textinput.text)} ) | "
                resultAnswer.append(result)
            textResult += "\n"

        ColortextResult = (givenA + 
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Matrix {self.MatA.name} Scalar to {self.checkEntry(self.textinput.text)}", self.MatA.rows, self.MatA.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n" + textResult)
        textResult = givenA + self.getAnswerFromResult(f"Answer: Matrix {self.MatA.name} Scalar to {self.checkEntry(self.textinput.text)}", self.MatA.rows, self.MatA.cols, resultAnswer) + "\nStep By Step\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.rows, self.MatA.cols)

class TransposeMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"Trans({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        textResult = ""
        resultAnswer = list()
        copyList = copy.deepcopy(self.MatA.allEntriesValue)
        
        for j in range(min(self.MatA.cols, 5)):
            for i in range(min(self.MatA.rows, 5)):
                resultAnswer.append(self.checkEntry(copyList[j][i]))
        
        ColortextResult = givenA + self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Transpose", self.MatA.cols, self.MatA.rows, resultAnswer)
        textResult = givenA + self.getAnswerFromResult("Answer: Transpose", self.MatA.cols, self.MatA.rows, resultAnswer)
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.cols, self.MatA.rows)

class DeterminantMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"Det({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not a Squared Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not a Squared Matrix.")
            return
        resultAnswer, textResult = self.find_determinant(self.turnMatrixEntriesNewList(self.MatA), self.MatA.cols, False)
        ColortextResult = givenA + f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Determinant[/color]: {round(resultAnswer, 3)}\n\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step by Step:\n" + textResult
        textResult = givenA + f"Determinant: {round(resultAnswer, 3)}\n\nStep by Step:\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(ColortextResult, textResult)

class BasketWeaveMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"B-Weave({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not a Squared Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not a Squared Matrix.")
            return
        elif self.MatA.cols > 3:
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA +
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix Size is Bigger than 3x3",
                givenA + "The Matrix Size is Bigger than 3x3.")
            return
        resultAnswer, textResult = self.determinant_in_weave(self.turnMatrixEntriesNewList(self.MatA), self.MatA.cols, False)
        ColortextResult = givenA + f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Determinant[/color]: {round(resultAnswer, 3)}\n\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step by Step:\n" + textResult
        textResult = givenA + f"Determinant: {round(resultAnswer, 3)}\n\nStep by Step:\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(ColortextResult, textResult)

class AreaTriangleMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA

    def changeName(self, name1: str, ____: str):
        self.name = f"Area-T({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if (not self.MatA.rows == self.MatA.cols+1) or self.MatA.rows != 3:
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not 3x2.",
                givenA + f"The Matrix {self.MatA.name} is not 3x2.")
            return
        newList = list()
        for r in range(self.MatA.rows):
            for c in range(self.MatA.cols):
                newList.append(self.checkEntry(self.MatA.allEntries[c + r * self.MatA.cols].textinput.text))
            newList.append(1)
        newMat = self.listToString(newList, self.MatA.rows)
        resultAnswer, textResult = self.determinant_in_weave(newList, self.MatA.rows, False)
        try:
            frac = Fraction(abs(resultAnswer), 2) 
            fractionVersion = f" -> {frac.numerator}" if frac.denominator == 1 else f" -> {frac.numerator}/{frac.denominator}"
        except TypeError:
            fractionVersion = f" -> {self.makeWhileif(abs(round(resultAnswer, 3)))}/2"
        answer = "Answer: Decimal and Fraction Version\n"
        newText = f"3. Multiply The Determinant to +-(1/2)\n{'' if resultAnswer >= 0 else '-'}(1/2) * ({self.makeWhileif(round(resultAnswer, 3))})\n\n{'Three Points is Collinear' if resultAnswer == 0 else 'Three Points is not Collinear'}"
        ColortextResult = (givenA + f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]" + answer + f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Area-Triangle[/color]: {self.makeWhileif(round(abs(resultAnswer*(1/2)), 3))}{fractionVersion}\n\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step by Step:\n"
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]1. Create New Matrix\n{newMat}\n"
            + f"[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]2. Get The Determinant of Matrix\n" + textResult + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Determinant[/color]: {round(resultAnswer, 3)}\n\n" + f"[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]{newText}")
        textResult = (givenA + answer + f"Area-Triangle: {self.makeWhileif(round(abs(resultAnswer*(1/2)), 3))}{fractionVersion}\n\nStep by Step:\n"
                    + f"\n1. Create New Matrix\n{newMat}\n" + "2. Get The Determinant of Matrix\n" + textResult + f"\nDeterminant: {round(resultAnswer, 3)}\n\n" + newText)
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(ColortextResult, textResult)

class TetrahedronMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA

    def changeName(self, name1: str, ____: str):
        self.name = f"Tetra({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if (not self.MatA.rows == self.MatA.cols+1) or self.MatA.rows != 4:
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not 4x3.",
                givenA + f"The Matrix {self.MatA.name} is not 4x3.")
            return
        newList = list()
        for r in range(self.MatA.rows):
            for c in range(self.MatA.cols):
                newList.append(self.checkEntry(self.MatA.allEntries[c + r * self.MatA.cols].textinput.text))
            newList.append(1)
        newMat = self.listToString(newList, self.MatA.rows)
        resultAnswer, textResult = self.find_determinant(newList, self.MatA.rows, False)
        try:
            frac = Fraction(abs(resultAnswer), 6)
            fractionVersion = f" -> {frac.numerator}" if frac.denominator == 1 else f" -> {frac.numerator}/{frac.denominator}"
        except TypeError:
            fractionVersion = f" -> {self.makeWhileif(abs(round(resultAnswer, 3)))}/6"
        answer = "Answer: Decimal and Fraction Version\n"
        result = self.makeWhileif(abs(round(resultAnswer*(1/6), 3)))
        newText = f"3. Multiply The Determinant to +-(1/6)\n{'' if resultAnswer >= 0 else '-'}(1/6) * ({self.makeWhileif(round(resultAnswer, 3))})\n\n{'Four Points is Coplanar' if resultAnswer == 0 else 'Four Points is not Coplanar'}"
        ColortextResult = (givenA + f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]" + answer + f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Tetrahedron[/color]: {result}{fractionVersion}\n\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step by Step:\n"
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]1. Create New Matrix\n{newMat}\n"
            + f"[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]2. Get The Determinant of Matrix\n" + textResult + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Determinant[/color]: {round(resultAnswer, 3)}\n\n" + f"[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]{newText}")
        textResult = (givenA + answer + f"Tetrahedron: {result}{fractionVersion}\n\nStep by Step:\n"
                    + f"\n1. Create New Matrix\n{newMat}\n" + "2. Get The Determinant of Matrix\n" + textResult + f"\nDeterminant: {round(resultAnswer, 3)}\n\n" + newText)
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(ColortextResult, textResult)

class PointMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA

    def changeName(self, ___: str, ____: str):
        self.name = f"{self.MatA.cols}-Point({self.MatA.name})"
        self.mainLabel.text = self.name

    def find_determinant(self, matrixList: list, colSize: int, firstBool: bool):
        textResult = ""
        if colSize == 1:
            textResult += f"({round(matrixList[0], 3)})"
            return matrixList[0], textResult
        if colSize <= 2:
            if firstBool is False: textResult += "("
            textResult += f"({round(matrixList[0], 3)} * {round(matrixList[3], 3)}) - ({round(matrixList[1], 3)} * {round(matrixList[2], 3)}))"
            return (matrixList[0]*matrixList[3]) - (matrixList[1]*matrixList[2]), textResult

        result = 0
        newResult : str = str()
        new_matrix = [0 for _ in range((colSize-1)*(colSize-1))]
        for i in range(colSize):
            index = 0
            for j in range(i):
                for k in range(colSize-1): new_matrix[index + ((colSize-1)*k)] = matrixList[j + (colSize * (k+1))]
                index += 1
            for j in range((colSize-1)-i):
                for k in range(colSize-1): new_matrix[index+((colSize-1)*k)] = matrixList[(i + j + 1) + (colSize * (k + 1))]
                index += 1

            if i % 2 == 0:
                if (i != 0): textResult += " + \n"
                textResult += (f"({round(matrixList[i], 3)} * (") if firstBool else (f"({matrixList[i]} * (")
                r1, r2 = self.find_determinant(new_matrix, colSize-1, True)
                sign = '-' if r1 < 0 else '+'
                if firstBool: result += matrixList[i] * r1
                else: newResult +=  '' if (i+1 != colSize and r1 == 0) else (
                    (f" {'' if (sign == '+' and not newResult) or i == 0 else sign} {abs(r1) if r1 != 1 else ''}{matrixList[i]}")
                    if i + 1 != colSize else f" = {r1* -1}")
                textResult += r2 + (")" * min(colSize - 2, 2))
            else:
                textResult += (f" - \n({round(matrixList[i], 3)} * (") if firstBool else (f" - \n({matrixList[i]} * (")
                r1, r2 = self.find_determinant(new_matrix, colSize-1, True)
                sign = '-' if r1 >= 0 else '+'
                if firstBool: result -= matrixList[i] * r1
                else: newResult +=  '' if (i+1 != colSize and r1 == 0) else (
                    (f" {'' if (sign == '+' and not newResult) else sign} {abs(r1) if r1 != 1 else ''}{matrixList[i]}")
                    if i + 1 != colSize else f" = {r1}")
                textResult += r2 + (")" * min(colSize - 2, 2))

        if firstBool is False: return newResult, textResult
        return result, textResult

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if self.MatA.cols <= 1:
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} must be larger than 1x1.",
                givenA + f"The Matrix {self.MatA.name} must be larger than 1x1.")
            return
        elif not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not a Squared Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not a Squared Matrix.")
            return

        newList = [(string.ascii_lowercase[26-self.MatA.cols:] if self.MatA.cols > 2 else "xy") [i] for i in range(self.MatA.cols)]
        newList.append(1)
        for r in range(self.MatA.rows):
            for c in range(self.MatA.cols):
                newList.append(self.checkEntry(self.MatA.allEntries[c + r * self.MatA.cols].textinput.text))
            newList.append(1)
        newMat = self.listToString(newList, self.MatA.rows+1)
        resultAnswer, textResult = self.find_determinant(newList, self.MatA.cols+1, False)
        ColortextResult = (givenA
            + f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]{self.MatA.cols}-Point Form[/color]: {resultAnswer}\n\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step by Step:\n"
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]1. Create New Matrix\n{newMat}\n"
            + f"[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]2. Get The Determinant of Matrix\n" + textResult)
        textResult = (givenA
            + f"{self.MatA.cols}-Point Form: {resultAnswer}\n\nStep by Step:\n"
            + f"\n1. Create New Matrix\n{newMat}\n"
            + f"2. Get The Determinant of Matrix\n{textResult}")
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(ColortextResult, textResult)

class MinorsMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"Minors({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not a Squared Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not a Squared Matrix.")
            return
        self.firstBool = False
        resultAnswer, textResult = self.find_minors_matrix(self.MatA)
        ColortextResult = (givenA + 
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Minors", self.MatA.rows, self.MatA.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n" + textResult)
        textResult = givenA + self.getAnswerFromResult("Answer: Minors", self.MatA.rows, self.MatA.cols, resultAnswer) + "\nStep By Step:\n" + textResult
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.rows, self.MatA.cols)


class CofactorMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"Cofactor({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not Squared Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not Squared Matrix.")
            return
        resultAnswer, textResult, anotherResult = self.find_minors_matrix(self.MatA, True)
        newString = ""
        for r in range(self.MatA.rows):
            newString += "| "
            for c in range(self.MatA.cols): newString += str(anotherResult[c + r * self.MatA.cols]) + f" * (-1)^{r}+{c} | "
            newString += "\n"

        ColortextResult = (givenA + 
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Cofactor", self.MatA.rows, self.MatA.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]1. Get The Minors of the Matrix {self.MatA.name}\n" + textResult
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]2. Get The Cofactor using (-1)^i+j\n" + newString)
        textResult = (givenA + 
            self.getAnswerFromResult("Answer: Cofactor", self.MatA.rows, self.MatA.cols, resultAnswer)
            + "\nStep By Step:\n" + f"1. Get The Minors of the Matrix {self.MatA.name}\n" + textResult
            + "\n2. Get The Cofactor using (-1)^i+j\n" + newString)
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.rows, self.MatA.cols)

class AdjugateMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA

    def changeName(self, name1: str, ____: str):
        self.name = f"Adjugate({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not Squared Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not Squared Matrix.")
            return

        resultAnswer, textResult, anotherResult = self.find_minors_matrix(self.MatA, True)
        newString2 = ""
        for r in range(self.MatA.rows):
            newString2 += "| "
            for c in range(self.MatA.cols): newString2 += str(anotherResult[c + r * self.MatA.cols]) + f" * (-1)^{r}+{c} | "
            newString2 += "\n"
        copyList = copy.deepcopy(resultAnswer)
        newString = ""
        for j in range(min(self.MatA.rows, 5)):
            newString += "| "
            for i in range(min(self.MatA.cols, 5)):
                newString += f"{round(resultAnswer[i + j * self.MatA.cols], 3)} | "
                resultAnswer[i + j * self.MatA.cols] = copyList[j + i * self.MatA.cols]
            newString += " ->  | "
            for i in range(min(self.MatA.cols, 5)): newString += f"{round(copyList[j + i * self.MatA.cols], 3)} | "
            newString += "\n"
        
        ColortextResult = (givenA + 
            self.getAnswerFromResult(f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Adjugate Matrix {self.MatA.name}", self.MatA.rows, self.MatA.cols, resultAnswer)
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]1. Get The Minors of the Matrix {self.MatA.name}\n" + textResult
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]2. Get The Cofactor using (-1)^i+j\n" + newString2
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]3. Transpose The Matrix\n" + newString)
        textResult = (givenA + 
            self.getAnswerFromResult(f"Answer: Adjugate Matrix {self.MatA.name}", self.MatA.rows, self.MatA.cols, resultAnswer)
            + "\nStep By Step:\n" + f"1. Get The Minors of the Matrix {self.MatA.name}\n" + textResult
            + "\n2. Get The Cofactor using (-1)^i+j\n" + newString2
            + "\n3. Transpose The Matrix\n" + newString)
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, resultAnswer, self.MatA.rows, self.MatA.cols)

class InverseMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"Inv({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if not self.isSquaredMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not Squared Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not Squared Matrix.")
            return
    
        determinant, determinantTextResult = self.find_determinant(self.turnMatrixEntriesNewList(self.MatA), self.MatA.cols, False)
        if determinant == 0:
            ColordeterminantTextResult = (givenA +
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not Invertible\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Determinant[/color]: {determinant}\n\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step by Step:\n" + determinantTextResult)
            determinantTextResult = givenA + f"The Matrix {self.MatA.name} is not Invertible\nDeterminant: {round(determinant, 3)}\n\nStep by Step:\n" + determinantTextResult
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(ColordeterminantTextResult, determinantTextResult)
            return

        resultAnswer, textResult, anotherResult = self.find_minors_matrix(self.MatA, True)
        cofactorString = ""
        for r in range(self.MatA.rows):
            cofactorString += "| "
            for c in range(self.MatA.cols): cofactorString += str(anotherResult[c + r * self.MatA.cols]) + f" * (-1)^{r}+{c} | "
            cofactorString += "\n"
        copyList = copy.deepcopy(resultAnswer)
        newString = ""
        for j in range(min(self.MatA.rows, 5)):
            newString += "| "
            for i in range(min(self.MatA.cols, 5)):
                newString += f"{round(resultAnswer[i + j * self.MatA.cols], 3)} | "
                resultAnswer[i + j * self.MatA.cols] = copyList[j + i * self.MatA.cols]
            newString += " ->  | "
            for i in range(min(self.MatA.cols, 5)): newString += f"{round(copyList[j + i * self.MatA.cols], 3)} | "
            newString += "\n"
        
        newString2 = ""
        for r in range(self.MatA.rows):
            newString2 += "| "
            for c in range(self.MatA.cols): newString2 += f"{round(resultAnswer[c + (r * self.MatA.cols)], 3)} * (1 / {round(determinant, 3)}) | "
            newString2 += "\n"
        
        answerString = ""
        newResultAnswer = list()
        for r in range(self.MatA.rows):
            answerString += "| "
            for c in range(self.MatA.cols):
                first = round(resultAnswer[c + (r * self.MatA.cols)] * (1 / determinant), 3)
                first = int(first) if first == int(first) else first
                newResultAnswer.append(first)
                answerString += f"{first} | "
            answerString += " ->  | "
            for c in range(self.MatA.cols):
                try:
                    first = Fraction(resultAnswer[c + (r * self.MatA.cols)], determinant)
                    answerString += f"{first.numerator}/{first.denominator} | " if first.denominator != 1 else f"{first.numerator} | "
                except TypeError:
                    first = round(resultAnswer[c + (r * self.MatA.cols)], 3)
                    first = int(first) if first == int(first) else first
                    second = round(determinant, 3)
                    second = int(second) if second == int(second) else second
                    answerString += f"{first}/{second}"                
            answerString += "\n"

        ColortextResult = (givenA + 
            f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Inverse of Matrix {self.MatA.name}\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Decimal Inverse and Fraction Version\n" + answerString
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]1. Get The Determinant of Matrix {self.MatA.name}\n" + determinantTextResult
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Determinant[/color] = {round(determinant, 3)}\n"
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]2. Get The Minors of the Matrix {self.MatA.name}\n" + textResult
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]3. Get The Cofactor using (-1)^i+j\n" + cofactorString
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]4. Transpose The Matrix\n" + newString
            + f"\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]5. Scalar using the 1 / Determinant\n" + newString2)
        textResult = (givenA + 
            f"Answer: Inverse of Matrix {self.MatA.name}\nDecimal Inverse and Fraction Version\n" + answerString
            + "\nStep By Step:\n" + f"1. Get The Determinant of Matrix {self.MatA.name}\n" + determinantTextResult + f"\nDeterminant = {round(determinant, 3)}\n"
            + f"\n2. Get The Minors of the Matrix {self.MatA.name}\n" + textResult
            + "\n3. Get The Cofactor using (-1)^i+j\n" + cofactorString
            + "\n4. Transpose The Matrix\n" + newString + f"\n5. Scalar using the 1 / Determinant\n" + newString2)
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabel(ColortextResult, textResult, newResultAnswer, self.MatA.rows, self.MatA.cols)

class CramersRuleMatrixFunction(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
    
    def changeName(self, name1: str, ____: str):
        self.name = f"Cramers({name1})"
        self.mainLabel.text = self.name

    def functions(self):
        givenA = self.getMatrixGiven(self.MatA)
        if not self.isAugmentedMatrix(self.MatA):
            self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(givenA + 
                f"[color={self.MainApp.CT.CurrentTheme.ERROR_COLOR}]The Matrix {self.MatA.name} is not an Augmented Matrix.",
                givenA + f"The Matrix {self.MatA.name} is not an Augmented Matrix.")
            return
        textResult : str = str()
        DeterminantStringColor : str = str()
        allDeterminantList : list[list[float]] = list()
        allDeterminant : list[int] = list()
    
        for newCols in range(self.MatA.cols):
            allDeterminantList.append(list())
            for r in range(self.MatA.rows):
                for c in range(self.MatA.cols-1):
                    value = self.checkEntry(self.MatA.allEntriesValue[c][r])
                    allDeterminantList[newCols].append(value)
            if newCols:
                for newR in range(self.MatA.rows):
                    allDeterminantList[newCols][(newCols-1) + (newR * (self.MatA.cols-1))] = self.checkEntry(self.MatA.allEntriesValue[self.MatA.cols-1][newR])

            det, txt = self.find_determinant(allDeterminantList[newCols], self.MatA.cols-1, False)
            allDeterminant.append(det)
            DeterminantStringColor += f"A{newCols if newCols else ''}:\n{self.listToString(allDeterminantList[newCols], self.MatA.cols-1)}[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Determinant[/color] = {self.makeWhileif(det)}\n{txt}\n\n"
            textResult += f"A{newCols if newCols else ''}:\n{self.listToString(allDeterminantList[newCols], self.MatA.cols-1)}Determinant = {self.makeWhileif(det)}\n{txt}\n\n"
        answerString : str = str()
        ColoredanswerString : str = str()

        divideString : str = str()
        ColoreddivideString : str = str()
        if allDeterminant[0] == 0:
            for i in range(1, len(allDeterminant)):
                if allDeterminant[i] != 0:
                    answerString = "No Solution\n"
                    divideString += f"Since |A| is 0 and 1 of determinant of Matrix {self.MatA.name} is not 0.\nThis Matrix {self.MatA.name} has no Solution.\n"
                    break
            else:
                answerString = "Infinite Solution\n"
                divideString += f"Since |A| is 0 and All the determinant of Matrix {self.MatA.name} is 0.\nThis Matrix {self.MatA.name} has infinitely many Solution.\n"
            ColoreddivideString = divideString
        else:
            answerString += f"Decimal and Fraction Version\n"
            ColoredanswerString += f"[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Decimal and Fraction Version\n"
            divideString += f"2. Divide all calculated Determinant to Main Determinant of the Matrix {self.MatA.name}\n"
            ColoreddivideString += f"[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]2. Divide all Determinant to |A| of the Matrix {self.MatA.name}\n"
            for i in range(1, len(allDeterminant)):
                string : str = str()
                try:
                    first = Fraction(allDeterminant[i], allDeterminant[0])
                    string += f"{first.numerator}/{first.denominator}" if first.denominator != 1 else f"{first.numerator}"
                except TypeError:
                    first = self.makeWhileif(round(allDeterminant[i], 3))
                    second = self.makeWhileif(round(allDeterminant[0], 3))
                    string += f"{first}/{second}"
                divideString += f"x{i} = {self.makeWhileif(round(allDeterminant[i], 3))}/{self.makeWhileif(round(allDeterminant[0], 3))}\n"
                ColoreddivideString += f"x{i} = {self.makeWhileif(round(allDeterminant[i], 3))}/{self.makeWhileif(round(allDeterminant[0], 3))}\n"
                answerString += f"x{i} = {self.makeWhileif(round(allDeterminant[i]/allDeterminant[0], 3))}  ->  {string}\n"
                ColoredanswerString += f"x{i} = {self.makeWhileif(round(allDeterminant[i]/allDeterminant[0], 3))}  ->  {string}\n"
        
        ColortextResult = (givenA + 
            f"[color={self.MainApp.CT.CurrentTheme.TITLE_COLOR}]Answer: Solve Matrix Cramers\n" + ColoredanswerString
            + f"\n[color={self.MainApp.CT.CurrentTheme.STEP_BY_STEP}]Step By Step:\n[color={self.MainApp.CT.CurrentTheme.NUMBER_COLOR}]1. Get The Determinant\n"
            + DeterminantStringColor + "\n" + ColoreddivideString)
        textResult = (givenA + 
            f"Answer: Solve Matrix Cramers\n" + answerString
            + f"\nStep By Step:\n1. Get The Determinant\n"
            + textResult + "\n" + divideString)
        self.parent.parent.parent.parent.MatrixResult.turnStringToLabelF(ColortextResult, textResult)

class ChangeButton(MatrixFunction):
    
    def __init__(self, MatA: MatrixHolder, MatB: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
        self.MatB = MatB
    
    def changeName(self, name1: str, name2: str):
        self.name = f"{name1} <-> {name2}"
        self.mainLabel.text = self.name

    def functions(self):
        self.MatA.name, self.MatB.name = self.MatB.name, self.MatA.name
        for text in self.MatA.parent.allFunctionsWidget.grid.children:
            text.changeName(self.MatA.name, self.MatB.name)
        self.MatA.rows, self.MatB.rows = self.MatB.rows, self.MatA.rows
        self.MatA.cols, self.MatB.cols = self.MatB.cols, self.MatA.cols
        self.MatA.allEntriesValue, self.MatB.allEntriesValue = self.MatB.allEntriesValue, self.MatA.allEntriesValue
        self.MatA.changeMatrix()
        self.MatB.changeMatrix()

class MatrixAtoB(MatrixFunction):

    def __init__(self, MatA: MatrixHolder, MatB: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
        self.MatB = MatB

    def changeName(self, name1: str, name2: str):
        self.name = f"{name1} -> {name2}"
        self.mainLabel.text = self.name

    def functions(self):
        mat1 = self.MatA
        mat2 = self.MatB
        mat2.rows, mat2.cols = mat1.rows, mat1.cols
        for index, text in enumerate(mat1.allEntriesValue):
            mat2.allEntriesValue[index] = text
        mat2.changeMatrix()

class MatrixBtoA(MatrixFunction):

    def __init__(self, MatA: MatrixHolder, MatB: MatrixHolder, name: str = "Function", **kwargs):
        super().__init__(name, **kwargs)
        self.MatA = MatA
        self.MatB = MatB

    def changeName(self, name1: str, name2: str):
        self.name = f"{name2} -> {name1}"
        self.mainLabel.text = self.name

    def functions(self):
        mat1 = self.MatA
        mat2 = self.MatB
        mat1.rows, mat1.cols = mat2.rows, mat2.cols
        for index, text in enumerate(mat2.allEntriesValue):
            mat1.allEntriesValue[index] = text
        mat1.changeMatrix()

class OpenResultBox(CustomWidget):
    
    def __init__(self, name: str, **kwargs):
        size = ((Window.width * 0.8, Window.height*0.05) if Window.width < Window.height else
                (Window.width * 0.8, Window.height*0.08))
        pos = (Window.width*0.1, ((Window.height - ((Window.height*0.2)*3)) - (Window.height*0.01) - ((((Window.height*0.2) / 4) * 1.5) * (4+1)) ))
        super().__init__(pos, size, name, False, **kwargs)
        app = App.get_running_app()
        self.displayDesign(
            app.CT.CurrentTheme.FUNC_BUTTON_LINE,
            app.CT.CurrentTheme.FUNC_BUTTON_COLOR,
            app.CT.CurrentTheme.FUNC_BUTTON_PRESSED,
            app.CT.CurrentTheme.FUNC_BUTTON_FG)

    def on_touch_down(self, touch):
        if self.parent.disabledResult is False:
            super().on_touch_down(touch)

    def functions(self):
        if self.parent.MatrixResult.isFullSize:
            self.parent.MatrixResult.closeResult()
        else:
            self.parent.MatrixResult.showResult()
            if self.parent.allFunctionsWidget.opened:
                self.parent.allFunctionsWidget.close()
