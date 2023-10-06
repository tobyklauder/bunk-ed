#Author: Toby Klauder 

class Cabin: 

    _cabin_count =  0 # The number of cabins created (static)

    def __init__(self, _cabin_gender) -> None:
        """
        Initializes a cabin object.

        args:
        _cabin_gender: the cabin gender as a number (0 for male, 1 for female)
        _cabin_number: the cabin number
        """
        self._cabin_gender = _cabin_gender 
        self._campers = [] 
        self.cabin_grade = [] 
        self._cabin_name = ""

        # Set the cabin number and increment the cabin count
        self._cabin_number = Cabin._cabin_count
        Cabin._cabin_count += 1

        # Set the cabin's counselor (not stored by default according to client)
        self._counselor = ""


    def validate_camper(self, camper) -> bool:
        """
        Ensures that the camper is a valid addition to the cabin.
        
        args:
        camper: camper object to validate with the cabin

        returns: 
        True if the camper is valid to add to the cabin
        """

        # Assume camper is valid to add to the cabin
        add_flag = True

        # For all campers in the cabin, check if the camper is a valid pair
        for o_camper in self._campers: 
            if o_camper.valid_pair(camper) == False: 

                # If any camper is not a valid match to the camper, the camper is not valid to be added to the cabin. 
                add_flag = False

        return add_flag


    def add_camper(self, camper) -> int:
        """
        attempts to add the camper to the cabin. 

        args: 
            camper: camper object to add to the cabin
        returns:
            1 if the camper was successfully added to the cabin
            -1 if the cabin is full
        """

        # If the cabin already has the maximum number of campers
        if len(self._campers) >= 10:
            return -1
        
        # If the camper's grade isn't in the cabin grade and cabin grade has less than 2 distinct grades
        if camper.get_grade() not in self._cabin_grade and len(self._cabin_grade) == 0:
            self._cabin_grade.append(camper.get_grade())
        # If the camper's grade isn't a match and cabin grade has 2 distinct grades or if the camper's grade matches
        elif camper.get_grade() in self._cabin_grade:
            pass
        elif camper.get_grade() not in self._cabin_grade and len(self._cabin_grade) == 1 and abs(camper.get_grade() - self._cabin_grade[0]) <= 1:
            self._cabin_grade.append(camper.get_grade())
        else: 
            return -1 

        self._campers.append(camper)
        return 1


    def remove_camper(self, camper):
        """
        Removes the camper from the cabin.

        args: 
            camper: camper object to remove from the cabin
        """
        self._campers.remove(camper)

    # Setters

    def set_counselor(self, counselor):
        """
        Sets the cabin's counselor. 

        args: 
         counselor: the counselor's name
        """
        self._counselor = counselor

    def set_cabin_name(self, name): 
        """
        Sets the cabin's name. 

        args: 
            name: the cabin's name
        """
        self._cabin_name = name 
    
    # Getters 

    def get_counselor(self) -> str:
        """
        Gets the counselor of the cabin. 

        args: 
            name: the counselors name 
        """
        return self._counselor
    
    def get_cabin_name(self) -> str:
        """
        Get's the name of the cabin.

        returns: 
            the name of the cabin
        """
        return self._cabin_name
    
    def get_cabin_number(self) -> int:
        """
        Gets the cabin number.

        returns:
            the cabin number
        """
        return self._cabin_number
    
    def get_cabin_gender(self) -> int: 
        """
        Get the cabin gender 

        returns: 
            the cabin gender 
        """
        return self._cabin_gender
    
    def get_campers(self) -> list:
        """
        Gets the campers in the cabin.

        returns: 
            list of campers in the cabin 
        """ 
        return self._campers