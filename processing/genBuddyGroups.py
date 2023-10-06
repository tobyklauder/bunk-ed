# Author: Toby Klauder 

# Python imports 
import pandas as pd
from fuzzywuzzy import process

# Local imports 
from objects.buddy_group import BuddyGroup

def create_camper_lookup(campers):
    """
    Create a lookup dictionary mapping camper names to camper objects.
    
    Args:
        campers (dict): A dictionary with genders as keys and lists of camper objects as values.
        
    Returns:
        dict: A dictionary with camper names as keys and camper objects as values.
    """
    
    # Initialize an empty dictionary to hold the mapping of camper names to camper objects
    camper_lookup = {}

    # Iterate over each list of campers (grouped by gender) in the campers dictionary
    for gender_list in campers.values():
        
        # For each camper in the current gender list
        for camper in gender_list:
            
            # Map the camper's name to the camper object in the lookup dictionary
            camper_lookup[camper.get_name()] = camper

    # Return the completed lookup dictionary
    return camper_lookup


def find_existing_group_for_buddy(buddy_group, _df, group_lookup):
    """
    Finds an existing group for a given buddy group.

    Args:
        buddy_group (list): A list of buddies to find a group for.
        _df (pandas.DataFrame): A DataFrame containing the 'Full Name' column to search for buddy matches.
        group_lookup (dict): A dictionary containing buddy names as keys and their corresponding group as values.

    Returns:
        list or None: A list of buddies in an existing group if a match is found, otherwise None.
    """

    # Return an empty list if the input buddy_group is also empty
    if not buddy_group:
        return []  
    
     # Loop through each buddy in the input list
    for buddy in buddy_group:  
        # Use fuzzy string matching to find the best match for the buddy's name in the DataFrame
        buddy_best_match, buddy_score = process.extractOne(buddy, _df['Full Name'].tolist())
        
        # Check if the fuzzy matching score is greater than 85 and if the best match exists in the group_lookup dictionary
        if buddy_score > 85 and buddy_best_match in group_lookup:
            # Return the existing group associated with the matched buddy's name
            return group_lookup[buddy_best_match]
    
    # If no match is found for any buddy in the input group, return None
    return None


def recursively_add_buddies(group, buddy, _df, camper_lookup, group_lookup):
    """
    Checks to see if you can recursively add buddies to a group.

    Args:
        group (BuddyGroup): The group to add the buddies to.
        buddy (str): The buddy to add to the group.
        _df (DataFrame): A pandas DataFrame containing camper data.
        camper_lookup (dict): A dictionary mapping camper names to camper objects.
        group_lookup (dict): A dictionary mapping group IDs to group objects.
    
    Returns:
        None
    """
        # Perform fuzzy string matching to find the best matching buddy name in the DataFrame
    best_match, score = process.extractOne(buddy, _df['Full Name'].tolist())

    # Look up the camper associated with the best matching buddy, or set to None if not found
    matched_camper = camper_lookup.get(best_match, None)

    # Check if the matching score is above 85, there's a matched camper, and the camper is not already in the group
    if score > 85 and matched_camper and not group.is_member_in_group(matched_camper):
        # Add the matched camper to the group
        group.add_member(matched_camper)
        
        # Remove the best matched buddy from the camper_lookup dictionary
        del camper_lookup[best_match]
        
        # Add the camper to the group_lookup dictionary, mapping the camper's name to the group
        group_lookup[matched_camper.get_name()] = group

        # Now, check this matched camper's buddies and try to add them to the group
        next_buddies = matched_camper.get_buddy_requests()
        
        # Check if next_buddies is not None before iterating
        if next_buddies:
            for next_buddy in next_buddies:
                # Recursively add the buddies to the group
                recursively_add_buddies(group, next_buddy, _df, camper_lookup, group_lookup)



