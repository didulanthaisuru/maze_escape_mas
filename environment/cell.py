# environment/cell.py

class Cell:
    """Represents a single cell in the maze grid"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_wall = False
        self.is_start = False
        self.is_exit = False
        self.visited = False
        self.is_dead_end = False
        self.explored_by = set()  # Set of agent IDs that have explored this cell
        
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
    
    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def reset_exploration(self):
        """Reset exploration status"""
        self.visited = False
        self.explored_by.clear()