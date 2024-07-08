import os 
import sys 

labels_second_image = [
    'RECREATION ROOM', 'THEATER ROOM', 'LAUNDRY', 'ROOM B'
    'Hall', 'Room A', 'Stairs', 'Bath', 'Wet Bar', 'D1'
    'D2', 'D3', 'D4', 'D5', 'D6'
]

file = open("Blocton-1.txt", "w") 

for item in labels_second_image:
    file.write(item+"\n")