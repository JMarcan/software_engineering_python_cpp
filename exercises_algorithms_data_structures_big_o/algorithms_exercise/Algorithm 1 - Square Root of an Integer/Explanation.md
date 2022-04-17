To calculate square root of a provided number without using any existing Python build-in functionality,
the algorithm iteratively multiply i*i till result is less than a given number. The floor of the square root of the number is then i - 1. 
I've applied binary search for its quick O(log2 n) run.

Time complexity: O(log n)
Space Complexity: O(1)
Where n is value of the Integer