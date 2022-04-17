'''The module top_k_elements allows you 
 to get record_identifiers of k-largest values
 by processing file  (method 'get_top_k_from_file') or
 by processing stdin (method 'process_stdin')

 Example:
    output = TopElements.get_top_k_from_file(k, file_path)
        where k is your desired number of max values
    output = TopElements.get_top_k_from_stdin(5, "tests/input_test_3.txt")

 Expected input format:
    <unique record identifier><white_space><numeric value>
    e.g.:
        1426828011 9
        1426828028 350
        1426828037 25
    Lines that do not conform to the format are ignored.
    Module notifies you about them by issuing warning message.

 Time complexity: O(log(k) + O(n) = O(n) 
  - Algorithm itself takes O(log k) where k is your desired number of max values
  - However, processing of extremely large files exceeding available RAM
    requires reading line by line which itself is O(n) operation

 Space complexity: 
  - O(k) where k is your desired number of max values

 The algorithm is based on binary heap

  TODO: Depends on end-users feedback. Few options:
    - speedup processing:
        - E.g. if bottleneck would be CPU and not I/O, 
            we could add multiprocessing, each processing a different part of the file
    - improve user experience:
        - E.g. improve input data quality analysis so user sees how many and which lines were skipped
        - E.g. display progress % with number of processed/remaining lines
'''
import unittest
import heapq
import sys
import logging
import os.path
from typing import List

logger = logging.getLogger(__name__)

class TopElements:
    '''TopElements allows you 
        to get record_identifiers of k-largest values
        by processing file  (method 'get_top_k_from_file') or
        by processing stdin (method 'process_stdin')
    '''
    @staticmethod
    def get_top_k_from_stdin(k: int)-> List[int]:
        '''Returns top k record_identifiers associated with the highest value

            Args:
                k (int) : number of top k record_identifiers to be returned
            Returns:
                top_k   : top k record_identifiers with the highest value
        '''
        # return empty list for k-values that are 0 or negative 
        if k < 1:
            return []

        # variables
        top_k_candidates = [] # binary heap (min-heap)
        line_idx = 1
        
        # process stdin
        for line in sys.stdin:
            if 'Exit' == line.rstrip():
                break
            res = TopElements.__process_line(top_k_candidates, k, line)
            if res == 0:
                logging.warning(
                    f'Invalid data format. Skipping this one: \'{line}\'') 
            line_idx += 1

         # return top-x elements
        return TopElements.__return_top_k(top_k_candidates)

    @staticmethod
    def get_top_k_from_file(k: int, input_file : str = None) -> List[int]:
        '''Returns top k record_identifiers associated with the highest value
        
            Args:
                k           (int): number of top k record_identifiers to be returned
                input_file  (str): path to file containing data to be analyzed
            Returns:
                top_k: top k record_identifiers with the highest value        
        '''
        # return empty list for k-values that are 0 or negative 
        if k < 1:
            return []

        # variables
        top_k_candidates = [] # binary heap (min-heap)
        invalid_lines = 0
        line_idx = 1

        # Process input file
        try:
            f = open(input_file, 'r')
        except IOError:
            logging.error(f'Cannot open file \'{input_file}\'') 
            return []

        # Reading line by line (O(n)) allows us to read extremely large files exceeding available RAM
        for line in f:
            res = TopElements.__process_line(top_k_candidates, k, line)
            if res == 0:
                invalid_lines += 1
                logging.warning(
                    f'{invalid_lines}. Invalid data format. input_file: \'{input_file}\' Skipping line: \'{line_idx}\'. Line data: \'{line}\'') 
            line_idx += 1
        f.close()
           
        # Return top-x elements
        return TopElements.__return_top_k(top_k_candidates)

    @staticmethod
    def __process_line(top_k_candidates: list, k: int, line: str) -> int:
        '''Process data in a given line 
            and keep it between top_k_candidates 
            if it has a higher value than previous candidates or if k limit was not reached yet.
            Only the highest k candicates are kept to optimize memory and handle even extremely large files. 

            Args:
                top_k_candidates (list): number of top k elements that will be returned
                k                (int):  number of top k elements that will be returned
                line             (str):  data of a given line to be processed

            Returns:
                (int): 1 if the line was processed. 0 if data were in the wrong format

            Algorithm time complexity: O(log(k)
            Space complexity: O(k)       
        ''' 
        # parse the line
        # & catch and skip incorrect input line processing
        item = line.split()
        
        if len(item) != 2:
            return 0
        try:
            index = int(item[0])
        except:
            return 0
        try:    
            value = int(item[1])
        except:
            return 0
        
        # Store first top k elements into the heap
        if len(top_k_candidates) < k:
            heapq.heappush(top_k_candidates, (value, index))

        # Keep only top k elements in the heap
        else:
            min_top_value = top_k_candidates[0][0] #It's min-heap
            if value > min_top_value:
                # Time complexity: O(log(k))
                # Space complexity: O(k)
                heapq.heappushpop(top_k_candidates, (value, index))
        return 1

    @staticmethod
    def __return_top_k(top_k_candidates: list) -> List[int]:
        top_k = []
        for item in top_k_candidates:
            index = item[1]
            top_k.append(index)

        return top_k