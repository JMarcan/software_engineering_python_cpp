To provide autocomplete function based on user input and optimize its run time,
Trie structure was implemented with a simple recursive function. 

In the best case, all words in the Trie have common letter (e.g. "trie", "trigger", "trigonometry", "tripod") and algorithm will take only as long as the longest word to traverse. It takes O(k) where k is the length of the longest word.
In the worst case there are no letters shared (e.g. "ant, "function", "trie") and each word will be in separate branch that must be traversed. It takes O(n) time and storage where n is number of words in the Trie.

Time complexity: O(n) 
Space Complexity O(n)
where n is number of words in the Trie