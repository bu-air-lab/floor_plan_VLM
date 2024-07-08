import os 
import sys 

labels_first_image = [
    'Doctor Office', 'Exam 1', 'Exam 2', 'Exam 3', 'Exam 4', 'Exam 5', 'Exam 6', 
    'Hallway', 'Procedures', 'supply', 'supply', 'supply', 'lab', 'lab/nurse',
    'Waiting Area', 'Business Ofiice', 'data', 'wc', 'Nurse/supply'
]

file = open('Blocton-1.txt', 'w')

for item in labels_first_image:
    file.write(item+"\n")