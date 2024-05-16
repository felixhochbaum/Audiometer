import tkinter as tk
from .ui import setup_ui

def run_app():
    root = tk.Tk()
    root.title("Sound Player")
    app = setup_ui(root)
    app.mainloop()
