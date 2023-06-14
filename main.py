# Written by Toby Klauder (Lil Dip) - 2023. 
# If anybody is reading this and has questions, call 206-696-1071

import re
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

# Function to check if a substring (search) is present in a string (text) using case-insensitive comparison
def is_substring_in_string(search, text):
    return re.search(search, text, re.IGNORECASE) is not None

def assign_cabins(sorted_campers_df, min_cabin_size=8, max_cabin_size=10, output_file='cabin_pairings.txt'):
    sorted_campers_df.reset_index(drop=True, inplace=True)

    output_path = os.path.join(os.path.expanduser("~"), "Documents/Bunked", output_file)

    buddy_columns = [col for col in sorted_campers_df.columns if 'Buddy' in col]

    buddy_groups = []  # List to store buddy groups

    for row_index, row in sorted_campers_df.iterrows():
        for column in buddy_columns:
            buddy_value = row[column]
            if buddy_value in sorted_campers_df['Full Name'].values:
                buddy_row = sorted_campers_df[sorted_campers_df['Full Name'] == buddy_value].iloc[0]

                if buddy_row['Gender'] == row['Gender']:
                    curr_grade = int(row['2023 > Grade'][:-2])
                    buddy_grade = int(buddy_row['2023 > Grade'][:-2])
                    grade_diff = abs(buddy_grade - curr_grade)
                    if grade_diff == 0 or grade_diff == 1:
                        curr_name = row['Full Name']
                        group_found = False
                        for group in buddy_groups:
                            if curr_name in group or buddy_value in group:
                                group.add(curr_name)
                                group.add(buddy_value)
                                group_found = True
                                break
                        if not group_found:
                            buddy_groups.append(set([curr_name, buddy_value]))

    i = 0
    while i < len(buddy_groups) - 1:
        j = i + 1
        while j < len(buddy_groups):
            if buddy_groups[i].intersection(buddy_groups[j]):
                buddy_groups[i].update(buddy_groups[j])
                del buddy_groups[j]
            else:
                j += 1
        i += 1

    cabins = {'Male': [], 'Female': []}  # Separate cabins by gender
    for group in buddy_groups:
        group_list = list(group)
        group_gender = sorted_campers_df[sorted_campers_df['Full Name'] == group_list[0]]['Gender'].values[0]
        if len(group) <= max_cabin_size:
            cabins[group_gender].append(group_list)
            for camper in group:
                sorted_campers_df = sorted_campers_df[sorted_campers_df['Full Name'] != camper]

    # Assign remaining campers to cabins
    for gender in sorted_campers_df['Gender'].unique():
        for grade in sorted(sorted_campers_df['2023 > Grade'].unique()):
            campers = sorted_campers_df[(sorted_campers_df['Gender'] == gender) & (sorted_campers_df['2023 > Grade'] == grade)]['Full Name'].tolist()
            while len(campers) > 0:
                camper_added = False
                for cabin in cabins[gender]:
                    if len(cabin) < max_cabin_size:
                        cabin.append(campers.pop())
                        camper_added = True
                        break
                if not camper_added:
                    if len(campers) >= max_cabin_size:  # Create a new cabin if there are at least 10 campers remaining
                        cabins[gender].append(campers[:max_cabin_size])
                        campers = campers[max_cabin_size:]
                    else:  # Assign remaining campers to the last cabin, even if it's less than 10
                        cabins[gender][-1].extend(campers)
                        campers = []


    # Merge smaller cabins if they are of the same gender
    for gender in cabins:
        i = 0
        while i < len(cabins[gender]):
            if len(cabins[gender][i]) < min_cabin_size:
                for j in range(i + 1, len(cabins[gender])):
                    if len(cabins[gender][i]) + len(cabins[gender][j]) <= max_cabin_size:
                        cabins[gender][i].extend(cabins[gender][j])
                        cabins[gender].pop(j)
                        break
                else:  # Only increase i if no merge occurred
                    i += 1
            else:  # Cabin size is already ok, move to the next
                i += 1

    # Write the cabin assignments to a text file
    with open(output_path, 'w') as file:
        for gender in cabins:
            for i, cabin in enumerate(cabins[gender], start=1):
                file.write(f"{gender} Cabin {i}:\n")
                for camper in cabin:
                    file.write(f"{camper}\n")
                file.write("\n")  # Add a blank line between cabins

    print("Cabin assignments have been written to the output file.")




#allows the user to open a .csv file for processing 
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        campers_df = pd.read_csv(file_path)
        campers_df['Full Name'] = campers_df['First name'] + ' ' + campers_df['Last name']  # new line to create 'Full Name'
        
        # Create a new column 'SortValue' in the DataFrame where if the 'Age' is less than or equal to 0,
        # it will take the value of '2023 > Grade' otherwise it will take the value of 'Age'
        campers_df['SortValue'] = campers_df['Age'].where(campers_df['Age'] > 0, campers_df['2023 > Grade'])

        # Now sort the DataFrame based on the 'SortValue' and 'Gender' columns
        sorted_campers_df = campers_df.sort_values(by=['Gender', 'SortValue'])

        # Make sure to drop the 'SortValue' column after sorting
        sorted_campers_df.drop('SortValue', axis=1, inplace=True)

        assign_cabins(sorted_campers_df)


window = tk.Tk()
window.title("Bunk'ed")
window.geometry("200x120")

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
header_frame = tk.Frame(window, bg="#023047")
header_frame.pack(side="top", fill="x")
header_label = tk.Label(header_frame, text="Bunk'ed", font=("Comic Sans MS", 25), bg="#023047", fg="white")
header_label.pack(pady=5)

#set baby blue background color for the frame 
frame = ttk.Frame(window, padding="10 10 10 10", style="Custom.TFrame")
style.configure("Custom.TFrame", background="#8ecae6")
frame.pack(expand=True, fill="both")


#open file dialog to collect the .csv camper file 
attach_button = ttk.Button(frame, text="Camper Data", style="Custom.TButton", command=open_file_dialog)
attach_button.pack(pady=5, anchor="center")

window.mainloop()




