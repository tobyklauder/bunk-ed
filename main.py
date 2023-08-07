# Written by Toby Klauder (Lil Dip) - 2023. 
# If anybody is reading this and has questions, call 206-696-1071
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

MIN_CABIN_SIZE = 8
MAX_CABIN_SIZE = 10

def debug_verify_all_campers_assigned(sorted_campers_df, cabins):
    unassigned_campers = []

    # Checking if all the campers are assigned to a cabin
    for _, row in sorted_campers_df.iterrows():
        camper_found = False
        for gender in ['Male', 'Female']:
            for cabin in cabins[gender]:
                if row['Full Name'] in cabin:
                    camper_found = True
                    break
            if camper_found:
                break

        if not camper_found:
            unassigned_campers.append(row['Full Name'])

    if unassigned_campers:
        # Create a dictionary to group cabins by grade and gender
        grouped_cabins = {}
        for gender in ['Male', 'Female']:
            for grade in sorted_campers_df['2023 > Grade'].unique():
                grouped_cabins[(gender, grade)] = []
                for cabin in cabins[gender]:
                    for camper in cabin:
                        assigned_camper_info = sorted_campers_df.loc[sorted_campers_df['Full Name'] == camper]
                        if assigned_camper_info['2023 > Grade'].item() == grade:
                            grouped_cabins[(gender, grade)].append(cabin)
                            break

        # Iterate through the unassigned campers and assign them to the appropriate cabin
        for camper in unassigned_campers.copy():
            unassigned_camper_info = sorted_campers_df.loc[sorted_campers_df['Full Name'] == camper]
            grade = unassigned_camper_info['2023 > Grade'].item()
            gender = unassigned_camper_info['Gender'].item()

            # Append the camper to the appropriate cabin
            appropriate_cabins = grouped_cabins.get((gender, grade), [])
            if appropriate_cabins:
                appropriate_cabins[0].append(camper)
                unassigned_campers.remove(camper)
   
        print(unassigned_campers)

    else:
        print("All campers have been assigned to a cabin.")

    return unassigned_campers



def create_buddy_groups(sorted_campers_df, buddy_columns):
    """Create buddy groups based on mutual buddy preferences."""
    
    # Create buddy groups
    buddy_groups = []

    for _, row in sorted_campers_df.iterrows():
        for column in buddy_columns:
            buddy_value = row[column]
            if pd.isna(buddy_value):  # Skip if no buddy
                continue

            buddy_rows = sorted_campers_df[sorted_campers_df['Full Name'] == buddy_value]
            if buddy_rows.empty:  # Skip if buddy not found
                continue

            buddy_row = buddy_rows.iloc[0]
            if buddy_row['Gender'] != row['Gender']:  # Skip if different gender
                continue

            curr_grade = int(row['2023 > Grade'][:-2])
            buddy_grade = int(buddy_row['2023 > Grade'][:-2])
            grade_diff = abs(buddy_grade - curr_grade)
            if grade_diff > 1:  # Skip if grade difference is too large
                continue

            # Find or create a group for current camper and buddy
            curr_name = row['Full Name']
            buddy_group = next((group for group in buddy_groups if curr_name in group), None)
            if buddy_group is None:
                buddy_group = set()
                buddy_groups.append(buddy_group)
            buddy_group.update([curr_name, buddy_value])

    for buddy_group in buddy_groups: 
        print(buddy_group)

    return buddy_groups

def merge_intersecting_groups(buddy_groups):
    """Merge intersecting buddy groups into one."""
    # Merge intersecting groups
    i = 0
    while i < len(buddy_groups):
        j = i + 1
        while j < len(buddy_groups):
            if not buddy_groups[i].isdisjoint(buddy_groups[j]):
                buddy_groups[i].update(buddy_groups[j])
                del buddy_groups[j]
            else:
                j += 1
        i += 1

    return buddy_groups 

def assign_groups_to_cabins(buddy_groups, sorted_campers_df, max_cabin_size):
    """Assign buddy groups to cabins, splitting large groups if necessary."""
    # Copy cabins to avoid in-place modifications
    cabins = {'Male': [], 'Female': []}
    for group in buddy_groups:
        group_list = list(group)
        group_gender = sorted_campers_df[sorted_campers_df['Full Name'] == group_list[0]]['Gender'].values[0]
        while len(group_list) > 0:
            cabin_size = min(len(group_list), max_cabin_size)
            cabin = group_list[:cabin_size]
            cabins[group_gender].append(cabin)
            group_list = group_list[cabin_size:]

    return cabins

def verify_cabin_grade_restriction(cabin, sorted_campers_df):
    cabin_grades = [int(sorted_campers_df[sorted_campers_df['Full Name'] == camper]['2023 > Grade'].values[0][:-2]) for camper in cabin]
    min_grade = min(cabin_grades)
    max_grade = max(cabin_grades)
    if max_grade - min_grade > 1:
        return False
    return True


