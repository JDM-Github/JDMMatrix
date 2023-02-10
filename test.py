from plyer import filechooser
from kivy.app import runTouchApp, App
from kivy.uix.widget import Widget
from kivy.uix.filechooser import FileChooser

class Test(Widget):
    
    def on_touch_down(self, touch):
        self.add_widget(FileChooser())

class test(App):
    
    def build(self):
        return Test()

if __name__ == "__main__":
    test().run()
# runTouchApp(FileChooser())