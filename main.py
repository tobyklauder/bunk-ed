# Written by Toby Klauder (Lil Dip) - 2023. 
# If anybody is reading this and has questions, call 206-696-1071

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font

# Custom Toggle Switch Design 10-40 

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


# normal matching algorithm 
def assign_cabins(sorted_campers_df, age_range=2, output_file='cabin_pairings.csv'):
    cabins = {}
    cabin_counter = 1
    processed_campers = set()

    # Group campers by gender
    grouped_campers = sorted_campers_df.groupby(['Gender'])

    for group, group_df in grouped_campers:
        gender = group
        group_df.reset_index(drop=True, inplace=True)

        for index, camper in group_df.iterrows():
            if camper['Name'] in processed_campers:
                continue

            current_cabin = [camper]
            processed_campers.add(camper['Name'])

            if camper['Buddy']:
                buddy = group_df.loc[(group_df['Name'] == camper['Buddy'])]
                if not buddy.empty and len(current_cabin) < 11:
                    current_cabin.append(buddy.iloc[0])
                    processed_campers.add(buddy.iloc[0]['Name'])

            while len(current_cabin) < 12:
                remaining_campers = group_df.loc[~group_df['Name'].isin(processed_campers)]
                if not remaining_campers.empty:
                    next_camper = remaining_campers.iloc[0]
                    age_diff = abs(camper['Age'] - next_camper['Age'])

                    if age_diff <= age_range:
                        current_cabin.append(next_camper)
                        processed_campers.add(next_camper['Name'])
                    else:
                        break
                else:
                    break

            cabins[cabin_counter] = current_cabin
            cabin_counter += 1

    # Write cabin pairings to a file
    with open(output_file, 'w') as f:
        for cabin_number, cabin in cabins.items():
            f.write(f"Cabin {cabin_number}:\n")
            for camper in cabin:
                f.write(f"{camper['Name']}\n")
            f.write("\n\n")

    return cabins




#aggressive matching algorithm (pairs based on school within normal constraints)
def assign_cabins_aggressive(sorted_campers_df, age_range=2, output_file='cabin_pairings.csv'):
    cabins = {}
    cabin_counter = 1
    processed_campers = set()

    # Group campers by gender
    grouped_campers = sorted_campers_df.groupby(['Gender'])

    for group, group_df in grouped_campers:
        gender = group
        group_df.reset_index(drop=True, inplace=True)

        for index, camper in group_df.iterrows():
            if camper['Name'] in processed_campers:
                continue

            current_cabin = [camper]
            processed_campers.add(camper['Name'])

            if camper['Buddy']:
                buddy = group_df.loc[(group_df['Name'] == camper['Buddy'])]
                if not buddy.empty and len(current_cabin) < 11:
                    current_cabin.append(buddy.iloc[0])
                    processed_campers.add(buddy.iloc[0]['Name'])

            # Find schoolmates within age range
            schoolmates = group_df.loc[
                (group_df['School'] == camper['School']) &
                (group_df['Gender'] == camper['Gender']) &
                (~group_df['Name'].isin(processed_campers)) &
                (group_df['Age'] <= camper['Age'] + age_range) &
                (group_df['Age'] >= camper['Age'] - age_range)]

            if not schoolmates.empty and len(current_cabin) + len(schoolmates) <= 12:
                current_cabin.extend(schoolmates.to_dict('Records'))
                processed_campers.update(schoolmates['Name'])

            while len(current_cabin) < 12:
                remaining_campers = group_df.loc[
                    ~group_df['Name'].isin(processed_campers) &
                    (group_df['Age'] <= camper['Age'] + age_range) &
                    (group_df['Age'] >= camper['Age'] - age_range)]

                if not remaining_campers.empty:
                    next_camper = remaining_campers.iloc[0]
                    current_cabin.append(next_camper)
                    processed_campers.add(next_camper['Name'])
                else:
                    break

            cabins[cabin_counter] = current_cabin
            cabin_counter += 1

    # Write cabin pairings to a file
    with open(output_file, 'w') as f:
        for cabin_number, cabin in cabins.items():
            f.write(f"Cabin {cabin_number}:\n")
            for camper in cabin:
                f.write(f"{camper['Name']}\n")
            f.write("\n\n")

    return cabins



def open_file_dialog():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        campers_df = pd.read_csv(file_path)
        sorted_campers_df = campers_df.sort_values(by=['Gender', 'Grade'])
        if tight_coupling(): 
            cabins = assign_cabins_aggressive(sorted_campers_df)
        else: 
            cabins = assign_cabins(sorted_campers_df)



def tight_coupling():
    return tight_coupling_var.get()

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
tight_coupling_toggle = CustomToggle(frame, variable=tight_coupling_var, command=tight_coupling)
tight_coupling_toggle.pack(pady=5)



#open file dialog to collect the .csv camper file 
attach_button = ttk.Button(frame, text="Attach File", style="Custom.TButton", command=open_file_dialog)
attach_button.pack(pady=5, anchor="center")

root.mainloop()


