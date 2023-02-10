from kivy.uix.label import Label
from kivy.uix.image import Image

class Label2(Label): ...

class NewImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "asset/mainBg0.png"