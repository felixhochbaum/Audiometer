import tkinter as tk
from .audio_player import AudioPlayer

# https://www.youtube.com/watch?v=eaxPK9VIkFM


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sound Player")
        #self.geometry(f"{size[0]}x{size[1]}")
        self.geometry("400x200")
        self.menu = Menu(self)
        self.menu.pack()

class Menu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.audio_player = AudioPlayer()
        self.create_widgets()

    def create_widgets(self):
        self.play_button = tk.Button(self, text="Click me :)", command=self.audio_player.start_beep)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Make it stop!", command=self.audio_player.stop_beep)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)


def setup_ui():
    app = App()
    return app
