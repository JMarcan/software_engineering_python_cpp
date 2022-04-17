class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = set()
        self.users = set()

    def add_group(self, group):
        self.groups.add(group)

    def add_user(self, user):
        self.users.add(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name




def is_user_in_group(user, group):
    """
    Check whether the user belongs to the group

    Args:
      user(str): user name/id
      group(class:Group): group to check user membership against
      
    Returns:
        - True if user is in the group, False otherwise
    """
    if isinstance(group, Group) == False:
        print("[Warrning] is_user_in_group: provided group (\'{0}\') does not exists. Returning False".format(group))
        return False
        
    # check whether user is a direct member of the group
    if user in group.users:
        return True

    # check whether user is member of any sub group of the group
    for g in group.groups:
        if is_user_in_group(user, g):
            return True
        
    return False
    
def test_cases():
    """
    Execute test cases for active directory implementation
    Print statements whether the test case passed or not are printed
    
    Args:
      None

    Returns:
       None
    """
    parent = Group("parent")
    child = Group("child")
    sub_child = Group("subchild")

    sub_child_user = "sub_child_user"
    sub_child.add_user(sub_child_user)

    child.add_group(sub_child)
    parent.add_group(child)
    
    # TC 1 - user is direct member of this group
    if is_user_in_group(sub_child_user, sub_child) == True:
        print ("TC 1. Passed")
    else:
        print ("TC 1. Failed")
        
     # TC 1 - user is direct member of child group
    if is_user_in_group(sub_child_user, parent) == True:
        print ("TC 2. Passed")
    else:
        print ("TC 2. Failed")
    
    # TC 2 - not existing user, existing group
    if is_user_in_group("not existing user", parent) == False:
        print ("TC 3. Passed")
    else:
        print ("TC 3. Failed")
    
    # TC 3 - not existing user group
    if is_user_in_group("not existing user", "not existing group") == False:
        print ("TC 4. Passed")
    else:
        print ("TC 4. Failed") 
    
     

if __name__ == '__main__':
    # execute test cases  
    test_cases()   