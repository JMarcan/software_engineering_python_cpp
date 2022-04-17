To rearrange array digits so two numbers are formed in a way that their sum is maximum and optimize its run time,
my algorithm applies first mergesort to sort the array in O(n log(n)) time. 

Then it loops through the list and to produce a maximum sum of these two numbers,
 each even element is added to the number one, each odd element is added to the number two.

Time complexity: O(n log(n)) inherited from mergesort
Space Complexity: O(n)
Where n is the array size 