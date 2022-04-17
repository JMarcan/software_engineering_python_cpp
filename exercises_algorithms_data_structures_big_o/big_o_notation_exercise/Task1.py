"""
Read file into texts and calls.
"""

import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
TASK 1:
How many different telephone numbers are there in the records? 
Print a message:
"There are <count> different telephone numbers in the records."
"""

unique_numbers = set()

for record in texts:
    #if number is not yet in the list, add it
    if record[0] not in unique_numbers:
        unique_numbers.add(record[0])
        
     #if number is not yet in the list, add it
    if record[1] not in unique_numbers:
        unique_numbers.add(record[1])
        
for record in calls:
    #if number is not yet in the list, add it
    if record[0] not in unique_numbers:
        unique_numbers.add(record[0])
        
     #if number is not yet in the list, add it
    if record[1] not in unique_numbers:
        unique_numbers.add(record[1])        
# Answer to the Task 1
print ("There are <{0}> different telephone numbers in the records".format(len(unique_numbers)))