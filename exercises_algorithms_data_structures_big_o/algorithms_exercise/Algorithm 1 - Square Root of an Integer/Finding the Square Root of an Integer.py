def sqrt(number:int):
    """
     Calculates square root of a provided number 
     without using any predefined built in functions
     
     Time complexity: O(log n)
     Space Complexity: O(1)
     Where n is value of the Integer
    
     Args:
         - number(int): number for which will be calculated square root 

     Returns:
        - ans(int): calculated square root of a provided number 
                    -1 when not positive numeric value was provided
   """
   
    # corner cases when negative number is provided, return -1
    if number < 0:
        return -1
    
    # corner cases when number is 0 or 1
    if number == 0 or number == 1:
        return number
    
    # binary search for floor(sqrt(x))
    start = 1
    end = number
    while (start <= end):
        mid = (start + end) // 2
        
        # if number is a perfect square
        if (mid*mid == number):
            return mid
        
        # We need floor, so we update answer as long as mid*mid is smaller than x and move closer to sqrt
        if mid * mid < number:
            start = mid + 1
            ans = mid
            
        # mid * mid is greated than x => end the cycle. Sqrt is the last ans
        else:
            end = mid - 1
            
    return ans

# test cases
print ("Pass" if  (3 == sqrt(9)) else "Fail")
print ("Pass" if  (4 == sqrt(16)) else "Fail")
print ("Pass" if  (5 == sqrt(27)) else "Fail")

# edge cases
print ("Pass" if  (0 == sqrt(0)) else "Fail")
print ("Pass" if  (1 == sqrt(1)) else "Fail")
print ("Pass" if  (-1 == sqrt(-3)) else "Fail")