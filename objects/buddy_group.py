class BuddyGroup: 

    _members = [] 
    _grades = []
    _gender = ""

    def __str__(self): 
        out = ""

        for member in self._members: 
            out += str(member.get_name()) + "\n"

        return out
    
    def get_grades(self):
        return self._grades
    
    def get_gender(self): 
        return self._gender 
    
    def remove_member(self, member):
        self._members.remove(member)
    
    def add_member(self, member):
        # If first added to the group, the group is of that gender 
        if self._gender == "": 
            self._gender = member.get_gender() 

        if member.get_gender() != self._gender: 
            return -1 

        # If the member's grade isn't in the group grade and group grade has less than 2 distinct grades
        if member.get_grade() not in self._grades and len(self._grades) == 0: 
            self._grades.append(member.get_grade())
        # If the member's grade isn't a match and group grade has 2 distinct grades or if the member's grade matches
        elif member.get_grade() in self._grades:
            pass
        elif member.get_grade() not in self._grades and len(self._grades) == 1 and abs(member.get_grade() - self._grades[0]) <= 1:
            self._grades.append(member.get_grade())
        else: 
            return -1
    
        self._members.append(member)