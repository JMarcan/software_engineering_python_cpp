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
TASK 2: Which telephone number spent the longest time on the phone
during the period? Don't forget that time spent answering a call is
also time spent on the phone.
Print a message:
"<telephone number> spent the longest time, <total time> seconds, on the phone during 
September 2016.".
"""

time_spent = {}

for record in calls:
    
    time = int(record[3])
    
    calling_number = record[0]
    #if number is already in the list, increment its calling time
    #if number is not yet in the list, set current calling time as number's calling time
    if calling_number in time_spent:
        time_spent[calling_number] = time_spent[calling_number] + time
    else:
        time_spent[calling_number] = time
        
    receiving_number = record[1]
    #if number is already in the list, increment its calling time
    #if number is not yet in the list, set current calling time as number's calling time
    if receiving_number in time_spent:
        time_spent[receiving_number] = time_spent[receiving_number] + time
    else:
        time_spent[receiving_number] = time
    
most_calling_number = max(zip(time_spent.values(), time_spent.keys()))

# Answer to the Task 2
print("<{0}> spent the longest time, <{1}> seconds, on the phone during \
      September 2016.".format(most_calling_number[1], most_calling_number[0]))
