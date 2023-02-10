import kivy

kivy.require("1.9.1")
import json
from plyer import orientation
from theme import Theme
from src import Toast
from configuration import WINDOW_WIDTH, WINDOW_HEIGHT
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase

LabelBase.register(
    fn_regular="asset/consolas.ttf",
    name="consolas")

if kivy.platform != "android": 
    Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    Window.left = 5
    Window.top = 30
from kivy.app import App
from newUI import MainScreenWidget


class MatrixCalculator(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "asset/icon.png"
        try:
            with open("config.json") as f: self.Matrixconfig = json.load(f)
        except json.decoder.JSONDecodeError:
            with open("config.json", "w") as f: json.dump({"Allmatrix": ["A", "B", "C", "D", "E", "F"]}, f)
            with open("config.json") as f: self.Matrixconfig = json.load(f)
        self.allVariables()
        self.CT = Theme()
        self.CT.CurrentTheme = getattr(self.CT, (self.Matrixconfig.get("CurrentTheme") if self.Matrixconfig.get("CurrentTheme") else "ORIGINAL"))

    def restart(self, theme: str):
        self.Matrixconfig["CurrentTheme"] = theme
        self.matrixCalc.MatrixFunctions.MatrixResult.coloredResultString = self.matrixCalc.MatrixFunctions.MatrixResult.resultString
        self.saveConfig()
        self.realWidget.clear_widgets()
        self.CT.CurrentTheme = getattr(self.CT, self.Matrixconfig.get("CurrentTheme"))
        self.matrixCalc = MainScreenWidget()
        self.realWidget.add_widget(self.matrixCalc)
        Toast(f"Current Theme: {theme}", duration=3).start()

    def allVariables(self):
        config = self.Matrixconfig
        self.allMatrixHolder = dict()
        for name in self.Matrixconfig.get("Allmatrix"):
            self.allMatrixHolder[name] = [3 if not config.get(f"{name}Rows") else config.get(f"{name}Rows"),
                  3 if not config.get(f"{name}Cols") else config.get(f"{name}Cols"),
                  [["0" for _ in range(10)] for __ in range(10)] if not config.get(f"{name}EValue") else config.get(f"{name}EValue")]
        self.graphSave = 0 if not config.get("GraphSaveCount") else config.get("GraphSaveCount")

    def saveConfig(self):
        allName = list(self.allMatrixHolder.keys())
        holder = self.allMatrixHolder
        self.matrixCalc.addTheme()
        self.Matrixconfig["CurrentFirst"] = self.matrixCalc.MatrixFunctions.firstMatrixHolder.name
        self.Matrixconfig["CurrentSecond"] = self.matrixCalc.MatrixFunctions.secondMatrixHolder.name
        for index in range(len(self.allMatrixHolder)):
            self.Matrixconfig[f"{allName[index]}Rows"] = holder.get(f"{allName[index]}")[0]
            self.Matrixconfig[f"{allName[index]}Cols"] = holder.get(f"{allName[index]}")[1]
            self.Matrixconfig[f"{allName[index]}EValue"] = holder.get(f"{allName[index]}")[2]
        self.Matrixconfig["ResultList"] = self.matrixCalc.MatrixFunctions.MatrixResult.resultList
        self.Matrixconfig["CResultString"] = self.matrixCalc.MatrixFunctions.MatrixResult.coloredResultString
        self.Matrixconfig["ResultString"] = self.matrixCalc.MatrixFunctions.MatrixResult.resultString
        self.Matrixconfig["ResultRows"] = self.matrixCalc.MatrixFunctions.MatrixResult.resultRows
        self.Matrixconfig["ResultCols"] = self.matrixCalc.MatrixFunctions.MatrixResult.resultCols
        self.Matrixconfig["LastScreen"] = self.matrixCalc.sm.old_Screen
        self.Matrixconfig["CurrentScreen"] = self.matrixCalc.sm.current
        self.Matrixconfig["GraphSaveCount"] = self.graphSave
        with open("config.json", "w") as f: json.dump(self.Matrixconfig, f, indent=4, separators=(',', ': '))

    def on_stop(self):
        self.saveConfig()
        self.Matrixconfig["LastScreen"] = "Main"
        self.Matrixconfig["CurrentScreen"] = "Main"
        with open("config.json", "w") as f: json.dump(self.Matrixconfig, f, indent=4, separators=(',', ': '))
        return super().on_stop()

    def on_start(self):
        if kivy.platform == "android": orientation.set_portrait()
        Window.bind(on_keyboard=self.hook_keyboard)
        return super().on_start()

    def hook_keyboard(self, _, key, *__):
        if key == 27:
            self.matrixCalc.addTheme()
            if self.matrixCalc.MatrixFunctions.MatrixResult.isFullSize:
                self.matrixCalc.MatrixFunctions.MatrixResult.closeResult()
            elif self.matrixCalc.MatrixFunctions.allFunctionsWidget.opened:
                self.matrixCalc.MatrixFunctions.allFunctionsWidget.close()
            elif self.matrixCalc.sm.current == "Theme":
                self.matrixCalc.sm.transition.direction = "right"
                self.matrixCalc.sm.change_Screen = self.matrixCalc.sm.old_Screen
            elif self.matrixCalc.sm.current == "Field":
                self.matrixCalc.sm.transition.direction = "right"
                self.matrixCalc.sm.change_Screen = "Main"
            elif self.matrixCalc.sm.current == "Graph":
                self.matrixCalc.graph.removeAll()
                self.matrixCalc.sm.transition.direction = "right"
                self.matrixCalc.sm.change_Screen = self.matrixCalc.sm.old_Screen
            elif self.matrixCalc.exitScreen.isExitScreen:
                self.matrixCalc.exitScreen.close()
                self.stop()
            else: self.matrixCalc.exitScreen.show()
            return True

    def build(self):
        self.realWidget = Widget()
        self.matrixCalc = MainScreenWidget()
        self.realWidget.add_widget(self.matrixCalc)
        return self.realWidget

if __name__ == "__main__": 
    MatrixCalculator().run()
