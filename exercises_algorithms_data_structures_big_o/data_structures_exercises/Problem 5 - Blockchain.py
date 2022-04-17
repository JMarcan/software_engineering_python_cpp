import hashlib
from datetime import datetime

  
class Block:

    def __init__(self, timestamp, data_hash, previous_hash, previous_block, index):
      """
        Initialize one blockchain Block 
    
        Args:
            - timestamp(str): timestamp when the block was created 
            - data_hash(str): hashed data to be stored
            - previous_hash(str): hash of the previous block
            - index(int): index of a block

        Returns:
            - None
      """
      self.timestamp = timestamp
      self.hash = data_hash
      self.previous_hash = previous_hash
      self.previous_block = previous_block
      self.index = index
      
    def __repr__(self):
        return str.format("\nThis is a block with an index: \'{0}\', timestamp:\'{1}\', \
                          hash: \'{2}\', previous hash: \'{3}\'\n \
                          ".format(self.index, self.timestamp, self.hash, self.previous_hash))
  
class Blockchain:
    
    def __init__(self, name):
        """
        Initialize a blockchain 
    
        Args:
            - name(str): name of the blockchain

        Returns:
            - None
      """
        self.name = name
        self.head = None
        self.last_block_idx = 0
    
    def calc_hash(self, hash_str):
      sha = hashlib.sha256()
     
      sha.update(hash_str.encode('utf-8'))
      
      return sha.hexdigest()
  
    def add_block(self, data):
        """
        Add a block to the blockchain 
    
        Args:
            - data(str): data to be written into the new block

        Returns:
            - True if the block was added. Otherwise False
      """
        if data is None or type(data) is not str or len(data) < 1 :
            print ("[Warrning] add_block: Invalid data (None, or not string or empty string). No block is addedd.")
            return False
   
        self.last_block_idx += 1
        data_hash = self.calc_hash(data)
        
        previous_block = self.head
        if self.head == None:
            # for the first block initialization
            previous_hash = None
        else:
            previous_hash = self.head.hash
        
        b = Block(datetime.now(), data_hash, previous_hash, previous_block, self.last_block_idx)
        self.head = b
        
        return True
        
def test_cases():
    blockchain = Blockchain("My Blockchain")
    
    #TC 1
    res = blockchain.add_block("First Block")
    if res == True:
        print ("TC 1. Passed")
    else:
        print ("TC 1. Failed")
    
    #TC 2
    res = blockchain.add_block("Second Block")
    if res == True:
        print ("TC 2. Passed")
    else:
        print ("TC 2. Failed")
    
    #TC 3
    res = blockchain.add_block("Third Block")
    if res == True:
        print ("TC 3. Passed")
    else:
        print ("TC 3. Failed")
    
    #TC 4 - corner case - None
    res = blockchain.add_block(None)
    if res == False:
        print ("TC 4. Passed")
    else:
        print ("TC 4. Failed")
    
    #TC 5 - corner case - empty string
    res = blockchain.add_block("")
    if res == False:
        print ("TC 5. Passed")
    else:
        print ("TC 5. Failed")
    
    # visual verification for TC 1-3
    block = blockchain.head
    while block:
        print (block)
        block = block.previous_block
      
if __name__ == '__main__':
    # execute test cases  
    test_cases() 

    
    