'''
 To run unit tests for the top_k_elements module, 
 execute from the main project directory
 python -m unittest
'''
import unittest
from top_k_elements.top_k_elements import TopElements

class Test_Top_k_elements(unittest.TestCase):
    '''
    P.S. assertCountEqual is used here to comply with requirements.
        Despite its name it checks whether two lists contains the same elements
        without taking into consideration their order
        Example:
        - [0, 1, 1] and [1, 0, 1] is evaluated equal
        - [0, 0, 1] and [0, 1] is evaluated not equal
    '''

    def test_1(self):
        # Example behaviour 1 from requirements
        k = 3
        input_file = 'tests/input_test_1.txt'
        expected_output = [1426828028, 1426828066, 1426828056]
        output = TopElements.get_top_k_from_file(k, input_file)

        self.assertCountEqual(expected_output, output)

    def test_2(self):
        # Example behaviour 2 from requirements
        k = 2
        input_file = 'tests/input_test_2.txt'
        expected_output = [1426828011, 1426828066]
        output = TopElements.get_top_k_from_file(k, input_file)

        self.assertCountEqual(expected_output, output)
    
    def test_3(self):
        # Empty input
        k = 3
        input_file = 'tests/input_test_3.txt'
        expected_output = []
        output = TopElements.get_top_k_from_file(k, input_file)

        self.assertCountEqual(expected_output, output)

    def test_4(self):
        # Partially invalid input 
        # containing empty lines and 
        # lines containing only value or index
        k = 3
        input_file = 'tests/input_test_4.txt'
        expected_output = [1426828051, 1426828066, 1426828027]
        output = TopElements.get_top_k_from_file(k, input_file)
        
        print("Note: Warnings are expected for this test case. User is warned about intentionaly provided partly corrupted input data")
        self.assertCountEqual(expected_output, output)

    def test_5(self):
        # negative k value
        # consider it then as 0 top elements (empty list) shall be returned
        k = -3
        input_file = 'tests/input_test_4.txt'
        expected_output = []
        output = TopElements.get_top_k_from_file(k, input_file)

        self.assertCountEqual(expected_output, output)

    def test_6(self):
        # not existing file
        # consider it then as 0 top elements (empty list) shall be returned
        k = 3
        input_file = 'tests/input_test_771.txt'
        expected_output = []
        output = TopElements.get_top_k_from_file(k, input_file)
        print("Note: Error is expected in console for this case. User is informed about intentionally provided not existing file")
        self.assertCountEqual(expected_output, output)