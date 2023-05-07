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