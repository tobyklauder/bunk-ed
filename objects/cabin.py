#Author: Toby Klauder 

class Cabin: 

    # Private internal state

    _campers = []
    _counselor = ""
    _cabin_name = ""
    _cabin_number = 0
    _cabin_gender = 0 # 0 for male, 1 for female, 2 for other 
    _cabin_grade = [] 

    def __init__(self, _cabin_number, _cabin_gender) -> None:
        self._cabin_number = _cabin_number
        self._cabin_gender = _cabin_gender 


    def validate_camper(self, camper) -> bool:
        """Ensures that the camper is a valid addition to the cabin."""
        add_flag = True
        for o_camper in self._campers: 
            if o_camper.valid_pair(camper) == False: 
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
        self._campers.remove(camper)

    # Setters

    def set_counselor(self, counselor):
        self._counselor = counselor

    def set_cabin_name(self, name): 
        self._cabin_name = name 
    
    # Getters 

    def get_counselor(self) -> str:
        return self._counselor
    
    def get_cabin_name(self) -> str:
        return self._cabin_name
    
    def get_cabin_number(self) -> int:
        return self._cabin_number
    
    def get_cabin_gender(self) -> int: 
        return self._cabin_gender
    
    def get_campers(self) -> list: 
        return self._campers