import tkinter as tk
import tkinter.ttk as ttk
import threading
from tkinter import messagebox
from .audiogram import create_audiogram #TODO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.instructions import text_Familiarization
import ttkbootstrap as tb
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime

class App(tb.Window):

    def __init__(self, familiarization_func, audiogram_func, program_funcs:dict):
        """Main application window. Contains all pages and controls the flow of the program.

        Args:
            familiarization_func (function): function to be called for familiarization
            *program_funcs (function): function(s) to be called for the main program
        """
        super().__init__(themename="solar")  # Set/change the theme Link: https://ttkbootstrap.readthedocs.io/en/latest/themes/dark/

        # General theme settings
        self.title("Sound Player")
        self.geometry("800x800")
        self.minsize(650,650)
        self.attributes('-fullscreen', True)  #for fullscreen mode
        self.bind("<Escape>", self.exit_fullscreen)
        self.audiogram_func = audiogram_func

        #self.set_icon("app/00_TUBerlin_Logo_rot.jpg") change the icon maybe? #TODO
        
        #this might solve the different GUI on macOS LINUX and WINDOWS problem... #TODO
        self.tk.call('tk', 'scaling', 2.0)  # Adjust for high-DPI displays
        
        # Dictionary to store all pages
        self.program_funcs = program_funcs
        self.frames = {}
        self.binaural_test = False

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
        for name, program_func in program_funcs.items():
            frame = DuringProcedureView(self, 
                                        program_func,
                                        text="Programm läuft...")
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show MainMenu first
        self.show_frame(MainMenu)

        # Create menubar
        self.create_menubar()

        # Override the close button protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Startseite", command=lambda: self.show_frame(MainMenu))

        # Settings for chaning the theme Link: lighthttps://ttkbootstrap.readthedocs.io/en/latest/themes/dark/
        ChangeTheme = tk.Menu(file_menu, tearoff=0)
        
        ChangeTheme.add_command(label="light", command=lambda: self.change_theme("sandstone"))
        ChangeTheme.add_command(label="dark", command=lambda: self.change_theme("solar"))
        file_menu.add_cascade(label="change theme", menu=ChangeTheme)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)

    def change_theme(self, theme_name):
        """Change to the specified theme"""
        current_theme = self.style.theme_use()

        if current_theme == theme_name:
            messagebox.showwarning("Ops..", "Dieses Theme wird bereits verwendet.")
        else:
            self.style.theme_use(theme_name)

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

    def set_icon(self, path):
        """Set the window icon using Pillow"""
        img = Image.open(path)
        photo = ImageTk.PhotoImage(img)
        self.iconphoto(False, photo)          

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
        self.binaural_test = tk.BooleanVar()
        self.use_calibration = tk.BooleanVar(value=True)
        self.selected_option = None
        self.patient_number = ""
        self.create_widgets()

    def create_widgets(self):

        self.patient_number_label = ttk.Label(self, text="Probandennummer:",font=('Arial', 12))
        self.patient_number_label.pack(padx=10, pady=10)
        self.patient_number_entry = ttk.Entry(self,width=self.button_width+1)
        self.patient_number_entry.pack(padx=10, pady=10)

        self.gender_label = ttk.Label(self, text="Geschlecht (Optional):", font=('Arial', 12))
        self.gender_label.pack(padx=10, pady=10)
        self.gender_dropdown = ttk.Combobox(self, values=["Männlich", "Weiblich", "Divers", "Keine Angabe"], state="readonly", width=self.button_width - 1)
        self.gender_dropdown.set("Geschlecht...")
        self.gender_dropdown.pack(padx=10, pady=10)
        ''' # doesn't work yet
        self.birthday_label = ttk.Label(self, text="Geburstag (Optional):", font=('Arial', 12))
        self.birthday_label.pack(padx=10, pady=10)
        self.birthday_entry = DateEntry(self, date_pattern='dd.mm.yyyy', width=24, background='darkblue',
                                        foreground='white', borderwidth=2, maxdate=datetime.today())
        '''

        self.label = ttk.Label(self, text="\nBitte wählen Sie ein Programm", font=('Arial', 16))
        self.label.pack(pady=10)

        # Dropdown menu
        options = list(self.parent.program_funcs.keys())
        self.dropdown = ttk.Combobox(self, values=options, state="readonly", width=self.button_width - 1)
        self.dropdown.set("Test wählen...")
        self.dropdown.pack(pady=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.on_option_selected)

        #TODO nur wenn sinnvoll anzeigen
        self.bi_button = ttk.Checkbutton(self, 
                                         text="Binaurale Testung", 
                                         variable=self.binaural_test)
        self.bi_button.pack(pady=10)

        self.cal_button = ttk.Checkbutton(self, 
                                         text="Werte aus letzter Kalibrierung verwenden", 
                                         variable=self.use_calibration,)
        self.cal_button.pack(pady=10)

    def on_option_selected(self, event):
        self.selected_option = self.dropdown.get()
        self.show_start_button()

    def show_start_button(self):
        if self.start_button is None:
            self.start_button = ttk.Button(self,
                                           text="Test starten",
                                           command=self.run_familiarization,
                                           width=self.button_width)
            self.start_button.pack(pady=10)

    def run_familiarization(self):
        self.patient_number = self.patient_number_entry.get()
        if not self.patient_number:
            messagebox.showwarning("Warnung", "Bitte geben Sie eine Probandennummer ein.")
            return
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
        self.use_calibration = self.parent.frames[MainMenu].use_calibration.get()
        self.parent.show_frame(DuringFamiliarizationView)
        self.parent.wait_for_process(lambda: self.parent.frames[DuringFamiliarizationView].program(id=self.parent.frames[MainMenu].patient_number, calibrate=self.use_calibration), 
                                     lambda: self.parent.show_frame(ProgramPage))


