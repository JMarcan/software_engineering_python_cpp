correct = [[1,2,3],
           [2,3,1],
           [3,1,2]]

incorrect = [[1,2,3,4],
             [2,3,1,3],
             [3,1,2,3],
             [4,4,4,4]]

incorrect2 = [[1,2,3,4],
             [2,3,1,4],
             [4,1,2,3],
             [3,4,1,2]]

incorrect3 = [[1,2,3,4,5],
              [2,3,1,5,6],
              [4,5,2,1,3],
              [3,4,5,2,1],
              [5,6,4,3,2]]

incorrect4 = [['a','b','c'],
              ['b','c','a'],
              ['c','a','b']]

incorrect5 = [ [1, 1.5],
               [1.5, 1]]
               
# Define a function check_sudoku() here:

def check_sudoku(sudoku_list):
    ''' 
    Check whether provided sudoku configuration is valid sudoku:
    1. Each column of the square contains each of the whole numbers from 1 to n exactly once.
    2. Each row of the square contains each of the whole numbers from 1 to n exactly once.

    Args: 
        sudoku_list: configuration of sudoku to be checked
    
    Returns:
        True if the field fulfills the rules. False otherwise
    '''
    return check_sudoku_A(sudoku_list)
    
def check_sudoku_A(sudoku_list):
    ''' 
    Check whether provided sudoku configuration is valid sudoku:
    1. Each column of the square contains each of the whole numbers from 1 to n exactly once.
    2. Each row of the square contains each of the whole numbers from 1 to n exactly once.

    This implementation creates a list with the integers 1, 2, ..., n.
    We will check that each number in the row is in the list
    and remove the numbers from the list once they are verified
    to ensure that each number only occurs once in the row.
    
    Args: 
        sudoku_list: configuration of sudoku to be checked
    
    Returns:
        True if the field fulfills the rules. False otherwise
    '''
    for row in sudoku_list:
        # Create a list with the integers 1, 2, ..., n.
        # We will check that each number in the row is in the list
        # and remove the numbers from the list once they are verified
        # to ensure that each number only occurs once in the row.
        check_list = list(range(1, len(sudoku_list[0]) + 1))
        for i in row:
            if i not in check_list:
                return False
            check_list.remove(i)
    for n in range(len(sudoku_list[0])):
        # We do the same here for each column in the square.
        check_list = list(range(1, len(sudoku_list[0]) + 1))
        for row in sudoku_list:
            if row[n] not in check_list:
                return False
            check_list.remove(row[n])
    return True

def check_sudoku_B(sudoku_list):
    ''' 
    Check whether provided sudoku configuration is valid sudoku:
    1. Each column of the square contains each of the whole numbers from 1 to n exactly once.
    2. Each row of the square contains each of the whole numbers from 1 to n exactly once.

    This implementation counts for each number count of its occurance
    and checks that its not higher than one
    
    Args: 
        sudoku_list: configuration of sudoku to be checked
    
    Returns:
        True if the field fulfills the rules. False otherwise
    '''
    n = len(sudoku_list)
    
    # initialize nxn field indicating how many times given integer occured in each column
    numbers_occurance_colmn = [[0 for i in range(n)] for i in range(n)]
    # initialize n field indicating how many times given integer occured in a row
    numbers_occurance_row = [0 for i in range(n)]
    
    # Verify that
    #Each row of the square contains each of the whole numbers from 1 to n exactly once.
    #Each column of the square contains each of the whole numbers from 1 to n exactly once.
    for row in sudoku_list:
        # reset occurent count for a new row
        for i in range(n):
            numbers_occurance_row[i] = 0
            
        for column, item in enumerate(row):
             # check for a given value
             # whether sudoku configuration contains only digits
            if isinstance(item, int) == False:
                return False
            # check whether its an valid value
            if item  < 1 or item > n:
                return False    
            
            number_idx = item - 1
            numbers_occurance_row[number_idx] = numbers_occurance_row[number_idx] + 1
            numbers_occurance_colmn[column][number_idx] = numbers_occurance_colmn[column][number_idx] + 1

        #Each row of the square contains each of the whole numbers from 1 to n exactly once.
        if max(numbers_occurance_row) > 1:
            return False
        
        #Each column of the square contains each of the whole numbers from 1 to n exactly once.
        for i in range(n):
            if max(numbers_occurance_colmn[i]) > 1:
                return False
            
    return True
    
print(check_sudoku(incorrect))
#>>> False

print(check_sudoku(correct))
#>>> True

print(check_sudoku(incorrect2))
#>>> False

print(check_sudoku(incorrect3))
#>>> False

print(check_sudoku(incorrect4))
#>>> False

print(check_sudoku(incorrect5))
#>>> False



