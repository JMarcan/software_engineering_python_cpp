def sort_012(input_arr):
    """
    Given an input array consisting on only 0, 1, and 2, sort the array in a single traversal.

    Time Complexity O(n)
    Space Complexity O(n)
    Where n is the array size.  
    
    Args:
       input_arr(array): Array to be sorted
       
    Returns:
        sorted_arr(array): Sorted array
    """
    # Test that input_arr consists of digits between 0 and 9
    for element in input_arr:
        if element < 0 or element > 2:
            return (-1, -1)
        
    bin_zeros = []
    bin_ones = []
    bin_twos = []
    
    for element in input_arr:
        if element == 0:
            bin_zeros.append(element)
        elif element == 1:
            bin_ones.append(element)
        elif element == 2:
            bin_twos.append(element)
    
    sorted_arr = bin_zeros + bin_ones + bin_twos         
    return sorted_arr

def test_function(test_case):
    sorted_array = sort_012(test_case)
    print(sorted_array)
    if sorted_array == sorted(test_case):
        print("Pass")
    else:
        print("Fail")
        
def test_function_edge(test_case):
    sorted_array = sort_012(test_case)
    print(sorted_array)
    if sorted_array == (-1, -1):
        print("Pass")
    else:
        print("Fail")

print ("=== Test cases ===:")
test_function([0, 0, 2, 2, 2, 1, 1, 1, 2, 0, 2])
test_function([2, 1, 2, 0, 0, 2, 1, 0, 1, 0, 0, 2, 2, 2, 1, 2, 0, 0, 0, 2, 1, 0, 2, 0, 0, 1])
test_function([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2])

print ("=== Edge test cases ===:")
# test that -1 will be returned for provided invalid input with not allowed value 3
test_function_edge([1, 2, 3]) 
# test that -1 will be returned for provided invalid input with not allowed negative values
test_function_edge([0, -1, -2]) 