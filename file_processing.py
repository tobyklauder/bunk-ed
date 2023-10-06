# Author: Toby Klauder 

# Author defined imports 
from objects.camper import Camper
from objects.cabin import Cabin

# Python imports
import tkinter as tk
from tkinter import ttk
import pandas as pd 
from typing import Dict, List

def scrape_camper_csv(_df, column_names) -> Dict[str, List[Camper]]: 
    campers = {"Male": [], "Female": []} 

    # for each row in the table _df 
    for index, row in _df.iterrows(): 
        # Get camper gender 
        curr_gender = row[column_names["Gender"]]

        # Process Buddy Requests
        buddy_requests = process_buddy_requests(row[column_names["Buddy"]])

        # Add camper to the campers dictionary, including buddy-requests if they exist
        if buddy_requests:
            campers[curr_gender].append(Camper(row["Full Name"], row[column_names["Age"]], row[column_names["Grade"]], row[column_names["Gender"]], buddy_requests))
        else: 
            campers[curr_gender].append(Camper(row["Full Name"], row[column_names["Age"]], row[column_names["Grade"]], row[column_names["Gender"]]))

    return campers 


def process_buddy_requests(buddy_columns) -> List[str]:
    buddy_requests = []

    # For all buddy columns that are not NaN, add them to the buddy_requests list
    for buddy_column in buddy_columns:
        if pd.notna(buddy_column): 
            buddy_requests.append(buddy_column)

    return buddy_requests
