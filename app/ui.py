import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkinter import messagebox

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

        # Store results -> TODO: needs to be changed
        self.results = "Hier sollten später Ergebnisse angezeigt werden"
        
        # Dictionary to store all pages
        self.frames = {}

        # Pages, where the user can interact
        for F in (MainMenu, FamiliarizationPage, StandardProgramPage, ResultPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # View during familiarization
        frame = DuringFamiliarizationView(self, familiarization_func)
        self.frames[DuringFamiliarizationView] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # Views during program(s)
        for i, program_func in enumerate(program_funcs):
            frame = DuringProcedureView(self, program_func, text="Programm {} läuft...".format(i+1)) #TODO change this to useful information, this is just for testing purposes
            self.frames[DuringProcedureView] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show MainMenu first
        self.show_frame(MainMenu)

        # Create menubar
        self.create_menubar()

    def create_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Startseite", command=lambda: self.show_frame(MainMenu))
        file_menu.add_command(label="Button1")  # , command=)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)  # this button closes the app after asking
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Super Exit", command=self.destroy)  # this closes the app without asking. Just for the prototype
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Button1")  # , command=)
        edit_menu.add_command(label="Button2")  # , command=)
        menubar.add_cascade(label="Edit", menu=edit_menu)

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

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Möchten Sie wirklich das Programm beenden?"):
            self.destroy()

class MainMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Startseite", font=('Arial', 16))
        self.label.grid(row=0, column=0, pady=10)

        self.classic_button = ttk.Button(self, text="Klassisches Audiogramm", command=self.start)
        self.classic_button.grid(row=2, column=0, pady=10)

        self.button2 = ttk.Button(self, text="Hörschwellentest")
        self.button2.grid(row=3, column=0, pady=10)

        self.button3 = ttk.Button(self, text="Bileterale Testung")
        self.button3.grid(row=4, column=0, pady=10)

        self.button4 = ttk.Button(self, text="Custom")
        self.button4.grid(row=5, column=0, pady=10)

        self.button5 = ttk.Button(self, text="Exit", command=self.on_click_exit)
        self.button5.grid(row=6, column=0, pady=10)

        # Center the frame's content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_click_exit(self):
        self.parent.on_closing()

    def start(self):
        self.parent.show_frame(FamiliarizationPage)

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
        self.play_button = ttk.Button(self, text="Starte Eingewöhnung", command=self.start_familiarization)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)

        self.GoBack_button = ttk.Button(self, text="zurück", command=self.GoBack)
        self.GoBack_button.grid(row=2, column=5, padx=10, pady=10)
    

    def start_familiarization(self):
        """Starts the familiarization process
        """
        self.parent.show_frame(DuringFamiliarizationView)
        self.parent.wait_for_process(self.parent.frames[DuringFamiliarizationView].program, self.end_familiarization)

    def end_familiarization(self):
        """Ends the familiarization process and shows the next page
        """
        self.parent.show_frame(StandardProgramPage)

    def GoBack(self):
        self.parent.show_frame(MainMenu)

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
        self.start_button = ttk.Button(self, text="Starte Prozess", command=self.start_program)
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
        self.program = familiarization_func  # Hinweis: hier läuft gerade die Dummy Eingewöhnung
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
        self.program = program_func  # Hinweis: hier läuft gerade die Dummy Procedure
        self.text = text
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the view
        """
        self.info = ttk.Label(self, text=self.text)
        self.info.grid(row=0, column=0, padx=10, pady=10)

class ResultPage(ttk.Frame):
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
        self.BackToMainMenu = ttk.Button(self, text="Zurück zur Startseite", command=self.Back_To_MainMenu)
        self.BackToMainMenu.grid(row=10, column=0, padx=10, pady=10)
    
    def Back_To_MainMenu(self):
        self.parent.show_frame(MainMenu)

def setup_ui(startfunc, *programfuncs):
    app = App(startfunc, *programfuncs)
    return app