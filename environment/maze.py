# environment/maze.py

import random
from environment.cell import Cell

class Maze:
    """Maze environment for the simulation"""
    
    def __init__(self, width, height, wall_density=0.3, use_fixed_maze=True):
        self.width = width
        self.height = height
        self.wall_density = wall_density
        self.use_fixed_maze = use_fixed_maze
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.start_pos = None
        self.exit_pos = None
        self.correct_path_cells = set()  # Store correct path cells to avoid placing dead ends on them
        
    def generate(self):
        """Generate a solvable maze"""
        if self.use_fixed_maze:
            self._generate_fixed_maze()
        else:
            self._generate_random_maze()
    
    def _generate_fixed_maze(self):
        """Generate a PROPER COMPLEX maze with dense walls, corridors, and challenges"""
        # Start with ALL WALLS
        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].is_wall = True
                self.grid[x][y].is_trap = False
        
        # Keep only border as walls
        for x in range(self.width):
            self.grid[x][0].is_wall = True
            self.grid[x][self.height - 1].is_wall = True
        for y in range(self.height):
            self.grid[0][y].is_wall = True
            self.grid[self.width - 1][y].is_wall = True
        
        # Set start and exit positions
        self.start_pos = (2, 2)
        self.exit_pos = (self.width - 3, self.height - 3)
        
        # Create a DENSE maze using recursive backtracking-like pattern
        self._carve_maze_passages()
        
        # Add strategic walls to create more complexity
        self._add_maze_walls()
        
        # FIRST: Ensure solvable path exists and mark it
        self._ensure_solvable_path()
        
        # THEN: Create dead ends AWAY from the correct path
        self._create_dead_end_corridors()
        
        # Verify: Check that no dead ends are on the correct path (silent check)
        # Create trap chambers AWAY from correct path
        self._create_trap_zones()
        
        # Add some open rooms for variety
        self._create_rooms()
        
        # Ensure start and exit are accessible
        self.grid[self.start_pos[0]][self.start_pos[1]].is_wall = False
        self.grid[self.start_pos[0]][self.start_pos[1]].is_start = True
        self.grid[self.exit_pos[0]][self.exit_pos[1]].is_wall = False
        self.grid[self.exit_pos[0]][self.exit_pos[1]].is_exit = True
    
    def _carve_maze_passages(self):
        """Carve passages through the walls to create a maze"""
        # Create a grid-based maze with corridors
        
        # Horizontal corridors
        for y in range(2, self.height - 2, 3):
            for x in range(2, self.width - 2):
                self.grid[x][y].is_wall = False
        
        # Vertical corridors
        for x in range(2, self.width - 2, 3):
            for y in range(2, self.height - 2):
                self.grid[x][y].is_wall = False
        
        # Add diagonal passages for complexity
        for i in range(5, min(self.width - 5, self.height - 5), 6):
            for j in range(-2, 3):
                x, y = i + j, i + j
                if 2 < x < self.width - 2 and 2 < y < self.height - 2:
                    self.grid[x][y].is_wall = False
        
        # Add some random passages to connect areas
        for _ in range(40):
            x = random.randint(3, self.width - 4)
            y = random.randint(3, self.height - 4)
            if not self.grid[x][y].is_start and not self.grid[x][y].is_exit:
                self.grid[x][y].is_wall = False
    
    def _add_maze_walls(self):
        """Add walls to create more turns and complexity"""
        # Add strategic wall blocks
        wall_patterns = [
            # L-shaped walls
            [(0, 0), (1, 0), (0, 1)],
            [(0, 0), (-1, 0), (0, 1)],
            [(0, 0), (1, 0), (0, -1)],
            [(0, 0), (-1, 0), (0, -1)],
            # T-shaped walls
            [(0, 0), (1, 0), (-1, 0), (0, 1)],
            [(0, 0), (1, 0), (-1, 0), (0, -1)],
            # Plus signs
            [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)],
        ]
        
        # Place wall patterns randomly
        for _ in range(30):
            cx = random.randint(5, self.width - 6)
            cy = random.randint(5, self.height - 6)
            pattern = random.choice(wall_patterns)
            
            # Place the pattern
            for dx, dy in pattern:
                x, y = cx + dx, cy + dy
                if (3 < x < self.width - 3 and 3 < y < self.height - 3 and
                    not self.grid[x][y].is_start and not self.grid[x][y].is_exit):
                    self.grid[x][y].is_wall = True
        
        # Add some long wall segments to create corridors
        for _ in range(15):
            if random.random() < 0.5:
                # Horizontal wall
                sx = random.randint(4, self.width - 10)
                sy = random.randint(4, self.height - 4)
                length = random.randint(5, 10)
                for i in range(length):
                    x = sx + i
                    if (3 < x < self.width - 3 and
                        not self.grid[x][sy].is_start and not self.grid[x][sy].is_exit):
                        self.grid[x][sy].is_wall = True
            else:
                # Vertical wall
                sx = random.randint(4, self.width - 4)
                sy = random.randint(4, self.height - 10)
                length = random.randint(5, 10)
                for i in range(length):
                    y = sy + i
                    if (3 < y < self.height - 3 and
                        not self.grid[sx][y].is_start and not self.grid[sx][y].is_exit):
                        self.grid[sx][y].is_wall = True
    
    def _create_rooms(self):
        """Create some open rooms for variety"""
        room_positions = [
            (8, 8, 4, 4), (20, 10, 5, 4), (15, 20, 4, 5),
            (10, 15, 3, 3), (22, 22, 4, 4), (5, 18, 3, 3)
        ]
        
        for rx, ry, rw, rh in room_positions:
            if rx + rw < self.width - 2 and ry + rh < self.height - 2:
                # Clear room interior
                for x in range(rx, rx + rw):
                    for y in range(ry, ry + rh):
                        if (2 < x < self.width - 2 and 2 < y < self.height - 2 and
                            not self.grid[x][y].is_start and not self.grid[x][y].is_exit):
                            self.grid[x][y].is_wall = False
                
                # Add 2-3 doorways
                num_doors = random.randint(2, 3)
                for _ in range(num_doors):
                    side = random.choice(['top', 'bottom', 'left', 'right'])
                    if side == 'top' and ry > 2:
                        dx = random.randint(0, rw - 1)
                        self.grid[rx + dx][ry - 1].is_wall = False
                    elif side == 'bottom' and ry + rh < self.height - 2:
                        dx = random.randint(0, rw - 1)
                        self.grid[rx + dx][ry + rh].is_wall = False
                    elif side == 'left' and rx > 2:
                        dy = random.randint(0, rh - 1)
                        self.grid[rx - 1][ry + dy].is_wall = False
                    elif side == 'right' and rx + rw < self.width - 2:
                        dy = random.randint(0, rh - 1)
                        self.grid[rx + rw][ry + dy].is_wall = False
    
    def _create_dead_end_corridors(self):
        """Create TRUE dead ends - single cells where if you step in, you CANNOT move (even back)"""
        # These are trap cells - once you're there, you're completely stuck
        # IMPORTANT: Never place dead ends on the correct solution path!
        dead_end_positions = [
            (5, 5), (8, 3), (12, 6), (18, 4), (22, 8),
            (6, 12), (10, 15), (15, 18), (20, 14), (25, 20),
            (7, 20), (14, 10), (19, 22), (11, 25), (24, 12),
            (16, 8), (9, 18), (21, 16), (13, 23), (26, 6),
            (17, 11), (23, 19), (8, 24), (19, 7)
        ]
        
        for dx, dy in dead_end_positions:
            if dx >= self.width - 3 or dy >= self.height - 3:
                continue
            
            # CRITICAL: Skip if this cell is on the correct solution path
            if (dx, dy) in self.correct_path_cells:
                continue
            
            # Make sure this cell is a path (not wall)
            if (2 < dx < self.width - 2 and 2 < dy < self.height - 2 and
                not self.grid[dx][dy].is_start and not self.grid[dx][dy].is_exit):
                
                # Clear the cell itself
                self.grid[dx][dy].is_wall = False
                
                # Mark as DEAD END - true trap
                self.grid[dx][dy].is_dead_end = True
                self.grid[dx][dy].is_trap = True
                
                # Make sure it has at least one entrance (so agents can enter)
                # But once inside, they CANNOT leave (we'll handle this in agent logic)
                # Create one path leading TO this dead end
                entrance_dir = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                entrance_x = dx + entrance_dir[0]
                entrance_y = dy + entrance_dir[1]
                
                if 2 < entrance_x < self.width - 2 and 2 < entrance_y < self.height - 2:
                    # Also make sure entrance is not on correct path
                    if (entrance_x, entrance_y) not in self.correct_path_cells:
                        self.grid[entrance_x][entrance_y].is_wall = False
    
    def _create_trap_zones(self):
        """Create wrong path zones - you can explore and backtrack, but they don't lead to exit"""
        # These are NOT dead ends - agents can move around and escape
        # But they waste time because they don't lead anywhere useful
        # IMPORTANT: Avoid placing trap zones on the correct solution path!
        trap_centers = [
            (8, 8), (20, 10), (15, 20), (25, 15), (10, 25),
            (18, 25), (12, 12), (22, 22), (5, 18), (27, 7)
        ]
        
        for tx, ty in trap_centers:
            if tx >= self.width - 4 or ty >= self.height - 4:
                continue
            
            # Skip if trap center is on correct path
            if (tx, ty) in self.correct_path_cells:
                continue
            
            # Create a small area with paths (wrong path zone)
            zone_size = random.choice([3, 4])
            offset = zone_size // 2
            
            # Clear some paths in this zone
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    x, y = tx + dx, ty + dy
                    
                    # Skip if on correct path
                    if (x, y) in self.correct_path_cells:
                        continue
                    
                    if (2 < x < self.width - 2 and 2 < y < self.height - 2 and
                        not self.grid[x][y].is_start and not self.grid[x][y].is_exit):
                        # Make it a path, but it's a "wrong path" area
                        self.grid[x][y].is_wall = False
                        # Don't mark as trap - agents can move freely here
            
            # Add some internal walls to make it maze-like
            for _ in range(3):
                wx = tx + random.randint(-offset, offset)
                wy = ty + random.randint(-offset, offset)
                
                # Skip if on correct path
                if (wx, wy) in self.correct_path_cells:
                    continue
                
                if (2 < wx < self.width - 2 and 2 < wy < self.height - 2 and
                    not self.grid[wx][wy].is_start and not self.grid[wx][wy].is_exit):
                    self.grid[wx][wy].is_wall = True
            
            # Create entrance
            entrance_side = random.choice(['top', 'bottom', 'left', 'right'])
            if entrance_side == 'top' and ty - offset - 1 > 1:
                for step in range(2):
                    ey = ty - offset - 1 - step
                    if 2 < tx < self.width - 2 and 1 < ey < self.height - 1:
                        self.grid[tx][ey].is_wall = False
            elif entrance_side == 'bottom' and ty + offset + 1 < self.height - 1:
                for step in range(2):
                    ey = ty + offset + 1 + step
                    if 2 < tx < self.width - 2 and 1 < ey < self.height - 1:
                        self.grid[tx][ey].is_wall = False
            elif entrance_side == 'left' and tx - offset - 1 > 1:
                for step in range(2):
                    ex = tx - offset - 1 - step
                    if 1 < ex < self.width - 1 and 2 < ty < self.height - 2:
                        self.grid[ex][ty].is_wall = False
            elif entrance_side == 'right' and tx + offset + 1 < self.width - 1:
                for step in range(2):
                    ex = tx + offset + 1 + step
                    if 1 < ex < self.width - 1 and 2 < ty < self.height - 2:
                        self.grid[ex][ty].is_wall = False
    
    
    def _ensure_solvable_path(self):
        """Ensure there's a path from start to exit, creating one if needed"""
        # Clear immediate area around start
        sx, sy = self.start_pos
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x, y = sx + dx, sy + dy
                if 1 < x < self.width - 1 and 1 < y < self.height - 1:
                    self.grid[x][y].is_wall = False
                    self.grid[x][y].is_trap = False
                    self.grid[x][y].is_dead_end = False
        
        # Clear immediate area around exit
        ex, ey = self.exit_pos
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x, y = ex + dx, ey + dy
                if 1 < x < self.width - 1 and 1 < y < self.height - 1:
                    self.grid[x][y].is_wall = False
                    self.grid[x][y].is_trap = False
                    self.grid[x][y].is_dead_end = False
        
        # Find the correct path using BFS and store it
        correct_path = self._find_path_bfs()
        
        if not correct_path:
            # No path found - create one!
            self._create_guaranteed_path()
            # Find it again
            correct_path = self._find_path_bfs()
        
        # Mark all cells on the correct path as safe (no dead ends allowed)
        if correct_path:
            self.correct_path_cells = set(correct_path)
            for x, y in correct_path:
                self.grid[x][y].is_wall = False
                self.grid[x][y].is_dead_end = False
                self.grid[x][y].is_trap = False
        else:
            # Fallback - use simple guaranteed path
            self.correct_path_cells = set()
            x, y = sx, sy
            while x < ex:
                self.grid[x][y].is_wall = False
                self.grid[x][y].is_dead_end = False
                self.grid[x][y].is_trap = False
                self.correct_path_cells.add((x, y))
                x += 1
            while y < ey:
                self.grid[x][y].is_wall = False
                self.grid[x][y].is_dead_end = False
                self.grid[x][y].is_trap = False
                self.correct_path_cells.add((x, y))
                y += 1
            self.grid[ex][ey].is_wall = False
            self.grid[ex][ey].is_dead_end = False
            self.grid[ex][ey].is_trap = False
            self.correct_path_cells.add((ex, ey))
    
    def _find_path_bfs(self):
        """Use BFS to find a path from start to exit and return the path"""
        from collections import deque
        
        visited = set()
        queue = deque([(self.start_pos, [self.start_pos])])
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == self.exit_pos:
                return path
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    not self.grid[nx][ny].is_wall and (nx, ny) not in visited):
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return None
    
    def _generate_random_maze(self):
        """Generate a random solvable maze (original method)"""
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
    
    
    def _path_exists(self):
        """Check if a path exists from start to exit using BFS"""
        from collections import deque
        
        visited = set()
        queue = deque([self.start_pos])
        
        while queue:
            x, y = queue.popleft()
            
            if (x, y) == self.exit_pos:
                return True
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    not self.grid[nx][ny].is_wall and (nx, ny) not in visited):
                    queue.append((nx, ny))
        
        return False
    
    def _create_guaranteed_path(self):
        """Create a guaranteed winding path from start to exit"""
        sx, sy = self.start_pos
        ex, ey = self.exit_pos
        
        x, y = sx, sy
        
        # Create a winding path that avoids being too simple
        # Go right in steps
        while x < ex - 5:
            for _ in range(3):
                if x < ex:
                    self.grid[x][y].is_wall = False
                    self.grid[x][y].is_dead_end = False
                    self.grid[x][y].is_trap = False
                    x += 1
            # Go down a bit
            if y < ey:
                self.grid[x][y].is_wall = False
                self.grid[x][y].is_dead_end = False
                self.grid[x][y].is_trap = False
                y += 1
        
        # Complete the path to exit
        while x < ex:
            self.grid[x][y].is_wall = False
            self.grid[x][y].is_dead_end = False
            self.grid[x][y].is_trap = False
            x += 1
        
        while y < ey:
            self.grid[x][y].is_wall = False
            self.grid[x][y].is_dead_end = False
            self.grid[x][y].is_trap = False
            y += 1
        
        # Ensure exit is reachable
        self.grid[ex][ey].is_wall = False
        self.grid[ex][ey].is_dead_end = False
        self.grid[ex][ey].is_trap = False
        
        # Clear a bit around the path for easier navigation
        x, y = sx, sy
        while x <= ex:
            # Clear one cell above and below the path
            if y > 1:
                self.grid[x][y-1].is_wall = False
                self.grid[x][y-1].is_dead_end = False
            if y < self.height - 2:
                self.grid[x][y+1].is_wall = False
                self.grid[x][y+1].is_dead_end = False
            x += 1
            if y < ey:
                y += 1
    
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