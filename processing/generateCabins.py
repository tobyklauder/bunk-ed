# Author: Toby Klauder 

import pandas as pd
from fuzzywuzzy import fuzz

from objects.buddy_group import BuddyGroup

def gen_buddy_groups(_df, campers): 
    """
    Generates buddy group objects for the given camper db
    Args:
        _df (_type_): _description_
        campers (_type_): _description_
    """
    
    # 0 for male, 1 for female 
    buddy_groups = {0: [], 1: []}
    
    # Iterate through male camper groups 
    for camper in campers["Male"]: 
        # If the camper has a buddy-request, add them to the buddy group 
        if camper.get_buddy_requests(): 
            buddy_group = BuddyGroup()
            buddy_requests = camper.get_buddy_requests()

            generate_network(campers, buddy_requests, buddy_group)
        
        buddy_groups[0].append(buddy_group)
        
    for camper in campers["Female"]: 
        if camper.get_buddy_requests(): 
            buddy_group = BuddyGroup()
            buddy_requests = camper.get_buddy_requests()
            
            generate_network(campers, buddy_requests, buddy_group)
        
        buddy_groups[1].append(buddy_group)

    return 
def generate_network(campers, buddy_requests, buddy_group, gender_key):
     # Loop over all male campers 
     for buddy in buddy_requests: 
        for buddy_search in campers[gender_key]: 
                        
        # Get the name (cause dict stores Camper objects)
            buddy_search = buddy_search.get_name() 
                        
        # Allow for some spelling errors in the name 
            if is_name_similar(buddy, buddy_search):
                buddy_group.add_buddy(buddy_search)
                if buddy.get_buddy_requests():  
                    generate_network(campers, buddy_requests, buddy_group)
                else: 
                    campers[gender_key].remove(buddy) 

    
def is_name_similar(name1, name2, threshold=80):
    """
    Check if two names are similar based on a similarity score.
    """
    similarity = fuzz.ratio(name1, name2)
    return similarity >= threshold
            