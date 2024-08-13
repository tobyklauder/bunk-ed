import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd 

from processing.file_processing import scrape_camper_csv
from processing.genBuddyGroups import gen_buddy_groups
from processing.genBuddyGroups import debug_buddy_groups
from processing.genCabins import assign_cabins, get_unassigned_campers

class BunkedGui:

    def __init__(self, root) -> None:
        """
        Initialize the tkinter window 

        args:
            root: the root of the tkinter window

        returns:
            None
        """
        self.root = root
        self._df = None

        # Set the title for the window 
        self.root.title("Bunk'ed")
        
        # Set the size of the window 
        self.root.geometry("200x180")
        
        self.configure_styles()
        self.create_header()
        self.create_main_frame()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        # configure custom assets
        style.map("Custom.TButton",
                  background=[("active", "#2a9d8f")],
                  foreground=[("active", "white")])
        style.configure("Custom.TLabel", background="#8ecae6", font=("Comic Sans MS", 14))
        style.configure("Custom.TCheckbutton", background="#8ecae6")
        style.configure("Custom.TFrame", background="#8ecae6")

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#023047")
        header_frame.pack(side="top", fill="x")
        header_label = tk.Label(header_frame, text="Bunk'ed", font=("Comic Sans MS", 25), bg="#023047", fg="white")
        header_label.pack(pady=5)

    def create_main_frame(self):
        frame = ttk.Frame(self.root, padding="10 10 10 10", style="Custom.TFrame")
        frame.pack(expand=True, fill="both")

        attach_button = ttk.Button(frame, text="Camper Data", style="Custom.TButton", command=self.get_csv)
        attach_button.pack(pady=5, anchor="center")
        

        label = ttk.Label(frame, text="MAX_CABIN_SIZE", style="Custom.TLabel")
        label.pack(pady=5, anchor="center")


        self.numeric_var = tk.StringVar()
        numeric_entry = ttk.Entry(frame, textvariable=self.numeric_var, style="Custom.TEntry")
        numeric_entry.pack(pady=5, anchor="center")


        validate_numeric = (self.root.register(self.only_numbers), '%P')
        numeric_entry.config(validate="key", validatecommand=validate_numeric)
        

        
    def only_numbers(self, char):
        return char.isdigit() or char == ""

    def get_csv(self): 
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            self._df = pd.read_csv(file_path)
            self._df = self._df.dropna(how='all', axis=1)  # Drop columns that are entirely NaN
            self._df = self._df.dropna(how='all')  # Drop rows that are entirely NaN

            self.process_csv(self._df)



    def process_csv(self, campers_df):

        # default to a cabin size of 10 if none is provided
        max_cabin_size = 10

        try:
            max_cabin_size = int(self.numeric_var.get())
        except ValueError:
            print("No valid cabin size provided, defaulting.")

        column_names = {}

        grade_column = campers_df.filter(like="Current grade").columns[0]
        column_names["Grade"] = grade_column

        age_column = campers_df.filter(like="Age").columns[0]
        column_names["Age"] = age_column

        gender_column = campers_df.filter(like="Gender").columns[0]
        column_names["Gender"] = gender_column

        buddy_columns = campers_df.filter(like="Buddy").columns
        column_names["Buddy"] = buddy_columns

        campers_df['Full Name'] = campers_df['First name'] + ' ' + campers_df['Last name']  # new line to create 'Full Name'

        # Create a new column 'SortValue' in the DataFrame where if the 'Age' is less than or equal to 0,
        # it will take the value of 'Current grade' otherwise it will take the value of 'Age'
        campers_df['SortValue'] = campers_df[age_column].where(campers_df[age_column] > 0, campers_df[grade_column])

        # Now sort the DataFrame based on the 'SortValue' and 'Gender' columns
        sorted_campers_df = campers_df.sort_values(by=[gender_column, 'SortValue'])

        # Make sure to drop the 'SortValue' column after sorting
        sorted_campers_df.drop('SortValue', axis=1, inplace=True)

        campers_dict = scrape_camper_csv(sorted_campers_df, column_names)

        buddy_groups = gen_buddy_groups(sorted_campers_df, campers_dict)

        def flatten(lst):
            flat_list = []
            for group in lst:
                flat_list.extend(group.get_members())
            return flat_list

            # Getting assigned campers
        # Getting assigned campers
        assigned_campers = [camper for camper in flatten(buddy_groups)]

        # Get all campers' full names from the DataFrame
        all_campers_set = set(campers_df['Full Name'])

        # Get all assigned campers' full names
        assigned_campers_set = set(camper._name for camper in assigned_campers)

        # Find the unassigned campers
        unassigned_campers = all_campers_set - assigned_campers_set

        # Convert sets to lists
        assigned_campers_list = list(assigned_campers_set)
        unassigned_campers_list = list(unassigned_campers)

        # Ask user for directory to save the CSV files
    
        save_dir = filedialog.askdirectory(title="Select Directory to Save CSVs")

        if save_dir:  # If the user selects a directory
            # Create DataFrame for unassigned campers
            unassigned_campers_df = campers_df[campers_df['Full Name'].isin(unassigned_campers_list)]
            unassigned_campers_df.to_csv(f'{save_dir}/unassigned_campers.csv', index=False)

            # Creating the buddy groups CSV with extra lines between groups
            with open(f'{save_dir}/buddy_groups.csv', 'w') as f:
                for group in buddy_groups:
                    # Get members of the group and their details from the DataFrame
                    group_members = group.get_members()
                    group_df = campers_df[campers_df['Full Name'].isin([member._name for member in group_members])]

                    # Sort the group DataFrame by a specific column (e.g., 'Full Name')
                    group_df = group_df.sort_values(by='Full Name')

                    # Write the group data to the CSV
                    group_df.to_csv(f, index=False, header=f.tell() == 0)

                    # Write an empty line after each group
                    f.write('\n')

            print(f"CSV files created: {save_dir}/buddy_groups.csv and {save_dir}/unassigned_campers.csv")
        else:
            print("No directory selected, files not saved.")
            
        debug_buddy_groups(buddy_groups)
        
        quit()
        

    def get_data_frame(self): 
        return self._df


def main() -> None:
    root = tk.Tk()
    app = BunkedGui(root)
    root.mainloop()

main()