class ProgramPage(ttk.Frame):

    def __init__(self, parent):
        """Page for starting the main program

        Args:
            parent (App): parent application
        """
        super().__init__(parent)
        self.parent = parent
        self.selected_option = None 
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the page
        """
        self.start_button = ttk.Button(self, text="Starte Prozess", command=self.run_program)
        self.start_button.pack(padx=10, pady=200)
    
        for widget in self.winfo_children():
            widget.pack_configure(anchor='center')

    def run_program(self):
        """Runs the main program
        """
        self.selected_option = self.parent.frames[MainMenu].selected_option
        self.binaural_test = self.parent.frames[MainMenu].binaural_test.get()
        self.use_calibration = self.parent.frames[MainMenu].use_calibration.get()
        self.parent.show_frame(self.selected_option)
        self.parent.wait_for_process(lambda: self.parent.frames[self.selected_option].program(self.binaural_test, calibrate=self.use_calibration),
                                     lambda: self.parent.show_frame(ResultPage))


class DuringFamiliarizationView(ttk.Frame):
    
    def __init__(self, parent, familiarization_func):
        """View during familiarization process
        
        Args:
            parent (App): parent application
            familiarization_func (function): function to be called for familiarization"""
        super().__init__(parent)
        self.parent = parent
        self.program = familiarization_func 
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
        self.program = program_func 
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

        # Create audiogram plot
        fig = self.parent.audiogram_func()
        
        # Create widgets
        self.create_widgets(fig)

    def create_widgets(self,fig):
        """Creates the widgets for the view`
        """
        self.info = ttk.Label(self, text="Ergebnisse", font=('Arial', 18))
        self.info.pack(padx=10, pady=10)

        # Set the title on the parent window
        self.parent.title("Audiogram")

        # Display the plot
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, expand=0)

        self.BackToMainMenu = ttk.Button(self, text="Zurück zur Startseite", command=lambda: self.parent.show_frame(MainMenu))
        self.BackToMainMenu.pack(padx=10, pady=10)
    
    def back_to_MainMenu(self):
        self.parent.show_frame(MainMenu)


def setup_ui(startfunc, endfunc, programfuncs):
    app = App(startfunc, endfunc, programfuncs)
    return app