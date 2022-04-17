class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def __str__(self):
        cur_head = self.head
        out_string = ""
        while cur_head:
            out_string += str(cur_head.value) + " -> "
            cur_head = cur_head.next
        return out_string


    def append(self, value):

        if self.head is None:
            self.head = Node(value)
            self.tail = self.head
            return
        
        node = Node(value)
        self.tail.next = node
        self.tail = node

    def size(self):
        size = 0
        node = self.head
        while node:
            size += 1
            node = node.next

        return size

def union(llist_1, llist_2):
    """
        Returns union of two provided LinkedLists
    
        Args:
            - llist_1(LinkedList): data to be written into the new block
            - llist_2(LinkedList)

        Returns:
            - True if the block was added. Otherwise False
    """

    if llist_1 is None or isinstance(llist_1, LinkedList) is False or llist_2 is None or isinstance(llist_2, LinkedList) is False:
        print ("[Warrning] union: Lists cannot be none. Returning empty list")
        return LinkedList()

    if llist_1.head is None: 
        return llist_2
    
    if llist_2.head is None: 
        return llist_1

    union_list = LinkedList()
    s = set()
    
    # loop through l1 list
    current_l1 = llist_1.head
    while current_l1: 
        val = current_l1.value
        if val not in s: 
            s.add(val)
            union_list.append(val)
        current_l1 = current_l1.next

    # loop through l2 list
    current_l2 = llist_2.head 
    while current_l2: 
        val = current_l2.value
        if val not in s: 
            s.add(val)
            union_list.append(val)
        current_l2 = current_l2.next

    return union_list

def intersection(llist_1, llist_2):
    
    if llist_1 is None or isinstance(llist_1, LinkedList) is False or llist_2 is None or isinstance(llist_2, LinkedList) is False:
        print ("[Warrning] intersection: Lists cannot be none. Returning empty list")
        return LinkedList()
    
    intersected_list = LinkedList()
    s = set()
    
    current_l1 = llist_1.head
    
    while current_l1:
        if current_l1.value not in s:
            s.add(current_l1.value)
        current_l1 = current_l1.next
        
    current_l2 = llist_2.head
    while current_l2:
        val = current_l2.value
        if val in s:
            intersected_list.append(val)
            s.remove(val)
        current_l2 = current_l2.next
    
    return intersected_list


def test_cases():

    linked_list_1 = LinkedList()
    linked_list_2 = LinkedList()

    element_1 = [3,2,4,35,6,65,6,4,3,21]
    element_2 = [6,32,4,9,6,1,11,21,1]

    for i in element_1:
        linked_list_1.append(i)

    for i in element_2:
        linked_list_2.append(i)

    # TC 1 - Intersection
    print(intersection(linked_list_1,linked_list_2))
    if (str(intersection(linked_list_1,linked_list_2)) == "6 -> 4 -> 21 -> "):
        print ("TC 1. Passed")
    else:
        print ("TC 1. Failed")
    
    # TC 2 - Union
    print (union(linked_list_1,linked_list_2))
    if (str(union(linked_list_1,linked_list_2)) == "3 -> 2 -> 4 -> 35 -> 6 -> 65 -> 21 -> 32 -> 9 -> 1 -> 11 -> "):
        print ("TC 2. Passed")
    else:
        print ("TC 2. Failed")
        
    # TC 3 - Pass lists with value None to intersection
    linked_list_3 = None
    linked_list_4 = None
    
    if isinstance(intersection(linked_list_3,linked_list_4), LinkedList) == True:
        print ("TC 3. Passed")
    else:
        print ("TC 3. Failed") 
        
    # TC 4 - Pass lists with value None to union  
    if isinstance(union(linked_list_3,linked_list_4), LinkedList) == True:
        print ("TC 4. Passed")
    else:
        print ("TC 4. Failed")    

if __name__ == '__main__':
    # execute test cases  
    test_cases()    
'''
'''
