from .ui import setup_ui
#from .model import *
from .dummy_model import *

class Controller():
    def __init__(self):
        self.model = Familiarization()
        self.view = setup_ui(self.start)

    def run_app(self):
        self.view.mainloop()

    def start(self):
        self.model.familiarize()