def add_to_existing_group_or_create_new(camper, existing_group, buddy_group, _df, camper_lookup, group_lookup):
    """
    Adds a camper to an existing buddy group or creates a new buddy group with the camper as the first member.

    Args:
        camper (Camper): The camper to add to the buddy group.
        existing_group (BuddyGroup): The existing buddy group to add the camper to.
        buddy_group (list): A list of buddies for the camper.
        _df (DataFrame): A pandas DataFrame containing camper data.
        camper_lookup (dict): A dictionary mapping camper names to camper objects.
        group_lookup (dict): A dictionary mapping group IDs to group objects.

    Returns:
        list: A list of BuddyGroup objects that were created as a result of adding the camper to a group.
    """
    # Initialize an empty list to store buddy groups
    buddy_groups = []

    # Check if an existing group is provided, and if the camper can be added to it
    if existing_group and existing_group.add_member(camper) != -1:
        # If successful, remove the camper from the camper_lookup dictionary
        del camper_lookup[camper.get_name()]
    else:
        # If no existing group or unable to add the camper to it, create a new BuddyGroup
        group = BuddyGroup()
        
        # Add the camper to the newly created group
        group.add_member(camper)
        
        # Remove the camper from the camper_lookup dictionary
        del camper_lookup[camper.get_name()]

        # If there is a buddy_group (list of buddies), iterate through it
        if buddy_group is not None:
            for buddy in buddy_group:
                # Recursively add buddies to the group
                recursively_add_buddies(group, buddy, _df, camper_lookup, group_lookup)

        # Check if the group has more than one member
        if group.get_members_count() > 1:
            # If so, append the group to the list of buddy_groups
            buddy_groups.append(group)

    # Return the list of buddy_groups
    return buddy_groups


def process_buddies_by_gender(gender_key, campers, _df, camper_lookup, group_lookup):
    """
    Process buddies for a given gender.

    Args:
        gender_key (str): The gender key to process buddies for.
        campers (dict): A dictionary of campers, keyed by gender.
        _df (pandas.DataFrame): A DataFrame containing group information.
        camper_lookup (dict): A dictionary of campers, keyed by name.
        group_lookup (dict): A dictionary of groups, keyed by name.

    Returns:
        list: A list of buddy groups.
    """
    # Initialize an empty list to store buddy groups
    buddy_groups = []

    # Iterate through campers of a specific gender (campers[gender_key])
    for camper in campers[gender_key]:
        # Check if the camper's name is not in the camper_lookup dictionary
        if camper.get_name() not in camper_lookup:
            continue  # Skip this camper if their name is not in the lookup dictionary

        # Retrieve the list of buddy requests for the current camper
        buddy_group = camper.get_buddy_requests()
        
        # Find an existing group for the buddy group or create a new group
        existing_group = find_existing_group_for_buddy(buddy_group, _df, group_lookup)
        
        # Add the camper to existing groups or create new groups
        new_groups = add_to_existing_group_or_create_new(camper, existing_group, buddy_group, _df, camper_lookup, group_lookup)
        
        # Extend the buddy_groups list with the newly created or modified groups
        buddy_groups.extend(new_groups)

    # Return the list of buddy_groups
    return buddy_groups


def gen_buddy_groups(_df, campers):
    """
    Generate buddy groups for a given list of campers.

    Args:
        _df (pandas.DataFrame): A DataFrame containing camper buddy preferences.
        campers (list): A list of camper names.

    Returns:
        list: A list of buddy groups, where each group is a list of camper names.
    """
    # Initialize an empty list to store buddy groups
    buddy_groups = []

    # Initialize an empty dictionary to store group information
    group_lookup = {}

    # Create a camper lookup dictionary based on the campers provided
    camper_lookup = create_camper_lookup(campers)

    # Iterate through gender keys, which are ["Male", "Female"]
    for gender_key in ["Male", "Female"]:
        # Process buddies for each gender, creating buddy groups
        gender_buddy_groups = process_buddies_by_gender(gender_key, campers, _df, camper_lookup, group_lookup)
        
        # Extend the buddy_groups list with the groups created for this gender
        buddy_groups.extend(gender_buddy_groups)

    # Return the list of buddy_groups containing groups organized by gender
    return buddy_groups



def debug_buddy_groups(buddy_groups):
    """
    Print out buddy groups for debugging purposes.

    Args:
        buddy_groups (list): A list of buddy groups, where each group is a list of camper names.

    Returns:
        None
    """

    # For each buddy group 
    for group in buddy_groups:

        # Print spacing  
        print("\n\nGroup: ")

        # For each member in each buddy group 
        for buddy in group.get_members(): 
            print(buddy.get_name())
 
