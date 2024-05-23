import os 
import sys

hospital_labels = [
    "CONSULTATION", "WAITING", "EXAM A", "EXAM B", 
    "BUSINESS OFFICE", "Hallway", "EXAM C", 
    "STAFF WORK ROOM", "NURSE STATION", "EXAM D"
]


file = open("hospital.txt", "w") 

for item in hospital_labels:
    file.write(item+"\n")