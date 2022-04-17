class CachedItem:
    def __init__(self, value):
        self.value = value
        self.next_key = None
        self.prev_key = None

    def __repr__(self):
        """ return value as a string when class is used in print statement self.cached_items"""
        if self.value is None:
            return 'None'
        return str(self.value)


class LRU_Cache(object):

    def __init__(self, capacity):
        """
         Initialize LRU_Cache with selected capacity 
    
        Args:
            - capacity(int): cache capacity

        Returns:
            - None
        """
        if capacity < 1:
            print ("Warrning: Input cache capacity was less than 1 ({0}). \
                   Cache is initialized with the capacity 1".format(capacity))
            capacity = 1
            
        print ("Cache initialized with the capacity: {0}".format(capacity))
        
        self.cached_items = {}
        self.capacity = capacity
        self.num_entries = 0
        self.head_key = None
        self.tail_key = None

    def get(self, key):
        """
         Retrieve cached item from provided key. 
    
        Args:
            key(str): key of cached item to be retrieved

        Returns:
            - returns item.value
            - returns -1 if nonexistent in the cache 
        """
        
        item = self.cached_items.get(key)
        
        print("\nGet Element with Key: {0}\n \
        Head: {1}\n \
        Tail: {2}\n \
        Cache: {3}".format(key, self.head_key, self.tail_key, self.cached_items))
        
        if item is None:
            return -1
        
        if item.prev_key is not None:
            self.items[item.pre_keyv].next_key = item.next_key
        else:
            print("Updating tail with key: {0}".format(key))
            self.tail_key = item.next_key
            
        if item.next_key is not None:
            self.cached_items[item.next_key].prev_key = item.prev_key

        head = self.cached_items.get(self.head_key, None)
        if head is not None:
            head.next_key = key

        item.prev_key = self.head_key
        item.next_key = None

        self.head_key = key
        
        return item.value
          

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
    
    def size(self):
        return self.num_entries

def test_cases(cache_size):
    """
    Execute test cases for LRU_Cache
    Print statements whether the test case passed or not are printed
    
    Args:
      cache_size(int): size of cache to be initialized

    Returns:
       None
    """
    our_cache = LRU_Cache(cache_size)

    our_cache.set(1, 1)
    our_cache.set(2, 2)
    our_cache.set(3, 3)
    our_cache.set(4, 4)
    
    # TC 1
    if our_cache.get(1) == 1: # returns 1
        print ("TC 1. Passed")
    else: 
        print ("TC 1. Failed")
        
    # TC 2    
    if our_cache.get(2)  == 2: # returns 2
        print ("TC 2. Passed")
    else: 
        print ("TC 2. Failed")
        
    # TC 3 - old, already removed items from the cahce   
    if our_cache.get(9)  == -1: # returns -1 because 9 is not presented in the cache
        print ("TC 3. Passed")
    else: 
        print ("TC 3. Failed")
        
    our_cache.set(5, 5) 
    our_cache.set(6, 6)
    
    # TC 4 - old, already removed items from the cahce
    if our_cache.get(3)  == -1: # returns -1 because the cache reached it's capacity and 3 was the least recently used entry
        print ("TC 4. Passed")
    else: 
        print ("TC 4. Failed")
        
    # TC 5 - not existing index  
    if our_cache.get(-1)  == -1: # returns -1 because -1 index do not exists
        print ("TC 5. Passed")
    else: 
        print ("TC 5. Failed")
        
    # TC 6 - empty cache
    empty_cache = LRU_Cache(cache_size) 
    if empty_cache.get(1)  == -1: # returns -1 because the cache is empty
        print ("TC 6. Passed")
    else: 
        print ("TC 7. Failed")
        
if __name__ == '__main__':
    # execute test cases  
    test_cases(5)    
    