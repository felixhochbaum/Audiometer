from .ui import setup_ui
from .ui_alternative import setup_ui_alternative
from .model import *

class Controller():
    def __init__(self):
        self.model = Familiarization()
        self.view = setup_ui_alternative(self.start)

    def run_app(self):
        self.view.mainloop()

    def start(self):
        self.model.familiarize()
    #app = setup_ui()
    #app = setup_ui_alternative(self.)
    #app.mainloop()
