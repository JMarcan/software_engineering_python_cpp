import os

def find_files(suffix, path):
    """
    Find all files beneath path with file name suffix.

    Note that a path may contain further subdirectories
    and those subdirectories may also contain further subdirectories.

    There are no limit to the depth of the subdirectories can be.

    Args:
      suffix(str): suffix if the file name to be found
      path(str): path of the file system

    Returns:
       a list of paths
    """
    if not os.path.isdir(path):
        print("[Warrning] find_files: provided path (\'{0}\') is not valid. Returning empty list".format(path))
        return []
    
    if len(suffix) == 0 or suffix.isnumeric():
        print("[Warrning] find_files: provided suffix (\'{0}\') is not valid".format(suffix))
        return []
    
    files_list = []
    for file in os.listdir(path):
        if os.path.isfile(path + file): 
            if file.endswith(suffix):
                files_list.append(path + file)
        else: # in case of folder apply recursion
            files_list += find_files(suffix, path + file + "/")
    
    return files_list

def test_cases(path):
    """
    Execute test cases for function find_files(suffix, path) in a provided path
    Print statements whether the test case passed or not are printed
    
    Args:
      path(str): path of the folder in file system

    Returns:
       None
    """
    
    # TC 1 - find .c files
    expected_c_files = ['Problem_2_testdir/subdir1/a.c', 'Problem_2_testdir/subdir3/subsubdir1/b.c', 'Problem_2_testdir/subdir5/a.c', 'Problem_2_testdir/t1.c']
    if find_files(".c", path) == expected_c_files: # returns 1
        print ("TC 1. Passed")
    else: 
        print ("TC 1. Failed")
    
    # TC 2 - find .h files
    expected_h_files = ['Problem_2_testdir/subdir1/a.h', 'Problem_2_testdir/subdir3/subsubdir1/b.h', 'Problem_2_testdir/subdir5/a.h', 'Problem_2_testdir/t1.h']
    if find_files(".h", path) == expected_h_files: # returns 1
        print ("TC 2. Passed")
    else: 
        print ("TC 2. Failed")
        
    # TC 3 - deal with not existing path provided    
    if find_files(".h", "not_existing_path") == []:
        print ("TC 3. Passed")
    else: 
        print ("TC 3. Failed")
        
    
    # TC 4 - with empty extension 
    if find_files("", path) == []:
        print ("TC 4. Passed")
    else: 
        print ("TC 4. Failed")
        


if __name__ == '__main__':
    # execute test cases  
    path = "Problem_2_testdir/"
    test_cases(path)    

