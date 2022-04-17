'''
 The main user interface for top_k_elements allowing you 
 to get unique record identifiers of k-largest values
 by processing your file or
 by processing your stdinput
'''
import unittest
import argparse
import sys
import heapq
import logging
from typing import List
from top_k_elements.top_k_elements import TopElements

# configure logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

def print_results(top_k: List[int]) -> None:
    '''Print unique record identifiers of k-largest values 
        in the format specified in the requirements

        Args:
            - top_k(List[int]): list o top_k elements to be printed
        Returns:
            - None
    '''
    for item in top_k:
        print (item)
def main():
    '''User inteface processing your input arguments
        and printing unique record identifiers 
        of k-largest values in your data
        
        Console Args:
            - k     (int)           : number of top k record_identifiers to be returned
            - file  (str)(optional) : path to file with data to be analyzed. Otherwise, stdin is used
        Example:
            - Example 1 (stdin)     : python main.py -k 1
            - Example 2 (file)      : python main.py -k 3 --file tests/input_test_1.txt
        Returns:
            - None
    '''
    parser = argparse.ArgumentParser(description='Input file path')
    parser.add_argument("-k", type=int, required=True, help="k-largest values for which ID shall be returned")
    parser.add_argument("--file", help="Input file path")

    args = parser.parse_args()
    if args.file is not None:
        top_k = TopElements.get_top_k_from_file(args.k, args.file)
    else:
        top_k = TopElements.get_top_k_from_stdin(args.k)

    print_results(top_k)

if __name__ == '__main__':
    main()
    

