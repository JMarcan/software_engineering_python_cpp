def get_min_max(ints):
    """
    Return a tuple(min, max) out of list of unsorted integers.

    Time Complexity O(n)
    Space Complexity O(1)
    
    Args:
       ints(list): list of integers containing one or more integers
    """
    # Test that ints is an not empty array
    if len(ints) == 0:
          return -1, -1
    
    # Test that ints consists of digits between 0 and 9
    for element in ints:
        if element < 0 or element > 9:
            return -1, -1
        
    min_int = None
    max_int = None
    
    for i, element in enumerate(ints):
        if i == 0:
            min_int = element
            max_int = element
        else:
            if element < min_int:
                min_int = element
            if element > max_int:
                max_int = element
    
    return (min_int, max_int)

## Test Case of Ten Integers
import random

l = [i for i in range(0, 10)]  # a list containing 0 - 9
random.shuffle(l)

print ("Pass" if ((0, 9) == get_min_max(l)) else "Fail")

## Edge Test Case of single digit, should print 1,1
print ("Pass" if ((1, 1) == get_min_max([1])) else "Fail")

## Edge Test Case of empty input, , should print 1,1
print ("Pass" if ((-1, -1) == get_min_max([])) else "Fail")