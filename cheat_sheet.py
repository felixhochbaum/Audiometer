import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

# Zum Herumprobieren was verschiedene Themes und Buttons machen :)

#pip install git+https://github.com/RedFantom/ttkthemes


def on_button_click():
    """Callback-Funktion, die ausgeführt wird, wenn der Button geklickt wird."""
    label_var.set("Button was clicked!")

def on_checkbutton_toggle():
    """Callback-Funktion, die ausgeführt wird, wenn das Checkbutton angeklickt wird."""
    if check_var.get() == 1:
        label_var.set("Checkbutton is checked")
    else:
        label_var.set("Checkbutton is unchecked")

def on_radiobutton_select():
    """Callback-Funktion, die ausgeführt wird, wenn ein Radiobutton ausgewählt wird."""
    label_var.set(f"Radiobutton {radio_var.get()} selected")

def on_listbox_select(event):
    """Callback-Funktion, die ausgeführt wird, wenn ein Element in der Listbox ausgewählt wird."""
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(i) for i in selected_indices]
    label_var.set(f"Selected: {', '.join(selected_items)}")

# Hauptfenster erstellen
app = ThemedTk(theme="arc")
app.title("Enhanced Tkinter Example")
app.geometry("400x400")

# Frame erstellen
frame = ttk.Frame(app)
frame.pack(fill=tk.BOTH, expand=True)

# Label mit Variable
label_var = tk.StringVar()
label_var.set("Hello, Tkinter!")
label = ttk.Label(frame, textvariable=label_var)
label.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

# Entry
entry = ttk.Entry(frame)
entry.grid(row=1, column=0, pady=5, sticky="ew")

# Button
button = ttk.Button(frame, text="Click Me", command=on_button_click)
button.grid(row=1, column=1, pady=5, sticky="ew")

# Checkbutton
check_var = tk.IntVar()
checkbutton = ttk.Checkbutton(frame, text="Check me", variable=check_var, command=on_checkbutton_toggle)
checkbutton.grid(row=2, column=0, pady=5, sticky="w")

# Radiobuttons
radio_var = tk.StringVar()
radiobutton1 = ttk.Radiobutton(frame, text="Option 1", variable=radio_var, value="1", command=on_radiobutton_select)
radiobutton2 = ttk.Radiobutton(frame, text="Option 2", variable=radio_var, value="2", command=on_radiobutton_select)
radiobutton1.grid(row=3, column=0, pady=5, sticky="w")
radiobutton2.grid(row=3, column=1, pady=5, sticky="w")

# Listbox
listbox = tk.Listbox(frame, selectmode=tk.SINGLE)
listbox.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
for item in ["Item 1", "Item 2", "Item 3", "Item 4"]:
    listbox.insert(tk.END, item)
listbox.bind('<<ListboxSelect>>', on_listbox_select)


for i in range(2):
    frame.columnconfigure(i, weight=1)
frame.rowconfigure(4, weight=1)

app.mainloop()
