import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd 
from processing.file_processing import scrape_camper_csv
from processing.genBuddyGroups import gen_buddy_groups
from processing.genBuddyGroups import debug_buddy_groups

class BunkedGui:

    _df = None

    def __init__(self, root) -> None:
        """
        Initalize the tkinter window 

        args:
            root: the root of the tkinter window

        returns:
            None
        """
        self.root = root

        # Set the title for the window 
        self.root.title("Bunk'ed")
        
        # Set the size of the window 
        self.root.geometry("200x120")
        
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

    def get_csv(self): 
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        _df = None

        if file_path:
            _df = pd.read_csv(file_path)
            self.process_csv(_df)

        return _df 
    
    def process_csv(self, campers_df):

        column_names = {} 

        grade_column = campers_df.filter(like="Grade").columns[0]
        column_names["Grade"] = grade_column

        age_column = campers_df.filter(like="Age").columns[0]
        column_names["Age"] = age_column

        gender_column = campers_df.filter(like="Gender").columns[0]
        column_names["Gender"] = gender_column

        buddy_columns = campers_df.filter(like="Buddy").columns
        column_names["Buddy"] = buddy_columns

        campers_df['Full Name'] = campers_df['First name'] + ' ' + campers_df['Last name']  # new line to create 'Full Name'
            
            # Create a new column 'SortValue' in the DataFrame where if the 'Age' is less than or equal to 0,
            # it will take the value of '2023 > Grade' otherwise it will take the value of 'Age'
        campers_df['SortValue'] = campers_df[age_column].where(campers_df[age_column] > 0, campers_df[grade_column])

            # Now sort the DataFrame based on the 'SortValue' and 'Gender' columns
        sorted_campers_df = campers_df.sort_values(by=[gender_column, 'SortValue'])

            # Make sure to drop the 'SortValue' column after sorting
        sorted_campers_df.drop('SortValue', axis=1, inplace=True)

        campers_dict = scrape_camper_csv(sorted_campers_df, column_names)
            
        buddy_groups = gen_buddy_groups(sorted_campers_df, campers_dict)

        debug_buddy_groups(buddy_groups)

        
    def get_data_frame(self): 
        return self._df


def main() -> None:
    root = tk.Tk()
    app = BunkedGui(root)
    root.mainloop()

main() 

