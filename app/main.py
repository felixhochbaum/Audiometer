from .ui import setup_ui
from .model import *

class Controller():

    def __init__(self):
        program_functions = {"Klassisches Audiogramm" : self.start_standard_procedure,
                             "Kurzes Screening" : self.start_screen_procedure,
                             "Kalibrierung" : self.start_calibration}
        
        self.selected_program = ""
        self.calibration_funcs = [self.start_calibration, self.calibration_next_freq, self.calibration_repeat_freq, self.stop_sound, self.calibration_set_level]
        self.view = setup_ui(self.start_familiarization, self.create_audiogram, 
                             program_functions, self.calibration_funcs)

        # helper variable for calibration
        self.button_changed = False
        
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
        self.selected_program = "calibration"
        self.calibration = Calibration(startlevel=level, headphone_name=headphone)
        _, current_freq, current_spl = self.calibration_next_freq()
        return current_freq, current_spl

    def calibration_next_freq(self):
        more_freqs, current_freq, current_spl = self.calibration.play_one_freq()
        if more_freqs:
            return True, current_freq, current_spl
        elif self.button_changed == False:
            self.button_changed = True
            return False, current_freq, current_spl
        else:
            self.calibration.finish_calibration()
            return False, current_freq, current_spl

    def calibration_repeat_freq(self):
        self.calibration.repeat_freq()

    def calibration_set_level(self, spl):
        self.calibration.set_calibration_value(spl)

    def stop_sound(self):
        self.calibration.stop_playing()