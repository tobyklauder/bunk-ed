# Author: Toby Klauder

from objects.cabin import Cabin

def get_unassigned_campers(camper_lookup):
    """Get a list of campers that haven't been assigned to a buddy group.

    Args:
        camper_lookup (dict): A dictionary of campers, keyed by name.

    Returns:
        list: A list of unassigned camper objects.
    """
    return list(camper_lookup.values())

def assign_cabins(): 
    cabins = [] 
    
    for i in range(1, 31): 
        cabins.append(Cabin())
    
    for cabin in cabins: 
        print(cabin.get_cabin_number())

