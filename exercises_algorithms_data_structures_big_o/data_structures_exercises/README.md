# data_structures_exercise

## Motivation
I did this project as part of Udacity, Data Structure and Algorithms Nanodegree that I took to ensure that my code is written efficiently. 
This is especially important for solutions that need to be scaled. Or solutions with limited computing power. As robots.

## Project description
**My goal for the project was to use the right data structures for each of the six problems:**
1. LRU Cache: Design data structure known as a Least Recently Used (LRU) Cache
2. File Recursion: Design algorithm to find all files under a directory with extension *.c* 
3. Huffman Coding: Implement Huffman encoding and decoding algorithm
4. Active Directory: Write function providing efficient lookup of whether the user is in a group 
5. Blockchain: Use linked lists and hashing to create a full blockchain implementation
6. Union and Intersection: Design algorithm to provide union and intersection of two linked lists

**To achieve the optimal time and space complexity:**
1. LRU Cache: I use hash table combined with linked list achieving Time Complexity O(1),  Space complexity O(1) for set and get operations. Where n is the cache size
2. File Recursion: The algorithm goes through each item in a selected directory. Subfolders are searched by recursion call. Achieving Time Complexity O(n),  Space complexity O(n) where n is the number of items (files and subfolders) in a folder
3. Huffman Coding: The algorithm achieves for encoding Time Complexity O(n logn), Space complexity O(n). For decoding, it has Time Complexity O(n), Space complexity O(n). Where n is the number of characters 
4. Active Directory: As member users are unique inside of a specific group, set() structure is used instead of list offering average higher search (x in y) performance O(1) than list O(n). [Source](https://wiki.python.org/moin/TimeComplexity). The worst-case Time Complexity is O(n), Space complexity is O(n). Where n is the number of groups
5. Blockchain: The linked list structure containing hashes achieves Time Complexity O(1) for adding a new blockchains, Space Complexity O(n). Where n is the number of blocks
6. Union and Intersection:  The algorithm for union and intersection achieves Time Complexity O(n) , Space Complexity O(n). Where n is the number of items in both lists. 
 

**Sample solution for the 1. algorithm:**
1. LRU Cache:  The implemented data structure for cache works with a hash table (dictionary) referencing to the linked list (cached objects). 
- To address the need for fast lookup, the hash table (dictionary) was implemented to achieve O(1) time complexity 
- To address the need for fast insertion and deletion, the linked object working as a list was implemented to achieve O(1) time complexity.

Time and space complexity:
- get: Time O(1), Space O(1) -> Thanks to our hash table (dictionary)
- set: Time O(1), Space O(1) -> Thanks to our linked list
where n is a cache size

```
def set(self, key, value):
        """
         Set the value if the key is not present in the cache. 
         If the cache is at capacity remove the oldest item. 
    
        Args:
            key(str): key under which will be cache item accessed
            value(str): value to be stored for cache item

        Returns:
            None
        """
        
        if self.capacity < 1:
            print("Cannot perform operations on cache capacity less than 1 (0}".format(self.capacity))
            return
        
        head = self.cached_items.get(self.head_key)
        new_item = CachedItem(value)
        
        if head is None:
            self.head_key = key
            self.tail_key = key
        else:
            new_item.prev_key = self.head_key
            head.next_key = key
        
        self.cached_items[key] = new_item
        self.head_key = key
        
        if len(self.cached_items) > self.capacity:
            print("Cache capacity exceeded, deleting the last accessed item {0}".format(self.tail_key))
            tail = self.cached_items[self.tail_key]
            del self.cached_items[self.tail_key]
            self.tail_key = tail.next_key
```

## Usage & Files in the repository
- You can download the repository and find each algorithm in its folder.
- For example, Algorithm 1 is in file `Problem 1 - LRU Cache.py`
- Each solution is briefly described with its time and space complexities in in `Explanation.txt`

## Libraries used
Python 3