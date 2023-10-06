# Author: Toby Klauder 
# Date: 10/04/2023 

import re 
from typing import List 

class Camper:

    # Constructor for the camper class 
    def __init__(self, name, age, grade, gender, buddy_requests=None) -> None:
        """
        Creates a camper object. 

        args: 
        name: camper name (string)
        age: camper age (string)
        grade: camper grade (string)
        gender: camper gender (string)
        buddy_requests: camper buddy requests (string)

        returns: 
        None
        """
        self._name = name 
        self._age = int(age) 

        # Extract the grade from the grade column
        pattern = r'\d+'
        grade = re.findall(pattern, grade)

        # Set the grade to the first element in the matched list. 
        self._grade = int(grade[0])
        self._gender = gender  
        self._buddy_requests = buddy_requests

    # Getters
    def get_name(self) -> str: 
        """
        Returns the camper's name.

        args:
        None

        returns:
        camper name (string)
        """
        return self._name
    
    def get_age(self) -> int:
        """
        Returns the camper's age 

        args:
        None

        returns:
        camper age (int)
        """
        return self._age
    
    def get_grade(self) -> int:
        """
        Returns the camper's grade

        args: 
        None

        returns:
        camper grade (int)
        """
        return self._grade 
    
    def get_gender(self) -> str: 
        """
        Returns the camper's gender 

        args: 
        None 

        returns: 
        camper gender (string)
        """
        return self._gender 
    
    def get_buddy_requests(self) -> List[str]:
        """
        Return the camper's buddy requests 

        args:
        None 

        returns: 
        camper buddy requests 
        """
        return self._buddy_requests
    
    # Setters
    def set_name(self, name) -> None:
        """
        Set the camper's name 

        args: 
        new name for the camper - name (string)

        returns: 
        None
        """
        self._name = name

    def set_age(self, age) -> None:
        """
        Set the camper's age

        args:
        new age for the camper - age (int)

        returns:
        None
        """
        self._age = age
    
    def set_grade(self, grade) -> None:
        """
        Set's the campers grade

        args: 
        new grade for the camper - grade (int)

        returns:
        None
        """
        self._grade = grade 

    def set_gender(self, gender) -> None: 
        """
        Set's the campers gender 

        args: 
        new gender for the camper - gender (camper)

        returns: 
        None 
        """
        self._gender = gender 

    # Methods 

    def valid_pair(self, other_camper):
        """
        Compares two campers based on age and grade. 

        args: 
        other_camper: the other camper to compare to

        returns: 
        True if the campers are valid, False otherwise
        """
        if (abs(self._grade - other_camper.get_grade()) > 1 or self._gender != other_camper.get_gender()):
            return False
        else: 
            return True


    