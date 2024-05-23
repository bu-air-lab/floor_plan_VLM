import os 
import sys

baker_1_labels = [
    "EXAM", "WAITING", "NURSE STATION", "OFFICE", 
    "PROCEDURES", "EXAM 1", "EXAM 2", "X-RAY"
]

file = open('Baker-1.txt', 'w')

for item in baker_1_labels:
    file.write(item+"\n")




