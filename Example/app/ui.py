import tkinter as tk
import tkinter.ttk as ttk
import threading


class App(tk.Tk):

    def __init__(self, familiarization_func, *program_funcs):
        """Main application window. Contains all pages and controls the flow of the program.

        Args:
            familiarization_func (function): function to be called for familiarization
            *program_funcs (function): function(s) to be called for the main program
        """
        super().__init__()

        # General settings
        self.title("Sound Player")
        self.geometry("800x800")
        # TODO add more settings

        # Store results ->  TODO: needs to be changed
        self.results = "Hier sollten später Ergebnisse angezeigt werden"
        
        # Dictionary to store all pages
        self.frames = {}

        # Pages, where the user can interact
        for F in (FamiliarizationPage, StandardProgramPage, ResultPage): #TODO add menu page
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # View during familiarization
        frame = DuringFamiliarizationView(self, familiarization_func)
        self.frames[DuringFamiliarizationView] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # Views during program(s) 
        for i, program_func in enumerate(program_funcs):
            frame = DuringProcedureView(self, program_func, text="Programm {} läuft...".format(i+1)) #TODO change this to usefull information, this is just for testing purposes
            self.frames[DuringProcedureView] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show FamiliarizationPage first
        self.show_frame(FamiliarizationPage) #change this to MenuPage later


    def show_frame(self, page):
        """Show a frame for the given page name

        Args:
            page(class): class of the page to be shown
        """
        frame = self.frames[page]
        frame.tkraise()


    def wait_for_process(self, process, callback):
        """Starts a process in a new thread and calls a callback function when the process is done

        Args:
            process (function): function to be called
            callback (function): function to be called when process is done
        """
        threading.Thread(target=self.run_process, args=(process, callback)).start()


    def run_process(self, process, callback):
        """Runs a process and calls a callback function when the process is done
        
        Args:
            process (function): function to be called
            callback (function): function to be called when process is done
        """
        process()
        self.after(0, callback)


class FamiliarizationPage(ttk.Frame):

    def __init__(self, parent):
        """Page for starting the familiarization process

        Args:
            parent (App): parent application
        """
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()


    def create_widgets(self):
        """Creates the widgets for the page
        """
        self.play_button = ttk.Button(self, 
                                      text="Starte Eingewöhnung", 
                                      command=self.start_familiarization)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)


    def start_familiarization(self):
        """Starts the familiarization process
        """
        self.parent.show_frame(DuringFamiliarizationView)
        self.parent.wait_for_process(self.parent.frames[DuringFamiliarizationView].program, self.end_familiarization)

    def end_familiarization(self):
        """Ends the familiarization process and shows the next page
        """
        self.parent.show_frame(StandardProgramPage) 


class StandardProgramPage(ttk.Frame):

    def __init__(self, parent):
        """Page for starting the main program

        Args:
            parent (App): parent application
        """
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()


    def create_widgets(self):
        """Creates the widgets for the page
        """
        self.start_button = ttk.Button(self, 
                                       text="Starte Prozess",
                                       command=self.start_program)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)


    def start_program(self):
        """Starts the familiarization process
        """
        self.parent.show_frame(DuringProcedureView)
        self.parent.wait_for_process(self.parent.frames[DuringProcedureView].program, self.end_program)


    def end_program(self):
        """Ends the familiarization process and shows the next page
        """
        self.parent.show_frame(ResultPage) 


class DuringFamiliarizationView(ttk.Frame):

    def __init__(self, parent, familiarization_func):
        """View during familiarization process
        
        Args:
            parent (App): parent application
            familiarization_func (function): function to be called for familiarization"""
        super().__init__(parent)
        self.parent = parent
        self.program = familiarization_func #Hinweis: hier läuft gerade die Dummy Eingewöhnung
        self.text = "Eingewöhnung läuft..."
        self.create_widgets()


    def create_widgets(self):
        """Creates the widgets for the view
        """
        self.info = ttk.Label(self, text=self.text)
        self.info.grid(row=0, column=0, padx=10, pady=10)


class DuringProcedureView(ttk.Frame):

    def __init__(self, parent, program_func, text):
        """View during main program

        Args:
            parent (App): parent application
            program_func (function): function to be called for the main program
            text (str): text to be displayed
        """
        super().__init__(parent)
        self.parent = parent
        self.program = program_func #Hinweis: hier läuft gerade die Dummy Procedure
        self.text = text
        self.create_widgets()


    def create_widgets(self):
        """Creates the widgets for the view
        """
        self.info = ttk.Label(self, text=self.text)
        self.info.grid(row=0, column=0, padx=10, pady=10)


class ResultPage(ttk.Frame):
    # TODO find usefull method to store results earlier on

    def __init__(self, parent):
        """Page for showing the results of the program

        Args:
            parent (App): parent application"""
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()


    def create_widgets(self):
        """Creates the widgets for the view
        """
        self.info = ttk.Label(self, text=self.parent.results)
        self.info.grid(row=0, column=0, padx=10, pady=10)

    # TODO show plot of results



def setup_ui(startfunc, *programfuncs):
    app = App(startfunc, *programfuncs)
    return app

