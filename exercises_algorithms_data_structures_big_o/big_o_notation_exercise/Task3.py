"""
Read file into texts and calls.
"""
import csv
import math

with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
TASK 3:
(080) is the area code for fixed line telephones in Bangalore.
Fixed line numbers include parentheses, so Bangalore numbers
have the form (080)xxxxxxx.)

Part A: Find all of the area codes and mobile prefixes called by people
in Bangalore.
 - Fixed lines start with an area code enclosed in brackets. The area
   codes vary in length but always begin with 0.
 - Mobile numbers have no parentheses, but have a space in the middle
   of the number to help readability. The prefix of a mobile number
   is its first four digits, and they always start with 7, 8 or 9.
 - Telemarketers' numbers have no parentheses or space, but they start
   with the area code 140.

Print the answer as part of a message:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
The list of codes should be print out one per line in lexicographic order with no duplicates.

Part B: What percentage of calls from fixed lines in Bangalore are made
to fixed lines also in Bangalore? In other words, of all the calls made
from a number starting with "(080)", what percentage of these calls
were made to a number also starting with "(080)"?

Print the answer as a part of a message::
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
The percentage should have 2 decimal digits
"""
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

calls_from_bangalore = 0 # to calculate the Part B
calls_bangalore_bangalore = 0 # to calculate the Part B

called_prefixes_bangalore = []

for record in calls:
    calling_number = record[0]
    
    # if calling number is from Bangalore
    if calling_number.startswith("(080)") or calling_number.startswith("080"):
        calls_from_bangalore = calls_from_bangalore + 1
        
        called_number = record[1]
        called_prefix = ""
        #if it's fixxed line, extract area code from called number
        end = called_number.find(")")
        if end != -1:
            called_prefix = called_number[1:end]
            
            if called_prefix == "080":
                calls_bangalore_bangalore = calls_bangalore_bangalore + 1
        #if it's not fixed line, extracts mobile prefix
        else:
            #The prefix of a mobile number is its first four digits
            called_prefix = called_number[:4]
            
        #if are code or mobile prefix is not yet in the list, add it
        if called_prefix not in called_prefixes_bangalore:
            called_prefixes_bangalore.append(called_prefix)

# sort phone codes in lexicographic order
            
called_prefixes_bangalore.sort()

# Answer to the Task 3, the part A   
print("The numbers called by people in Bangalore have codes:")

for phone_code in called_prefixes_bangalore:
    print(phone_code)

#print (calls_bangalore_bangalore)
#print(calls_from_bangalore)
   
# Answer to the task 3, the part B    
print ("<{:.2f}> percent of calls from fixed lines in Bangalore are calls to other \
       fixed lines in Bangalore".format(
       round((100*calls_bangalore_bangalore)/calls_from_bangalore, 2)))    