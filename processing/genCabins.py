# Author: Toby Klauder

from objects.cabin import Cabin
import tkinter as tk
from tkinter import ttk
from objects.camper import Camper 
import sys 
from tkinter import filedialog

def get_unassigned_campers(camper_lookup):
    """Get a list of campers that haven't been assigned to a buddy group.

    Args:
        camper_lookup (dict): A dictionary of campers, keyed by name.

    Returns:
        list: A list of unassigned camper objects.
    """
    return list(camper_lookup.values())

def get_camper_by_name(name, df):
    # Create a camper object from the DataFrame row
    camper_data = df[df['Full Name'] == name].iloc[0]
    camper = Camper(camper_data['Full Name'], camper_data['Age'], camper_data['Current grade'], camper_data['Gender'])  # Assuming Camper class
    return camper

def assign_cabins(buddy_groups, campers_df, max_cabin_size):
    cabins = [Cabin() for _ in range(30)]

    def flatten(list): 
        flat_list = []
        for group in list: 
            flat_list.extend(group.get_members())
        return flat_list 
    
    # List of assigned campers from buddy groups
    assigned_campers = [camper.get_name() for camper in flatten(buddy_groups)]

    # List of all campers from the DataFrame
    all_campers = list(campers_df['Full Name'])

    # List of unassigned campers
    unassigned_campers = [camper for camper in all_campers if camper not in assigned_campers]

    # Assign buddy groups to cabins
    for group in buddy_groups:
        for camper in group.get_members():
            for cabin in cabins:
                if cabin.add_camper(camper, max_cabin_size) == 1:
                    break

    # Assign unassigned campers to cabins
    for camper_name in unassigned_campers:
        camper = get_camper_by_name(camper_name, campers_df)  # Assuming you have a function to get camper object by name
        for cabin in cabins:
            if cabin.add_camper(camper, max_cabin_size) == 1:
                break

    girl_cabins = [cabin for cabin in cabins if cabin.get_cabin_gender() == "Female"]
    guy_cabins = [cabin for cabin in cabins if cabin.get_cabin_gender() == "Male"]
    girl_cabins.sort(key=lambda cabin: cabin.get_average_grade())
    guy_cabins.sort(key=lambda cabin: cabin.get_average_grade())

    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user where they want to save the file
    file_path = filedialog.asksaveasfilename(
        initialdir="/", 
        title="Select file", 
        defaultextension=".txt",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if not file_path:
        print("File save cancelled.")
        return

    with open(file_path, "w") as file:
        i = 0
        while girl_cabins or guy_cabins:
            if i % 2 == 0 and girl_cabins:
                cabin = girl_cabins.pop(0)
                if cabin.get_campers():
                    file.write(f"Cabin {i + 1}:\n")
                    for camper in cabin.get_campers():
                        file.write(f" - {camper.get_name()}, Grade: {camper.get_grade()}, Gender: {camper.get_gender()}\n")
            elif i % 2 != 0 and guy_cabins:
                cabin = guy_cabins.pop(0)
                if cabin.get_campers():
                    file.write(f"Cabin {i + 1}:\n")
                    for camper in cabin.get_campers():
                        file.write(f" - {camper.get_name()}, Grade: {camper.get_grade()}, Gender: {camper.get_gender()}\n")
            else:
                # If we run out of cabins for one gender, just continue with the other
                if girl_cabins:
                    cabin = girl_cabins.pop(0)
                    if cabin.get_campers():
                        file.write(f"Cabin {i + 1}:\n")
                        for camper in cabin.get_campers():
                            file.write(f" - {camper.get_name()}, Grade: {camper.get_grade()}, Gender: {camper.get_gender()}\n")
                elif guy_cabins:
                    cabin = guy_cabins.pop(0)
                    if cabin.get_campers():
                        file.write(f"Cabin {i + 1}:\n")
                        for camper in cabin.get_campers():
                            file.write(f" - {camper.get_name()}, Grade: {camper.get_grade()}, Gender: {camper.get_gender()}\n")
                else:
                    # If no cabins are left for either gender, break the loop
                    break
            i += 1

    print("Cabins generated successfully.")
    sys.exit() 
