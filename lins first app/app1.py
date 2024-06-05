import tkinter as tk

class AudiometerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audiometer")
        
        self.geometry(f"{566}x{566}")

        self.create_widgets()
    

    def create_widgets(self):
        # Configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Label erstellen
        label = tk.Label(self, text="Willkommen zum Audiometer. Bitte wählen Sie eines der folgenden Programme:", font=("Arial", 16))
        label.grid(row=0, column=0, pady=20)

        button1 = tk.Button(self, text="klassisches Audiometer")
        button1.grid(row=1, column=0, pady=10)

        # Button 2
        button2 = tk.Button(self, text="Hoerschwellentest")
        button2.grid(row=2, column=0, pady=10)

        # Button 3
        button3 = tk.Button(self, text="bilaterale Testung")
        button3.grid(row=3, column=0, pady=10)

        # Button 4
        button4 = tk.Button(self, text="costum")
        button4.grid(row=4, column=0, pady=10)

if __name__ == "__main__":
    app = AudiometerApp()
    app.mainloop()
