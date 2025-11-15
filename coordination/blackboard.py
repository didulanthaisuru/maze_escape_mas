# Shared knowledge base (Blackboard pattern)

class Blackboard:
    """
    Blackboard system for shared knowledge among agents
    """
    
    def __init__(self):
        """
        Initialize the blackboard
        """
        self.shared_knowledge = {}
        self.explored_cells = set()
        self.obstacles = set()
        
    def update_knowledge(self, key, value):
        """
        Update shared knowledge
        
        Args:
            key: Knowledge key
            value: Knowledge value
        """
        self.shared_knowledge[key] = value
    
    def get_knowledge(self, key):
        """
        Retrieve knowledge by key
        
        Args:
            key: Knowledge key
        """
        return self.shared_knowledge.get(key)
    
    def mark_explored(self, position):
        """
        Mark a cell as explored
        
        Args:
            position: (x, y) position of the cell
        """
        self.explored_cells.add(position)
    
    def is_explored(self, position):
        """
        Check if a cell has been explored
        
        Args:
            position: (x, y) position of the cell
        """
        return position in self.explored_cells
