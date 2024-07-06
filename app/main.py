from .ui import setup_ui
from .model import *

class Controller():

    def __init__(self):
        program_functions = {"Klassisches Audiogramm" : self.start_standard_procedure,
                             "Kurzes Screening" : self.start_screen_procedure,
                             "Kalibrierung" : self.start_calibration}
        
        self.selected_program = ""

        self.view = setup_ui(self.start_familiarization, self.create_audiogram, 
                             program_functions)

         
        
    def run_app(self):
        self.view.mainloop()

    def start_familiarization(self, id="", headphone="Sennheiser_HDA200", calibrate=True, **additional_data):
        self.familiarization = Familiarization(id=id, headphone_name=headphone, calibrate=calibrate, **additional_data)
        return self.familiarization.familiarize()
    
    def create_audiogram(self):
        if self.selected_program == "standard":
            return self.standard_procedure.create_final_audiogram(self.familiarization.get_temp_csv_filename()) 
        elif self.selected_program == "screening":
            return self.screen_procedure.create_final_audiogram(self.familiarization.get_temp_csv_filename())
        else:
            print("There was an error, no process selected.")
            self.screen_procedure = ScreeningProcedure("")
            return self.screen_procedure.create_final_audiogram(None)

    def start_standard_procedure(self, binaural=False, headphone="Sennheiser_HDA200", calibrate=True, **additional_data):
        self.selected_program = "standard"
        self.standard_procedure = StandardProcedure(self.familiarization.get_temp_csv_filename(), headphone_name=headphone, calibrate=calibrate, **additional_data)
        self.standard_procedure.standard_test(binaural)

    def start_screen_procedure(self, binaural=False, headphone="Sennheiser_HDA200", calibrate=True, **additional_data):
        self.selected_program = "screening"
        self.screen_procedure = ScreeningProcedure(self.familiarization.get_temp_csv_filename(), headphone_name=headphone, calibrate=calibrate, **additional_data)
        self.screen_procedure.screen_test(binaural)

    def start_calibration(self, level, headphone="Sennheiser_HDA200"):
        self.selected_program = "Calibration"
        self.calibration = Calibration(startlevel=level, headphone_name=headphone)

    def calibration_next_freq(self, level):
        if self.selected_program != "Calibration":
            self.start_calibration()