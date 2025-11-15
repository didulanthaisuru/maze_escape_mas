# environment/maze.py

import random
from environment.cell import Cell

class Maze:
    """Maze environment for the simulation"""
    
    def __init__(self, width, height, wall_density=0.3):
        self.width = width
        self.height = height
        self.wall_density = wall_density
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.start_pos = None
        self.exit_pos = None
        
    def generate(self):
        """Generate a solvable maze"""
        # Clear the maze
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].is_wall = False
        
        # Add random walls
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < self.wall_density:
                    self.grid[x][y].is_wall = True
        
        # Set start position (top-left area)
        self.start_pos = (1, 1)
        self.grid[1][1].is_wall = False
        self.grid[1][1].is_start = True
        
        # Set exit position (bottom-right area)
        self.exit_pos = (self.width - 2, self.height - 2)
        self.grid[self.width - 2][self.height - 2].is_wall = False
        self.grid[self.width - 2][self.height - 2].is_exit = True
        
        # Ensure path exists from start to exit
        self._ensure_path()
        
        # Add borders
        for x in range(self.width):
            self.grid[x][0].is_wall = True
            self.grid[x][self.height - 1].is_wall = True
        for y in range(self.height):
            self.grid[0][y].is_wall = True
            self.grid[self.width - 1][y].is_wall = True
    
    def _ensure_path(self):
        """Use BFS to ensure a path exists, carving one if needed"""
        from collections import deque
        
        visited = set()
        queue = deque([self.start_pos])
        parent = {self.start_pos: None}
        
        while queue:
            x, y = queue.popleft()
            
            if (x, y) == self.exit_pos:
                # Path exists
                return
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    not self.grid[nx][ny].is_wall and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    parent[(nx, ny)] = (x, y)
        
        # No path found, carve one
        self._carve_path()
    
    def _carve_path(self):
        """Carve a guaranteed path from start to exit"""
        x, y = self.start_pos
        ex, ey = self.exit_pos
        
        # Simple path carving: move right then down
        while x < ex:
            self.grid[x][y].is_wall = False
            x += 1
        while y < ey:
            self.grid[x][y].is_wall = False
            y += 1
        self.grid[ex][ey].is_wall = False
    
    def get_neighbors(self, x, y):
        """Get valid neighboring cells (not walls)"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height and
                not self.grid[nx][ny].is_wall):
                neighbors.append((nx, ny))
        return neighbors
    
    def get_cell(self, x, y):
        """Get cell at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None
    
    def mark_dead_end(self, x, y):
        """Mark a position as a dead end"""
        cell = self.get_cell(x, y)
        if cell:
            cell.is_dead_end = True