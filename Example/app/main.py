from .ui import setup_ui

def run_app():
    app = setup_ui()
    app.mainloop()
