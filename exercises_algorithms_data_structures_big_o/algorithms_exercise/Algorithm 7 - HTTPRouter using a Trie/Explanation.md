To provide routing functionality for a web server and optimize its run time,
Trie structure was implemented with handler structure.

In the best case, all words in the Trie have common path (e.g. "/home" and "/home/user") and algorithm will take only as long as the longest path to traverse. It takes O(k) where k is the length of the longest path.
In the worst case there are no paths shared (e.g. "/other/path and "home/user") and each path  will be in separate branch that must be traversed. It takes O(n) time and storage where n is number of paths in the Trie.

Time complexity: O(n) 
Space Complexity O(n)
where n is number of paths in the Trie