# Author: Toby Klauder 
# Date: 10/04/2023 

import re 

class Camper:

    #Private internal state 
    _name = ""
    _age = 0
    _grade = 0
    _gender = "" # 0 for male, 1 for female, 2 for other 
    _buddy_requests = None

    # Constructor for the camper class 
    def __init__(self, name, age, grade, gender, buddy_requests=None):
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
    def get_name(self): 
        return self._name
    
    def get_age(self):
        return self._age
    
    def get_grade(self):
        return self._grade 
    
    def get_gender(self): 
        return self._gender 
    
    def get_buddy_requests(self):
        return self._buddy_requests
    
    # Setters
    def set_name(self, name):
        self._name = name

    def set_age(self, age):
        self._age = age
    
    def set_grade(self, grade):
        self._grade = grade 

    def set_gender(self, gender): 
        self._gender = gender 

    # Methods 

    def valid_pair(self, other_camper):
        """
        Compares two campers based on age and grade. 
        """
        if (abs(self._grade - other_camper.get_grade()) > 1 or self._gender != other_camper.get_gender()):
            return False
        else: 
            return True


    