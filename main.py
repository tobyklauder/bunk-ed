# Written by Toby Klauder (Lil Dip) - 2023. 
# If anybody is reading this and has questions, call 206-696-1071

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font

class CustomToggle(tk.Canvas):
    def __init__(self, parent, variable, command=None, *args, **kwargs):
        super().__init__(parent, width=50, height=25, *args, **kwargs)
        self.command = command
        self.variable = variable
        self.configure(highlightthickness=0, bd=0, bg="#8ecae6")
        self.bind("<Button-1>", self.toggle)

        self.variable.trace("w", self.update_display)

        self.update_display()

    def toggle(self, event=None):
        self.variable.set(not self.variable.get())
        if self.command:
            self.command()

    def update_display(self, *args):
        self.delete("all")
        radius = 5
        if self.variable.get():
            self.create_polygon(2, radius, 2, 23-radius, 2+radius, 23, 48-radius, 23, 48, 23-radius, 48, radius, 48-radius, 2, 2+radius, 2,
                                smooth=True, outline="#219ebc", width=2, fill="#219ebc")
            self.create_oval(25, 5, 45, 20, fill="white", outline="")
        else:
            self.create_polygon(2, radius, 2, 23-radius, 2+radius, 23, 48-radius, 23, 48, 23-radius, 48, radius, 48-radius, 2, 2+radius, 2,
                                smooth=True, outline="#219ebc", width=2, fill="#8ecae6")
            self.create_oval(5, 5, 25, 20, fill="white", outline="")






def open_file_dialog():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        print("File selected:", file_path)
        # Process the selected file here

def tight_coupling_changed():
    toggle_value = tight_coupling_var.get()
    print("Tight coupling:", toggle_value)

#create the primary window 
root = tk.Tk()
root.title("Bunk'ed")
root.geometry("400x200")

#create the style object
style = ttk.Style()
style.theme_use("default")

#configure custom assets 
style.map("Custom.TButton",
          background=[("active", "#2a9d8f")],
          foreground=[("active", "white")])
style.configure("Custom.TLabel", background="#8ecae6", font=("Comic Sans MS", 14))
style.configure("Custom.TCheckbutton", background="#8ecae6")


# Header frame
header_frame = tk.Frame(root, bg="#023047")
header_frame.pack(side="top", fill="x")
header_label = tk.Label(header_frame, text="Bunk'ed", font=("Comic Sans MS", 25), bg="#023047", fg="white")
header_label.pack(pady=5)

#set baby blue background color for the frame 
frame = ttk.Frame(root, padding="10 10 10 10", style="Custom.TFrame")
style.configure("Custom.TFrame", background="#8ecae6")
frame.pack(expand=True, fill="both")

#toggle for tight coupling, which aggressively searches the .csv file (see docs)
tight_coupling_label = ttk.Label(frame, text="Aggressive Grouping:", style="Custom.TLabel")
tight_coupling_label.pack(pady=10)
tight_coupling_var = tk.BooleanVar()
tight_coupling_toggle = CustomToggle(frame, variable=tight_coupling_var, command=tight_coupling_changed)
tight_coupling_toggle.pack(pady=5)



#open file dialog to collect the .csv camper file 
attach_button = ttk.Button(frame, text="Attach File", style="Custom.TButton", command=open_file_dialog)
attach_button.pack(pady=5, anchor="center")

root.mainloop()


