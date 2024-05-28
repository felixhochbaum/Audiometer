from .ui import setup_ui
from .ui_alternative import setup_ui_alternative

def run_app():
    app = setup_ui()
    #app = setup_ui_alternative()
    app.mainloop()
