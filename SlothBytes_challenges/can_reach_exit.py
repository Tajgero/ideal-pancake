class Node():
    """Data object"""
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        
    def __repr__(self):
        return f"{self.state} ->"


class QueueFrontier():
    """For BFS search"""
    def __init__(self):
        self.frontier = []
        
    def __repr__(self):
        return f"{self.frontier}"
    
    def __len__(self):
        return len(self.frontier)
    
    def __getitem__(self, idx):
        return self.frontier[idx]

    def add(self, node):
        self.frontier.append(node)
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
        
    def empty(self):
        return len(self.frontier) == 0
        
    def remove(self):
        if self.empty():
            raise Exception("Frontier not empty")
        
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node
        
   
def neighbors(path, state):
    """Returns neighboring cells for valid moves in path and check for exit"""
    neighbors = set()
    i, j = state
    
    max_row = len(path)
    max_col = len(path[0])
    
    moves = {
        "up" : (i - 1, j),
        "down" : (i + 1, j),
        "left" : (i, j - 1),
        "right" : (i, j + 1)
    }
    
    for move in moves.values():
        row, col = move
        if 0 <= row < max_row and 0 <= col < max_col:
            if path[row][col] != '#':
                neighbors.add(move)
    
    return neighbors
    

def can_reach_exit(path: list):
    """
    This function check if there is exit and outputs its path
    
    Args:
        path (list) : List of path defined by symbols
                      '.' - empty space (you can walk here)
                      '#' - wall (you cannot walk here)
                      '@' - starting position
                      'E' - exit
    Returns:
        output (bool) : Returns True if exit can be reach and False otherwise
    """
    # Finds starting positions
    start, end = None, None
    for row in range(len(path)):
        for col in range(len(path[0])):
            pos = (row, col)
            if path[row][col] == '@': 
                start = pos
            elif path[row][col] == 'E': 
                end = pos
            
    if start is None or end is None:
        raise Exception("There is no exit or start point")
        
    # Explores possible states
    frontier = QueueFrontier()
    frontier.add(Node(state=start, parent=None))
    explored = set()
    
    while not frontier.empty():
        node = frontier.remove()
        explored.add(node.state)
        
        for state in neighbors(path, node.state):
            if state not in explored and not frontier.contains_state(state):
                child = Node(state=state, parent=node)
                
                if child.state == end:
                    solution = []
                    node = child
                    while node.parent is not None:
                        solution.append(node)
                        node = node.parent
                    solution.append(Node(state=start, parent=None))
                    solution.reverse()
                    solution.append("End reached!")
                    print("Solution:\n", solution)
                    return True
                
                frontier.add(child)
    return False
                

if __name__ == '__main__':
    path1 = [
    "@..",
    ".#E",
    "..."
    ]
    
    path2 = [
    "@.#.",
    "..#E",
    "####"
    ]
    
    path3 = [
    "@...",
    ".###",
    "...E"
    ]
    
    path4 = [
    "###",
    "#@#",
    "##E"        
    ]
    
    assert can_reach_exit(path1) == True
    assert can_reach_exit(path2) == False
    assert can_reach_exit(path3) == True
    assert can_reach_exit(path4) == False
    print("All tests passed!")
