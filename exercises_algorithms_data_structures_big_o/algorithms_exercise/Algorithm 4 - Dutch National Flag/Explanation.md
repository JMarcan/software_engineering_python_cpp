To sort the array in a single traversal for an input array consisting on only 0, 1, and 2, and optimize its run time,
my algorithm loops through each element and if the element is zero, it appends it to the array of zeroes, 
if the element is one, it appends it in the array of ones, if the element is two, it appends it in the array of twos.
In the end all three arrays are merged into one and the sorted array is returned.


Time complexity: O(n) as we loop through each item
Space Complexity O(n)
Where n is the array size.  