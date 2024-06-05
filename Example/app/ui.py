import tkinter as tk
import tkinter.ttk as ttk


#Achtung, funktioniert noch nicht, bin noch mittendrin

class App(tk.Tk):
    def __init__(self, startfunc):
        super().__init__()
        self.title("Sound Player")
        self.geometry("400x200")
        self.frames = {}
        self.start = startfunc

        for F in (MenuPage, IntroductionPage, IntroductionDonePage):
            frame = F(self, self.start)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MenuPage)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MenuPage(ttk.Frame):
    def __init__(self, parent, start):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.play_button = tk.Button(self, text="Click me :)", command=self.show_intro)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)

    def show_intro(self):
        self.parent.show_frame(IntroductionPage)



class IntroductionPage(ttk.Frame):
    def __init__(self, parent, start):
        super().__init__(parent)
        self.start = start
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.info = ttk.Label(self, text="Eingewöhnung läuft...")
        self.info.grid(row=0, column=0, padx=10, pady=10)
        self.start(self.proceed)

    def proceed(self):
        self.parent.show_frame(IntroductionDonePage)


class IntroductionDonePage(ttk.Frame):
    def __init__(self, parent, start):
        super().__init__(parent)
        self.start = start
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.play_button = ttk.Button(self, text="Restart Introduction", command=self.show_menu)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)

    def show_menu(self):
        self.parent.show_frame(MenuPage)


def setup_ui(startfunc):
    app = App(startfunc)
    return app

