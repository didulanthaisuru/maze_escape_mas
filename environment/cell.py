# Cell class for maze grid

class Cell:
    """
    Cell class representing a single cell in the maze grid
    """
    
    def __init__(self, x, y):
        """
        Initialize a cell with coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        
    def remove_wall(self, direction):
        """
        Remove wall in specified direction
        
        Args:
            direction: Direction of wall to remove ('top', 'right', 'bottom', 'left')
        """
        if direction in self.walls:
            self.walls[direction] = False
    
    def has_wall(self, direction):
        """
        Check if cell has a wall in specified direction
        """
        return self.walls.get(direction, True)
