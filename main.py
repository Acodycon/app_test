import kivy
from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button

class main_logic(PageLayout):

    def __init__(self, **kwargs):
        super(main_logic, self).__init__(**kwargs)
        for i in range(7):
            self.add_widget(Button(text=str(i+1)))

class mainapp(App):
    def build(self):
        return main_logic()
    
if __name__ == "__main__":
    mainapp().run()