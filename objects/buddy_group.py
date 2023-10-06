#Author: Toby Klauder 

from typing import List

class BuddyGroup: 

    def __init__(self):
        """
        Creates a buddy group object. 
        """
        self. _members = [] 
        self._grades = []
        self._gender = ""
    
    def get_grades(self) -> List[int]:
        """
        Get the grades of the group (should be no more than 2)

        returns:
            the grades of the group
        """
        return self._grades
    
    def get_members(self) -> List[str]:
        """
        Gets the members of the group 

        returns: 
            the members of the group 
        """
        return self._members
    
    def is_member_in_group(self, member) -> bool:
        """
        Checks if a member is already in the group 

        returns: 
            True if the member is in the group, False otherwise
        """
        return member in self._members
    
    def get_members_count(self) -> int:
        """
        Get the total count of all members in the group

        returns: 
            the total count of all members in the group
        """
        return len(self._members)
    
    def clear_members(self) -> None:
        """
        Clears all of the members of the group 

        returns: 
            None
        """
        self._members.clear()
    
    def get_gender(self): 
        """
        Get the gender of the group 

        returns: 
            the gender of the group 
        """
        return self._gender 
    
    def remove_member(self, member):
        self._members.remove(member)
    
    def add_member(self, member):
        # If first added to the group, the group is of that gender 
        if self._gender == "": 
            self._gender = member.get_gender() 
            
        if len(self._members) == 10: 
            return -1 

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