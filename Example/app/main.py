from .ui import setup_ui
#from .model import *
from .dummy_model import *

class Controller():
    def __init__(self):
        self.familiarization = Familiarization()
        self.procedure = StandardProcedure()
        self.view = setup_ui(self.start_familiarization, 
                             self.standard_procedure) # add more procedures later

    def run_app(self):
        self.view.mainloop()

    def start_familiarization(self):
        self.familiarization.familiarize()

    def standard_procedure(self):
        self.procedure.standard_test()
