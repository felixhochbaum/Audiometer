from .ui import setup_ui
from .model import *
from .dummy_model import StandardProcedure, TestProcedure
from .audiogram import create_audiogram

class Controller():

    def __init__(self):
        program_functions = {"Klassisches Audiogramm" : self.start_standard_procedure,
                             "Test" : self.start_test_procedure}
        
        self.familiarization = Familiarization()
        self.standard_procedure = StandardProcedure()
        self.test_procedure = TestProcedure()
        self.view = setup_ui(self.start_familiarization, 
                             program_functions) 
    def run_app(self):
        self.view.mainloop()

    def start_familiarization(self):
        self.familiarization.familiarize()

    def start_standard_procedure(self):
        self.standard_procedure.standard_test()

    def start_test_procedure(self):
        self.test_procedure.test_test()
