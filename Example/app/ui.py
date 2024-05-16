import tkinter as tk
from .audio_player import AudioPlayer

# https://www.youtube.com/watch?v=eaxPK9VIkFM


class App(tk.Frame):
    def __init__(self, master=None, title="Sound Player", size=[400, 200]):
        super().__init__(master)
        self.master = master
        self.master.title(title)
        self.master.geometry(f"{size[0]}x{size[1]}")
        self.menu = Menu(self)
        self.pack()

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


def setup_ui(root):
    app = App(master=root)
    return app


if __name__ == "__main__":
    root = tk.Tk()
    setup_ui(root)
    root.mainloop()
