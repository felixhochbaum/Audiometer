import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkinter import messagebox
from .audiogram import create_audiogram #TODO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.instructions import text_Familiarization
import ttkbootstrap as tb

class App(tb.Window):
    def __init__(self, familiarization_func, program_funcs:dict):
        """Main application window. Contains all pages and controls the flow of the program.

        Args:
            familiarization_func (function): function to be called for familiarization
            *program_funcs (function): function(s) to be called for the main program
        """
        super().__init__(themename="superhero")  # Set/change the theme Link: https://ttkbootstrap.readthedocs.io/en/latest/themes/dark/

        self.program_funcs = program_funcs

        # General settings
        self.title("Sound Player")
        self.geometry("1000x800")
        # self.iconbitmap("path..")

        # Store results -> TODO: needs to be changed
        self.results = "Hier sollten später Ergebnisse angezeigt werden"

        # Dictionary to store all pages
        self.frames = {}

        # Pages, where the user can interact
        for F in (MainMenu, FamiliarizationPage, ProgramPage, ResultPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # View during familiarization
        frame = DuringFamiliarizationView(self, familiarization_func)
        self.frames[DuringFamiliarizationView] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        # View during programs
        for program_func in program_funcs.values():
            frame = DuringProcedureView(self, 
                                        program_func,
                                        text="Programm läuft...")
            self.frames[DuringProcedureView] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show MainMenu first
        self.show_frame(MainMenu)

        # Create menubar
        self.create_menubar()

        # Override the close button protocol (instead of extra button)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Startseite", command=lambda: self.show_frame(MainMenu))
        file_menu.add_command(label="Button1")  # , command=)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)

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
        self.button_width = 25
        self.start_button = None
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="\nBitte wählen Sie ein Programm", font=('Arial', 16))
        self.label.pack(pady=10)

        # Dropdown menu
        options = list(self.parent.program_funcs.keys())
        self.dropdown = ttk.Combobox(self, values=options, state="readonly", width=self.button_width-1)
        self.dropdown.set("Test wählen...")
        self.dropdown.pack(pady=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.on_option_selected)

        # Moved that to normal closing button
        # self.exit_button = ttk.Button(self, text="Exit", command=self.parent.on_closing,
        #                               width=self.button_width)
        # self.exit_button.pack(pady=10)

        for widget in self.winfo_children():
            widget.pack_configure(anchor='center')
    
    def on_option_selected(self, event):
        self.show_start_button()

    def show_start_button(self):
        if self.start_button is None:
            self.start_button = ttk.Button(self, 
                                           text="Test starten", 
                                           command=lambda: self.parent.show_frame(FamiliarizationPage), 
                                           width=self.button_width)
            self.start_button.pack(pady=10)


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
        button_width = 25 
       
        self.label = ttk.Label(self, text=text_Familiarization, font=('Arial', 16))
        self.label.pack(padx=10, pady=10)
        self.play_button = ttk.Button(self, 
                                      text="Starte Eingewöhnung", 
                                      command=self.run_familiarization, 
                                      width=button_width)
        self.play_button.pack(padx=10, pady=10)
        self.go_back_button = ttk.Button(self, 
                                         text="zurück", 
                                         command=lambda: self.parent.show_frame(MainMenu), 
                                         width=button_width)
        self.go_back_button.pack(padx=10, pady=10)

        for widget in self.winfo_children():
            widget.pack_configure(anchor='center')

    def run_familiarization(self):
        """Runs the familiarization process
        """
        self.parent.show_frame(DuringFamiliarizationView)
        self.parent.wait_for_process(self.parent.frames[DuringFamiliarizationView].program, 
                                     lambda: self.parent.show_frame(ProgramPage))

class ProgramPage(ttk.Frame):
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
        self.start_button = ttk.Button(self, text="Starte Prozess", command=self.run_program)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

    def run_program(self):
        """Runs the familiarization process
        """
        self.parent.show_frame(DuringProcedureView)
        self.parent.wait_for_process(self.parent.frames[DuringProcedureView].program, 
                                     lambda: self.parent.show_frame(ResultPage))

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
        
        # Beispielwerte
        #freq = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
        #dummy_right = [10, 15, 20, 25, 30, 35, 40, 45]
        #dummy_left = [5, 10, 15, 20, 25, 30, 35, 40]
        # Audiogramm erstellen
        #create_audiogram(freq, dummy_right, dummy_left)

        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the view
        """
        #self.info = ttk.Label(self, text=self.parent.results)
        #self.info.grid(row=0, column=0, padx=10, pady=10)

        self.info = ttk.Label(self, text="Ergebnisse", font=('Arial',18))
        self.info.grid(row=0, column=0, padx=10, pady=10)

        self.BackToMainMenu = ttk.Button(self, text="Zurück zur Startseite", command=self.back_to_MainMenu)
        self.BackToMainMenu.grid(row=11, column=0, padx=10, pady=10)

        # self.SaveResults = ttk.Button(self, text="Ergebnisse speichern", command=self.show_warning)
        # self.SaveResults.grid(row=10, column=0, padx=10, pady=10) #Ergebnisse sollen eh automatisch gespeichert werden

        # dummy values
        freq = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
        dummy_right = [10, 15, 20, 25, 30, 35, 40, 45]
        dummy_left = [5, 10, 15, 20, 25, 30, 35, 40]

        # audiogram plot
        fig = create_audiogram(freq, dummy_right, dummy_left)
        
        # Embed the plot in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)
   
    def show_warning(self):
            messagebox.showwarning("Warnung", "Funktioniert noch nicht :)")
    
    def back_to_MainMenu(self):
        self.parent.show_frame(MainMenu)

def setup_ui(startfunc, *programfuncs):
    app = App(startfunc, *programfuncs)
    return app