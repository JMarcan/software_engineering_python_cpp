def rotated_array_search(input_arr, number):
    """
    Find the index by searching in a rotated sorted array
    
    Time complexity: O(log2(n)) (as long as array is rotated only once)
    Space Complexity: O(1)
    Where n is the array size

    Args:
       input_array(array), number(int): Input array to search and the target
    Returns:
       int: Index or -1
    """
    
    pivot_idx = find_pivot(input_arr, 0, len(input_arr))
    
    # if we have not found an pivot, the array is not rotated
    if pivot_idx == -1:
        return binary_search(input_arr, number)
    
    #if we found a pivot then first 
    if input_arr[pivot_idx] == number:
        return pivot_idx
    
    if input_arr[0] <= number:
        return binary_search(input_arr, number, 0, pivot_idx-1);
    else:
        return binary_search(input_arr, number, pivot_idx+1, len(input_arr)-1,);
    

def find_pivot(input_arr, min_idx, max_idx):
    """
    Find the the pivor index of an rotated array
    
    Time complexity: O(1og2(n))
    Space Complexity: O(1)

    Args:
       input_array(array): rotated array
    Returns:
       pivot_idx(int)
    """
    
    mid = (min_idx + max_idx) // 2
    
    # if  mid element is higher than the next one, we found an pivot
    if mid < max_idx and input_arr[mid] > input_arr[mid + 1]: 
        return mid 
    # if  mid-1 element is higher than the next one (mid element), we found an pivot
    if mid > min_idx and input_arr[mid] < input_arr[mid - 1]: 
        return (mid-1) 
    
    # if the first element is higher than the current (mid) element,
    # call recrusion for the lower interval
    if input_arr[min_idx] >= input_arr[mid]: 
        return find_pivot(input_arr, min_idx, mid-1)
    # else if the first element is lower than the current (mid) element,
    # call recrusion for the higher interval
    else:
        return find_pivot(input_arr, mid + 1, max_idx) 
    
def binary_search(input_list, number, min_idx, max_idx):
    """
     Find the index for a given value (number) by searching in a sorted array
     
     Time complexity: O(log2(n))
     Space Complexity: O(1)
    
     Args:
         - input_list(array): sorted array of numbers to be searched in
         - number(int): number to be searched for

     Returns:
        - position(int): reuturns array index for the given number
                         returns -1 when the number was not found
    """
    # corner case for case when provided min_idx is higher than provided max_idx
    if max_idx < min_idx: 
        return -1
    
    # binary search
    while min_idx <= max_idx:
        mid = (min_idx + max_idx) // 2

        # Check if x is present at mid
        if input_list[mid] == number:
            return mid
        
        # If the guess was too low, set min to be one larger than the guess
        if input_list[mid] < number:
            min_idx = mid + 1
      
        # If the guess was too high, set max to be one smaller than the guess
        else:
            max_idx = mid - 1

    # if we got here, the number was not found
    return -1
    
def linear_search(input_list, number):
    """
     Find the index for a given value (number) by searching in a sorted array
     
     Time complexity: O(n) 
     Space Complexity: O(1)
    
     Args:
         - input_list(array): sorted array of numbers to be searched in
         - number(int): number to be searched for

     Returns:
        - position(int): reuturns array index for the given number
                         returns -1 when the number was not found
    """
    for index, element in enumerate(input_list):
        if element == number:
            return index
    return -1

def test_rotated_array_search(test_case):
    input_list = test_case[0]
    number = test_case[1]
    if linear_search(input_list, number) == rotated_array_search(input_list, number):
        print("Pass")
    else:
        print("Fail")

def test_binary_search(test_case):
    input_arr = test_case[0]
    number = test_case[1]
    if linear_search(input_arr, number) == binary_search(input_arr, number, 0, len(input_arr)):
        print("Pass")
    else:
        print("Fail")


print ("=== Binary search test cases execution ===:")
test_binary_search([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5]) 
test_binary_search([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4])     
test_binary_search([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3])    
test_binary_search([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2]) 
test_binary_search([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1]) 
   
print ("=== rotated_array_search, test cases ===:")
test_rotated_array_search([[6, 7, 8, 9, 10, 1, 2, 3, 4], 6])
test_rotated_array_search([[6, 7, 8, 9, 10, 1, 2, 3, 4], 1])
test_rotated_array_search([[6, 7, 8, 1, 2, 3, 4], 8])
test_rotated_array_search([[6, 7, 8, 1, 2, 3, 4], 1])
test_rotated_array_search([[6, 7, 8, 1, 2, 3, 4], 10])

print ("=== rotated_array_search, edge test cases ===:")
test_rotated_array_search([[6, 7, 8, 1, 2, 3, 4], 25]) #accessing non existing positive index
test_rotated_array_search([[6, 7, 8, 1, 2, 3, 4], -1]) #accessing negative