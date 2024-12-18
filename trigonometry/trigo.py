# from .matrixHolder import MatrixHolder
# from .matrixFunction import (
#     MatrixFunctionMenu,
#     OpenResultBox,
# )
from src.useFulfunction import CustomWidget
from .trigoMenu import TrigoMenu
# from .result import MatrixResultBox
from kivy.app import App
from kivy.utils import get_color_from_hex as GetColor

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from math import sin, cos, tan, radians
from matplotlib.backends.backend_agg import FigureCanvasAgg
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import matplotlib.pyplot as plt
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

class Trigonometry(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.allBooleanDisabler()
        self.higherWidget()

    def allBooleanDisabler(self):
        self.disabledFunction = False
        self.disabledHolder = False
        self.disabledMenu = False
        self.disabledResult = False

    def higherWidget(self):
        self.trigoMenu = TrigoMenu()
        self.trigoMenu2 = TrigoMenu2()
        self.trigoBody = TrigoBody()
        self.add_widget(self.trigoMenu)
        self.add_widget(self.trigoMenu2)
        self.add_widget(self.trigoBody)

class TrigoBody(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.size = (Window.width, Window.height*0.3)
        self.pos = (0, Window.height * 0.6)

        # self.description_label = Label(
        #     text="Welcome to the Trigonometry Body!\nThis area can display additional trigonometric info.",
        #     size_hint=(1, 0.3)
        # )
        # self.add_widget(self.description_label)

        # self.extra_info_label = Label(
        #     text="Use the menu above to perform calculations.\nThis section will be updated with details soon.",
        #     size_hint=(1, 0.2)
        # )
        # self.add_widget(self.extra_info_label)

class CustomButton(CustomWidget):

    def __init__(self, name: str, **kwargs):
        Rmax = 3
        size = (Window.width / Rmax, ((Window.height*0.2) / 4) if Window.width < Window.height else ((Window.width*0.2) / 4))
        pos = (-120, -200)
        super().__init__(pos, size, name, True, **kwargs)

class EntriesTextInput(TextInput):

    def __init__(self, size, pos, **kwargs):
        super().__init__(**kwargs)
        self.getFocused = False
        self.size = size
        self.pos = pos
        self.background_normal = ""
        self.background_active = ""
        app = App.get_running_app()
        self.displayDesign(
            app.CT.CurrentTheme.MATRIX_ENTRY_SELECTION,
            app.CT.CurrentTheme.MATRIX_ENTRY_FG,
            app.CT.CurrentTheme.MATRIX_ENTRY_COLOR,
            app.CT.CurrentTheme.MATRIX_ENTRY_CURSOR)
        self.bind(text=self.changeText)

    def displayDesign(self, Selection: str, ForeGround: str, MColor: str, Cursor: str):
        self.hint_text_color = GetColor(ForeGround)
        self.selection_color = GetColor(Selection)
        self.foreground_color = GetColor(ForeGround)
        self.background_color = GetColor(MColor)
        self.cursor_color = GetColor(Cursor)

    def on_focus(self, _, focus):
        if focus: Clock.schedule_once(lambda _: self.select_all(), 0.2)

    def changeText(self, *_):
        pass
        # self.parent.parent.allEntriesValue[self.parent.offset[1]][self.parent.offset[0]] = self.text
        # self.parent.parent.MainApp.allMatrixHolder.get(self.parent.parent.name)[2][self.parent.offset[1]][self.parent.offset[0]] = self.text

class TrigoMenu2(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.size = (Window.width, Window.height*0.9)
        self.pos = (0, 10)

        self.angle_input = EntriesTextInput(size=(Window.width*0.95, 50),
            pos=(Window.width * 0.025, 50),
            hint_text="Enter angle in degrees", multiline=False, size_hint=(1, None), height=50)
        self.add_widget(self.angle_input)

        self.result_label = Label(text="Result will appear here", size_hint=(1, None), height=50)
        self.add_widget(self.result_label)

        self.graph_image = Image(size_hint=(1, 1))
        self.add_widget(self.graph_image)

        self.buttons_layout = BoxLayout(size_hint=(1, None), height=50)

        self.sin_button = CustomButton(name="Sin")
        self.sin_button.func_binder = lambda *_: self.calculate_sin()
        self.cos_button = CustomButton(name="Cos")
        self.cos_button.func_binder = lambda *_: self.calculate_cos()
        self.tan_button = CustomButton(name="Tan")
        self.tan_button.func_binder = lambda *_: self.calculate_tan()

        self.buttons_layout.add_widget(self.sin_button)
        self.buttons_layout.add_widget(self.cos_button)
        self.buttons_layout.add_widget(self.tan_button)

        self.add_widget(self.buttons_layout)

    def calculate_sin(self):
        self.calculate_trig_function(sin, "Sin")

    def calculate_cos(self):
        self.calculate_trig_function(cos, "Cos")

    def calculate_tan(self):
        self.calculate_trig_function(tan, "Tan")

    def calculate_trig_function(self, func, func_name):
        try:
            angle = float(self.angle_input.text)
            result = func(radians(angle))
            self.result_label.text = f"{func_name}({angle}) = {result:.4f}"

            fig, ax = plt.subplots()
            angles = range(0, 361)
            values = [func(radians(a)) for a in angles]
            ax.plot(angles, values, label=f"{func_name}(x)")
            ax.axhline(0, color='black', linewidth=0.8)
            ax.axvline(0, color='black', linewidth=0.8)
            ax.set_xlabel("Angle (degrees)")
            ax.set_ylabel(f"{func_name}(x)")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)

            filepath = "temp_graph.png"
            fig.savefig(filepath, dpi=100)
            plt.close(fig)

            self.graph_image.source = filepath
            self.graph_image.reload()

        except ValueError:
            self.result_label.text = "Invalid input. Please enter a valid number."
        except OverflowError:
            self.result_label.text = f"{func_name}({angle}) is undefined."