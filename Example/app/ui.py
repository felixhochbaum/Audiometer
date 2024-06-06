import tkinter as tk
import tkinter.ttk as ttk
import threading

class App(tk.Tk):
    def __init__(self, familiarization_func, *program_funcs):
        super().__init__()
        self.title("Sound Player")
        self.geometry("800x800")
        
        self.frames = {}
        for F in (FamiliarizationPage, StandardProgramPage, ResultPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        frame = DuringFamiliarizationView(self, familiarization_func)
        self.frames[DuringFamiliarizationView] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        for i, program_func in enumerate(program_funcs):
            frame = DuringProcedureView(self, program_func, text="Programm {} läuft...".format(i+1))
            self.frames[DuringProcedureView] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FamiliarizationPage)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def wait_for_process(self, process, callback):
        threading.Thread(target=self.run_process, args=(process, callback)).start()

    def run_process(self, process, callback):
        process()
        self.after(0, callback)


class FamiliarizationPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.play_button = ttk.Button(self, 
                                      text="Starte Eingewöhnung", 
                                      command=self.start_familiarization)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)

    def start_familiarization(self):
        self.parent.show_frame(DuringFamiliarizationView)
        self.parent.wait_for_process(self.parent.frames[DuringFamiliarizationView].program, self.end_familiarization)

    def end_familiarization(self):
        self.parent.show_frame(StandardProgramPage) 


class StandardProgramPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.done_button = ttk.Button(self, text="Dummy")
        self.done_button.grid(row=0, column=0, padx=10, pady=10)



class DuringFamiliarizationView(ttk.Frame):
    def __init__(self, parent, familiarization_func):
        super().__init__(parent)
        self.parent = parent
        self.program = familiarization_func
        self.text = "Eingewöhnung läuft..."
        self.create_widgets()

    def create_widgets(self):
        self.info = ttk.Label(self, text=self.text)
        self.info.grid(row=0, column=0, padx=10, pady=10)


class DuringProcedureView(ttk.Frame):
    def __init__(self, parent, program_func, text):
        super().__init__(parent)
        self.parent = parent
        self.program = program_func
        self.text = text
        self.create_widgets()

    def create_widgets(self):
        self.info = ttk.Label(self, text=self.text)
        self.info.grid(row=0, column=0, padx=10, pady=10)


class ResultPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent




def setup_ui(startfunc):
    app = App(startfunc)
    return app

