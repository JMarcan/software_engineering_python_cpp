# big_O_notation_exercise

## Motivation
This project was completed as part of my Data Structures & Algorithms Nanodegree at Udacity,
that I took to ensure that my code is written efficiently. This is especially important for solutions that need to be scaled. Or solutions with limited computing power. As robots.

## Project description
**My goal for the project was to implement code to analyze a dataset of phone calls and calculate its Big-O Notation.**

![comparison of computational complexity](comparison_computational_complexity.png)

Tasks:
- Task 0. Identify what is the first record of texts and what is the last record of calls
- Task 1. Identify how many different telephone numbers are there in the records
- Task 2. Identify which telephone number spent the longest time on the phone
- Task 3. Identify all of the area codes and mobile prefixes called by people in Bangalore
- Task 4. Identify a set of possible telemarketers

## Usage
The implemented solutions can be downloaded and directly run for each task in its file.

## Files in the repository
- `Task0.py`: Implemented code for task 0
- `Task1.py`: Implemented code for task 1
- `Task2.py`: Implemented code for task 2
- `Task3.py`: Implemented code for task 3
- `Task4.py`: Implemented code for task 4
- `Analysis.txt`: Run time complexity analysis for each task (Worst-Case Big O Notation)
- `calls.csv`: Analyzed calls data. The following columns are present: calling telephone number (string), receiving telephone number (string), start timestamp of telephone call (string), duration of a telephone call in seconds (string)
- `texts.csv`: Analyzed text data. The following columns are present: sending telephone number (string), receiving telephone number (string), timestamp a of text message (string)

## Libraries used
Python 3


**Code sample for the 1. algorithm:**
- Time complexity: `O(n)` as we loop through each record. Where n is the number of records.
- Space complexity: `O(n)` as in the worst case each new record represents an unique number we need to store. Where n is the number of records.
- Design choice:  To store unique numbers, **Set structure** is used instead of List as it's the most efficient, and we don't care about the order of items to calculate the total count of unique numbers. When testing whether we already stored the given number, set works with hash tables, it just looks whether the object is at the position determined by its hash, so the speed of this operation does not depend on the size of the Set. In contrast, for List the whole List would need to be searched, which would provide us with worse performance than with Set structure.
```
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
```

**Code sample for the 2. algorithm:**
- Time complexity: `O(n)` as we loop through each record. Where n is the number of records.  
- Space complexity: `O(n)` as in the worst case each new record represents an unique number we need to store. Where n is the number of records.
- Design choice:  To store how much time each number spent by calling, **Dictionary structure** is used to store key-value pairs between phone number and time spent by calling. 
```
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
