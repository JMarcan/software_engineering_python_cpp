# algorithms_exercise

## Motivation
I did this project as part of Udacity, Data Structure and Algorithms Nanodegree that I took to ensure that my code is written efficiently. 
This is especially important for solutions that need to be scaled. Or solutions with limited computing power. As robots.

## Project description
**My goal for the project was to use the right algorithm for each of the seven problems:**
1. Finding the Square Root of an Integer: without using any predefined built-in functions
2. Search in a Rotated Sorted Array 
3. Rearrange Array Elements: to form two number such that their sum is maximum
4. Dutch National Flag Problem: Given an input array consisting of only 0, 1, and 2, sort the array in a single traversal
5. Autocomplete with tries: Provide auto-complete function based on user input
6. Max and Min in an Unsorted Array: without using any predefined built-in functions
7. Implement HTTPRouter using a Trie

**To achieve the optimal time and space complexity:**
1. Finding the Square Root of an Integer: The algorithm uses binary search. Achieving Time Complexity: O(log n). Space Complexity: O(1). Where n is the value of the Integer.
2. Search in a Rotated Sorted Array:  The algorithm first finds a pivot and then applies binary search. Achieving Time Complexity: O(log n). Space Complexity: O(1). Where n is the array size. 
3. Rearrange Array Elements: The algorithm first applies mergesort to sort the array, then it loops through the list to produce a maximum sum of these two numbers. Achieving Time Complexity: O(n log(n)) inherited from mergesort. Space Complexity: O(n). Where n is the array size.   
4. Dutch National Flag Problem: The algorithm loops through the array and sorts 3 possible numbers into predefined arrays that are in the end merged. Achieving Time Complexity: O(n) as we loop through each item. Space Complexity O(n). Where n is the array size.  
5. Autocomplete with tries: Trie structure with a simple recursive function is used. The worst-case Time Complexity: O(n)[*1]. Space complexity: O(n) where n is the number of words.
6. Max and Min in an Unsorted Array: The algorithm loops through the unsorted array and uses min and max variables. Achieving Time Complexity: O(n) as we loop through each element. Space Complexity O(1). Where n is the number of integers in the array.
7. Implement HTTPRouter using a Trie: Trie structure with the handler is used. The worst-case Time Complexity: O(n)[*1]. Space complexity: O(n) where n is the number of paths.  

[*1] Time complexity for Trie structure depends on the nature of its data:
- In the best-case, all words in the Trie have common letter (e.g. "trie", "trigger", "trigonometry", "tripod") and the algorithm will take only as long as the longest word to traverse. It takes O(k) where k is the length of the longest word.
- In the worst-case, there are no letters shared (e.g. "ant, "function", "trie") and each word will be in a separate branch that must be traversed. It takes O(n) time and storage where n is the number of words in the Trie.

**Code sample for the 1. algorithm:**
```
ef sqrt(number:int):
    """
     Calculates square root of a provided number 
     without using any predefined built in functions
     
     Time complexity: O(log n)
     Space Complexity: O(1)
    
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
```
 

## Usage & Files in the repository
- You can download the repository and find each algorithm in its folder. The code is commented with time and space complexities
- For example, Algorithm 1 is in folder `Algorithm 1 - Square Root of an Integer`
- Each subfolder contains the algorithm itself in `.py` (or `.ipynb` file) and a short description in `Explanation.txt`

## Libraries used
Python 3

