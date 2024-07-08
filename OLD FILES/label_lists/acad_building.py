import os
import sys 

academic_building_labels = [
    "RM 201", "RM 203", "RM 205", "RM 207", "RM 209", 
    "HALL 200", "RM 208", "RM 210", "004 ACADEMIC BUILDING SECOND FLOOR"
]

file = open('acad_building.txt', 'w')

for item in academic_building_labels:
    file.write(item+"\n")