def write_cabin_assignments_to_file(cabins, sorted_campers_df, output_path):
    """Write cabin assignments to a text file."""

    # Create the 'Documents/Bunked' directory if it doesn't exist
    bunked_dir = os.path.join(os.path.expanduser("~"), "Documents/Bunked")
    if not os.path.exists(bunked_dir):
        os.makedirs(bunked_dir)

    # Create the output file path
    output_file = os.path.join(bunked_dir, output_path)

    # Write cabin assignments to output file
    try:
        with open(output_file, 'w') as f:
            # Iterate over the cabins in an alternating gender manner
            for i in range(max(len(cabins['Male']), len(cabins['Female']))):
                for gender in ['Male', 'Female']:
                    if i < len(cabins[gender]):
                        cabin = cabins[gender][i]
                        f.write(f"{gender} Cabin {2*i + 1 + (gender == 'Female')}:\n")
                        for camper in cabin:
                            # Fetch camper's grade from the DataFrame
                            camper_grade = sorted_campers_df.loc[sorted_campers_df['Full Name'] == camper, '2023 > Grade'].values[0]
                            f.write(f"{camper}, Grade: {camper_grade}\n")
                        f.write("\n")

        print("Cabin assignments have been written to an output file.")
    except Exception as e:
        print("An error occurred while writing to the file:", str(e))




def assign_cabins(sorted_campers_df, output_file='cabin_pairings.txt'):
    sorted_campers_df.reset_index(drop=True, inplace=True)

    output_file = os.path.join(os.path.expanduser("~"), "Documents/Bunked", output_file)

    buddy_columns = [col for col in sorted_campers_df.columns if 'Buddy' in col]

    buddy_groups = create_buddy_groups(sorted_campers_df, buddy_columns)

    buddy_groups = merge_intersecting_groups(buddy_groups)

    cabins = assign_groups_to_cabins(buddy_groups, sorted_campers_df, MAX_CABIN_SIZE)

    cabins = assign_remaining_campers(cabins, sorted_campers_df, MAX_CABIN_SIZE)

    merge_cabins(cabins, MIN_CABIN_SIZE, MAX_CABIN_SIZE, sorted_campers_df)

    cabins = sort_cabins_by_age(cabins, sorted_campers_df)

    # Add this line of code before writing the final output
    unassigned_campers = debug_verify_all_campers_assigned(sorted_campers_df, cabins)

    write_cabin_assignments_to_file(cabins, sorted_campers_df, output_file)


def sort_cabins_by_age(cabins, sorted_campers_df):
    grade_to_num = {
        'K': 0,
        '1st': 1,
        '2nd': 2,
        '3rd': 3,
        '4th': 4,
        '5th': 5,
        '6th': 6,
        '7th': 7,
        '8th': 8,
        '9th': 9,
        '10th': 10,
        '11th': 11,
        '12th': 12
    }

    sorted_campers_df['Numeric Grade'] = sorted_campers_df['2023 > Grade'].map(grade_to_num)

    for gender in ['Male', 'Female']:
        cabins_with_avg_grade = []
        for cabin in cabins[gender]:
            avg_grade = sorted_campers_df[sorted_campers_df['Full Name'].isin(cabin)]['Numeric Grade'].mean()
            cabins_with_avg_grade.append((avg_grade, cabin))
        # Sort cabins by average grade
        cabins[gender] = [cabin for _, cabin in sorted(cabins_with_avg_grade)]

    return cabins


def merge_cabins(cabins, min_cabin_size, max_cabin_size, sorted_campers_df):
    max_cabin_count = 30

    for gender in ['Male', 'Female']:
        sorted_cabins = sorted(cabins[gender], key=len)
        i = 0
        while i < len(sorted_cabins):
            if len(sorted_cabins[i]) >= min_cabin_size:
                i += 1
                continue

            # Try to merge with any other cabin
            for j in range(len(sorted_cabins)):
                if i != j and len(sorted_cabins[i]) + len(sorted_cabins[j]) <= max_cabin_size:
                    temp_cabin = sorted_cabins[i] + sorted_cabins[j]
                    if verify_cabin_grade_restriction(temp_cabin, sorted_campers_df):
                        sorted_cabins[i] = temp_cabin
                        del sorted_cabins[j]
                        if j < i:
                            i -= 1  # Recheck with merged cabin
                        break
            else:
                # If the cabin is too small and cannot be merged, remove it
                del sorted_cabins[i]
            
            if len(sorted_cabins) > max_cabin_count:
                print(f"Maximum cabin limit reached for {gender}.")
                sorted_cabins = sorted_cabins[:max_cabin_count]
                break

        cabins[gender] = sorted_cabins


def assign_remaining_campers(cabins, sorted_campers_df, max_cabin_size):
    max_cabin_count = 30

    for _, row in sorted_campers_df.iterrows():
        if any(row['Full Name'] in cabin for cabin in cabins[row['Gender']]):
            continue
        curr_grade = int(row['2023 > Grade'][:-2])
        # Try to fill up existing cabins to their maximum size first
        for cabin in sorted(cabins[row['Gender']], key=len, reverse=True):
            if len(cabin) < max_cabin_size:
                cabin_grades = [int(sorted_campers_df[sorted_campers_df['Full Name'] == camper]['2023 > Grade'].values[0][:-2]) for camper in cabin]
                cabin.append(row['Full Name'])
                # Verify grade restriction after adding the camper
                if not verify_cabin_grade_restriction(cabin, sorted_campers_df):
                    cabin.remove(row['Full Name'])
                else:
                    break
        else:
            # If no existing cabin can accommodate the camper, open a new one if limit is not reached
            if len(cabins[row['Gender']]) < max_cabin_count:
                cabins[row['Gender']].append([row['Full Name']])
            else:
                print(f"Maximum cabin limit reached for {row['Gender']}. Cannot assign camper {row['Full Name']}.")

    # Check the cabin count and reduce if necessary
    for gender in ['Male', 'Female']:
        if len(cabins[gender]) > max_cabin_count:
            print(f"Maximum cabin limit reached for {gender}. Reducing cabin count.")
            cabins[gender] = cabins[gender][:max_cabin_count]

    return cabins






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




