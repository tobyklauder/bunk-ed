# bunk'ed 
## a lightweight application to group campers into their cabins

This small a lightweight application was built for SAMBICA Camps and Retreat Center during the Summmer of 2023. 

Previously, they had been creating all cabin assignments for campers by hand, which caused hours of labor on the part of the full time staff at the organization. 

This system takes in a .csv file. The file must include columns: "Name", "Age", "Grade", and "Buddy". Optionally, you may include "School". 

Campers will be matched to other campers of similar age and similar grade within a reasonable range as determined by the user. (i.e. a 4th grader may be placed into a cabin with a 5th grader if the age variance is 1)

Campers will also be reasonably placed with a buddy of their choosing if their buddy is also within the reasonable user defined paramaters for age and grade ranges. 

If aggressive pairing is enabled, then campers will also be matched with individuals from their school, also within the reasonable user defined parameters. 

Future features include: 

Black/Whitelists - to keep campers with previous conflict apart from one another. 

Development on this project is ongoing and is expected to conclude in early July 2023. 


# Maintainer Documentation 

## assign_cabins 

The assign_cabins function groups campers into cabins based on their gender and age, while also considering their buddy requests. The function takes three parameters: 'sorted_campers_df', a dataframe containing campers information, 'age_range', an optimal parameter that specifies the maximium allowed age difference between campers in a cabin (default is 2); and 'output_file'; an optional parameter that specifies the output file name for the cabin pairings (default is 'cabin_pairings.csv'). 

The function first groups the campers by gender and iterates through each gender group. For each camper, it checks if they have a buddy request and adds both the camper and their buddy to the same cabin if the buddy request can be fulfilled. The function then attempts to fill the cabin with campers within the specified age range. Once a cabin is full or there are no more campers to add, the cabin is added to the cabins dictionary, and the process continues with the next camper. 

Finally, the cabin pairings are written to a file specified by the 'output_file' parameter. The function returns the cabins dictionary, which contains the final cabin assignments. 

## assign_cabins_aggressive 

Works in the same way as the above, but also if possible groups campers by their school. 