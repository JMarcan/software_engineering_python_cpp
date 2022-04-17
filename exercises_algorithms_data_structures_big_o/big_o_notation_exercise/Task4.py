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
TASK 4:
The telephone company want to identify numbers that might be doing
telephone marketing. Create a set of possible telemarketers:
these are numbers that make outgoing calls but never send texts,
receive texts or receive incoming calls.

Print a message:
"These numbers could be telemarketers: "
<list of numbers>
The list of numbers should be print out one per line in lexicographic order with no duplicates.
"""

possible_telemarketers = []

# gather list of all unique numbers who called to anybody
for record in calls:
    calling_number = record[0]
    if calling_number not in possible_telemarketers:
        possible_telemarketers.append(calling_number)

# to identify possible telemarketers
# eliminate from the list numbers that send texts, receive texts or receive incoming calls

# eliminate the ones that receive calls
for record in calls:
    receiving_number = record[1]
    
    if receiving_number in possible_telemarketers:
        possible_telemarketers.remove(receiving_number)

# eliminate the ones that send or receive texts
for record in texts:
    sending_number = record[0]
    receiving_number = record[1]
    
    if sending_number in possible_telemarketers:
        possible_telemarketers.remove(sending_number)
        
    if receiving_number in possible_telemarketers:
        possible_telemarketers.remove(receiving_number)

possible_telemarketers.sort()

# Answer to the Task 4
print("Those numbers could be a telemarketers:")
for number in possible_telemarketers:
    print(number)
    

