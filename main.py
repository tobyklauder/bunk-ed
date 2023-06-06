# Written by Toby Klauder (Lil Dip) - 2023. 
# If anybody is reading this and has questions, call 206-696-1071

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

def assign_cabins(sorted_campers_df, min_cabin_size=8, max_cabin_size=12, output_file='cabin_pairings.txt'):
    sorted_campers_df.reset_index(drop=True, inplace=True)
    
    output_path = os.path.join(os.path.expanduser("~"), "Documents", output_file)

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
                    cabins[gender].append([campers.pop()])

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

    # Combine the lists of cabins for each gender, alternating between them
    combined_cabins = [None]*(len(cabins['Male'])+len(cabins['Female']))
    combined_cabins[::2] = cabins['Male']
    combined_cabins[1::2] = cabins['Female']

    # Write the cabin assignments to a text file
    with open(output_path, 'w') as file:
        for i, cabin in enumerate(combined_cabins, start=1):
            if i % 2 == 1:
                file.write(f"Male Cabin {i//2 + 1}:\n")
            else:
                file.write(f"Female Cabin {i//2}:\n")
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

  
        cabins = assign_cabins(sorted_campers_df)



#create the primary window 
root = tk.Tk()
root.title("Bunk'ed")
root.geometry("200x120")

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


#open file dialog to collect the .csv camper file 
attach_button = ttk.Button(frame, text="Attach File", style="Custom.TButton", command=open_file_dialog)
attach_button.pack(pady=5, anchor="center")

root.mainloop()


