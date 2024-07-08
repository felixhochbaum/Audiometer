from .ui import setup_ui
from .model import *

class Controller():

    def __init__(self):
        program_functions = {"Klassisches Audiogramm" : self.start_standard_procedure,
                             "Kurzes Screening" : self.start_screen_procedure}

        self.view = setup_ui(self.start_familiarization, program_functions)
        
    def run_app(self):
        self.view.mainloop()

    def start_familiarization(self, id="", **additional_data):
        self.familiarization = Familiarization(id=id, **additional_data)
        return self.familiarization.familiarize()

    def start_standard_procedure(self, binaural=False, **additional_data):
        self.selected_program = "standard"
        self.standard_procedure = StandardProcedure(self.familiarization.get_temp_csv_filename(), **additional_data)
        self.standard_procedure.standard_test(binaural)

    def start_screen_procedure(self, binaural=False, **additional_data):
        self.selected_program = "screening"
        self.screen_procedure = ScreeningProcedure(self.familiarization.get_temp_csv_filename(), **additional_data)
        self.screen_procedure.screen_test(binaural)
