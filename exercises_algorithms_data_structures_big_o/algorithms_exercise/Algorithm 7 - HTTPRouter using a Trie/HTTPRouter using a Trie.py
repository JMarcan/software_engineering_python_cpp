# A RouteTrie will store our routes and their associated handlers
class RouteTrie:
    def __init__(self, root_handler, not_found_handler):
        # Initialize the trie with an root node and a handler, this is the root path or home page node
        self.root = RouteTrieNode(root_handler)
        self.not_found_handler = not_found_handler
        
    def insert(self, path, handler):
        # Start at the root
        node = self.root

        # Iterate provided path
        for p in path.split('/'):
            # Filter out empty blocks
            if p:
                node.insert(p, self.not_found_handler)
                node = node.children[p]
        
        node.handler = handler
        
    def find(self, path):
        # Starting at the root, navigate the Trie to find a match for this path
        # Return the handler for a match, or None for no match

        node = self.root

        # Traverse Trie
        for p in path.split('/'):
            if p:
                if p in node.children.keys():
                    node = node.children[p]
                else:
                    return self.not_found_handler
        
        # Return handler if traversed to the end
        return node.handler
    
# A RouteTrieNode will be similar to our autocomplete TrieNode... with one additional element, a handler.
class RouteTrieNode:
    def __init__(self, handler):
        # Initialize the node with children as before, plus a handler
        self.children = {}
        self.handler = handler
        
    def insert(self, path, handler):
        # Insert the node as before
        self.children[path] = RouteTrieNode(handler)
        
# The Router class will wrap the Trie and handle 
class Router:
    def __init__(self, root_handler, not_found_handler):
        # Create a new RouteTrie for holding our routes
        # You could also add a handler for 404 page not found responses as well!
        self.trie = RouteTrie(root_handler, not_found_handler)
        
    def add_handler(self, path, handler):
        # Add a handler for a path
        self.trie.insert(path, handler)

    def lookup(self, path):
        # lookup path (by parts) and return the associated handler
        return self.trie.find(path)
        
# create the router and add a route
router = Router("root handler", "not found handler") # remove the 'not found handler' if you did not implement this
router.add_handler("/home/about", "about handler")  # add a route

# some lookups with the expected output
print(router.lookup("/")) # should print 'root handler'
print(router.lookup("/home")) # should print 'not found handler' or None if you did not implement one
print(router.lookup("/home/about")) # should print 'about handler'
print(router.lookup("/home/about/")) # should print 'about handler' or None if you did not handle trailing slashes
print(router.lookup("/home/about/me")) # should print 'not found handler' or None if you did not implement one