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
        
        # CRITICAL ORDER CHANGE: Create winding path FIRST before anything else
        self._create_complex_winding_path()
        
        # Create a DENSE maze using recursive backtracking-like pattern
        self._carve_maze_passages()
        
        # BLOCK all direct shortcuts with walls
        self._block_direct_paths()
        
        # Add strategic walls to create more complexity
        self._add_maze_walls()
        
        # Verify path still exists (should be the winding one we created)
        self._verify_path_exists()
        
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
        
        # IMPORTANT: Analyze and mark all actual dead ends in addition to manually created ones
        self._identify_all_dead_ends()
    
    def _carve_maze_passages(self):
        """Carve passages through the walls to create a DENSE maze with narrow corridors"""
        # Use recursive backtracking to create maze-like passages
        # This creates a more organic, less grid-like structure
        
        visited = set()
        stack = []
        
        # Start from a random internal point
        start_x = random.randint(3, self.width - 4)
        start_y = random.randint(3, self.height - 4)
        stack.append((start_x, start_y))
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        # Carve passages using recursive backtracking
        while stack:
            x, y = stack[-1]
            self.grid[x][y].is_wall = False
            visited.add((x, y))
            
            # Find unvisited neighbors
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (2 < nx < self.width - 2 and 2 < ny < self.height - 2 and
                    (nx, ny) not in visited):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # Choose random neighbor
                nx, ny, dx, dy = random.choice(neighbors)
                # Carve path to neighbor
                self.grid[x + dx // 2][y + dy // 2].is_wall = False
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Add MANY MORE random connections to create multiple paths and loops
        for _ in range(100):  # Increased from 30 to 100 for MUCH more open maze
            x = random.randint(3, self.width - 4)
            y = random.randint(3, self.height - 4)
            if not self.grid[x][y].is_start and not self.grid[x][y].is_exit:
                self.grid[x][y].is_wall = False
                # Also carve adjacent cell to create passage
                direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                nx, ny = x + direction[0], y + direction[1]
                if 2 < nx < self.width - 2 and 2 < ny < self.height - 2:
                    self.grid[nx][ny].is_wall = False
    
    def _create_complex_winding_path(self):
        """Create the MAIN winding path FIRST - this is the solution path"""
        sx, sy = self.start_pos
        ex, ey = self.exit_pos
        
        x, y = sx, sy
        path_cells = [(x, y)]
        
        # Create a snake-like winding path with many turns
        # Use a pattern: right, down, right, down, with some up/left variations
        direction = 'right'
        turn_counter = 0
        
        while x != ex or y != ey:
            moved = False
            
            if direction == 'right' and x < ex:
                # Move right for several steps
                steps = random.randint(4, 8)
                for _ in range(steps):
                    if x < ex:
                        self.grid[x][y].is_wall = False
                        path_cells.append((x, y))
                        x += 1
                        moved = True
                turn_counter += 1
                # Next direction - alternate between down and up
                if y < ey:
                    direction = 'down'
                elif y > ey:
                    direction = 'up'
                else:
                    direction = 'right'
                    
            elif direction == 'down' and y < ey:
                # Move down for several steps
                steps = random.randint(4, 8)
                for _ in range(steps):
                    if y < ey:
                        self.grid[x][y].is_wall = False
                        path_cells.append((x, y))
                        y += 1
                        moved = True
                turn_counter += 1
                # Sometimes go left to create zigzag
                if turn_counter % 3 == 0 and x > sx + 5:
                    direction = 'left'
                else:
                    direction = 'right'
                    
            elif direction == 'left' and x > sx + 3:
                # Move left to create zigzag
                steps = random.randint(3, 5)
                for _ in range(steps):
                    if x > sx + 3:
                        self.grid[x][y].is_wall = False
                        path_cells.append((x, y))
                        x -= 1
                        moved = True
                turn_counter += 1
                direction = 'down' if y < ey else 'right'
                
            elif direction == 'up' and y > sy + 3:
                # Move up occasionally
                steps = random.randint(2, 4)
                for _ in range(steps):
                    if y > sy + 3:
                        self.grid[x][y].is_wall = False
                        path_cells.append((x, y))
                        y -= 1
                        moved = True
                turn_counter += 1
                direction = 'right'
            
            # Safety: if stuck, move directly to goal
            if not moved:
                if x < ex:
                    self.grid[x][y].is_wall = False
                    path_cells.append((x, y))
                    x += 1
                elif y < ey:
                    self.grid[x][y].is_wall = False
                    path_cells.append((x, y))
                    y += 1
                elif x > ex:
                    self.grid[x][y].is_wall = False
                    path_cells.append((x, y))
                    x -= 1
                elif y > ey:
                    self.grid[x][y].is_wall = False
                    path_cells.append((x, y))
                    y -= 1
                else:
                    break
        
        # Mark exit
        self.grid[ex][ey].is_wall = False
        path_cells.append((ex, ey))
        
        # Store the correct path
        self.correct_path_cells = set(path_cells)
        
        # DON'T widen the path - keep it single cell width so it's hidden in the maze
        # Only ensure cells are passable, don't create obvious corridors
    
    def _block_direct_paths(self):
        """Block SOME direct shortcuts - but not too obviously"""
        sx, sy = self.start_pos
        ex, ey = self.exit_pos
        
        # Only block a few strategic diagonal shortcuts, not all of them
        for i in range(sx + 5, ex - 5, 3):  # Every 3rd cell, not every cell
            for j in range(sy + 5, ey - 5, 3):
                # If this is on the diagonal, and NOT on our winding path
                if abs(i - sx - (j - sy)) < 2 and (i, j) not in self.correct_path_cells:
                    if random.random() < 0.6:  # Only 60% chance to block
                        self.grid[i][j].is_wall = True
        
        # Add some strategic walls but not complete blocks
        # This makes the correct path less obvious without creating clear barriers
    
    def _verify_path_exists(self):
        """Verify the winding path is still intact"""
        # Quick BFS check
        from collections import deque
        visited = set()
        queue = deque([self.start_pos])
        
        while queue:
            pos = queue.popleft()
            if pos == self.exit_pos:
                return True  # Path exists
            if pos in visited:
                continue
            visited.add(pos)
            
            x, y = pos
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    not self.grid[nx][ny].is_wall and (nx, ny) not in visited):
                    queue.append((nx, ny))
        
        # If no path, clear the winding path again
        for px, py in self.correct_path_cells:
            self.grid[px][py].is_wall = False
        
        return False
    
    def _add_maze_walls(self):
        """Add MINIMAL walls - make maze navigable but still interesting"""
        # Add strategic wall blocks - but MUCH less aggressive
        wall_patterns = [
            # Simple L-shapes only
            [(0, 0), (1, 0), (0, 1)],
            [(0, 0), (-1, 0), (0, 1)],
            [(0, 0), (1, 0), (0, -1)],
            [(0, 0), (-1, 0), (0, -1)],
        ]
        
        # Place FEWER wall patterns - maze should be mostly open
        for _ in range(10):  # Reduced from 30 to 10
            cx = random.randint(5, self.width - 6)
            cy = random.randint(5, self.height - 6)
            pattern = random.choice(wall_patterns)
            
            # Place the pattern - but DON'T block the winding path
            for dx, dy in pattern:
                x, y = cx + dx, cy + dy
                if (3 < x < self.width - 3 and 3 < y < self.height - 3 and
                    not self.grid[x][y].is_start and not self.grid[x][y].is_exit and
                    (x, y) not in self.correct_path_cells):  # DON'T block winding path
                    self.grid[x][y].is_wall = True
        
        # Add FEWER long wall segments 
        for _ in range(5):  # Reduced from 15 to 5
            if random.random() < 0.5:
                # Horizontal wall
                sx = random.randint(4, self.width - 15)
                sy = random.randint(4, self.height - 4)
                length = random.randint(3, 5)  # Shorter walls
                for i in range(length):
                    x = sx + i
                    if (3 < x < self.width - 3 and
                        not self.grid[x][sy].is_start and not self.grid[x][sy].is_exit and
                        (x, sy) not in self.correct_path_cells):  # DON'T block winding path
                        self.grid[x][sy].is_wall = True
            else:
                # Vertical wall
                sx = random.randint(4, self.width - 4)
                sy = random.randint(4, self.height - 15)
                length = random.randint(3, 5)  # Shorter walls
                for i in range(length):
                    y = sy + i
                    if (3 < y < self.height - 3 and
                        not self.grid[sx][y].is_start and not self.grid[sx][y].is_exit and
                        (sx, y) not in self.correct_path_cells):  # DON'T block winding path
                        self.grid[sx][y].is_wall = True
        
        # NO random walls - keep it open
        # Agents need to be able to navigate!
    
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
        
        # Scale dead ends based on maze size
        # 30x30 maze had 24 dead ends, 50x50 should have ~40-45
        num_dead_ends = int((self.width * self.height) / 40)  # ~22 for 30x30, ~62 for 50x50
        # Cap it at reasonable amount
        num_dead_ends = min(num_dead_ends, 45)
        
        # Generate random positions for dead ends
        dead_end_positions = []
        attempts = 0
        max_attempts = num_dead_ends * 10
        
        while len(dead_end_positions) < num_dead_ends and attempts < max_attempts:
            attempts += 1
            dx = random.randint(5, self.width - 6)
            dy = random.randint(5, self.height - 6)
            
            # Skip if on correct path
            if (dx, dy) in self.correct_path_cells:
                continue
            
            # Skip if too close to start or exit
            if (abs(dx - self.start_pos[0]) < 5 and abs(dy - self.start_pos[1]) < 5):
                continue
            if (abs(dx - self.exit_pos[0]) < 5 and abs(dy - self.exit_pos[1]) < 5):
                continue
            
            # Skip if already have dead end nearby
            too_close = False
            for ex, ey in dead_end_positions:
                if abs(dx - ex) < 4 and abs(dy - ey) < 4:
                    too_close = True
                    break
            if too_close:
                continue
            
            dead_end_positions.append((dx, dy))
        
        # Create the dead ends
        for dx, dy in dead_end_positions:
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
        
        # Scale trap zones based on maze size
        # 30x30 had 10 traps, 50x50 should have ~15-18
        num_traps = int((self.width * self.height) / 80)  # ~11 for 30x30, ~31 for 50x50
        # Cap it at reasonable amount
        num_traps = min(num_traps, 18)
        
        # Generate random trap centers
        trap_centers = []
        attempts = 0
        max_attempts = num_traps * 10
        
        while len(trap_centers) < num_traps and attempts < max_attempts:
            attempts += 1
            tx = random.randint(5, self.width - 6)
            ty = random.randint(5, self.height - 6)
            
            # Skip if on correct path
            if (tx, ty) in self.correct_path_cells:
                continue
            
            # Skip if too close to start or exit
            if (abs(tx - self.start_pos[0]) < 6 and abs(ty - self.start_pos[1]) < 6):
                continue
            if (abs(tx - self.exit_pos[0]) < 6 and abs(ty - self.exit_pos[1]) < 6):
                continue
            
            # Skip if already have trap nearby
            too_close = False
            for ex, ey in trap_centers:
                if abs(tx - ex) < 6 and abs(ty - ey) < 6:
                    too_close = True
                    break
            if too_close:
                continue
            
            trap_centers.append((tx, ty))
        
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
        
        # IMPORTANT: Analyze and mark all actual dead ends
        self._identify_all_dead_ends()
    
    def _identify_all_dead_ends(self):
        """
        Analyze the entire maze and mark ALL cells that are actual dead ends.
        A dead end is a cell with only ONE non-wall neighbor (no way out except back).
        """
        dead_end_count = 0
        
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                cell = self.grid[x][y]
                
                # Skip walls, start, and exit
                if cell.is_wall or cell.is_start or cell.is_exit:
                    continue
                
                # Count non-wall neighbors
                neighbors = []
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height and
                        not self.grid[nx][ny].is_wall):
                        neighbors.append((nx, ny))
                
                # If only 1 neighbor, this is a dead end!
                if len(neighbors) == 1:
                    cell.is_dead_end = True
                    cell.is_trap = True  # Dead ends are traps
                    dead_end_count += 1
                else:
                    # Make sure it's not marked as dead end
                    cell.is_dead_end = False
                    cell.is_trap = False
        
        print(f"Identified {dead_end_count} dead ends in the maze")
    
    
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
        """Create a COMPLEX winding path from start to exit with MANY turns"""
        sx, sy = self.start_pos
        ex, ey = self.exit_pos
        
        x, y = sx, sy
        
        # Create a VERY winding path with multiple direction changes
        # We'll use a snake-like pattern with random variations
        
        path_cells = [(x, y)]
        direction = 'right'  # Start going right
        
        while (x, y) != (ex, ey):
            moved = False
            
            # Try to move in current direction
            if direction == 'right' and x < ex - 1:
                # Move right for a random distance
                steps = random.randint(3, 6)
                for _ in range(steps):
                    if x < ex:
                        self.grid[x][y].is_wall = False
                        self.grid[x][y].is_dead_end = False
                        self.grid[x][y].is_trap = False
                        path_cells.append((x, y))
                        x += 1
                        moved = True
                # Change direction
                direction = random.choice(['down', 'up']) if y != ey else 'down'
                
            elif direction == 'left' and x > sx + 2:
                # Move left for a random distance
                steps = random.randint(2, 4)
                for _ in range(steps):
                    if x > sx + 2:
                        self.grid[x][y].is_wall = False
                        self.grid[x][y].is_dead_end = False
                        self.grid[x][y].is_trap = False
                        path_cells.append((x, y))
                        x -= 1
                        moved = True
                # Change direction
                direction = random.choice(['down', 'right'])
                
            elif direction == 'down' and y < ey - 1:
                # Move down for a random distance
                steps = random.randint(3, 6)
                for _ in range(steps):
                    if y < ey:
                        self.grid[x][y].is_wall = False
                        self.grid[x][y].is_dead_end = False
                        self.grid[x][y].is_trap = False
                        path_cells.append((x, y))
                        y += 1
                        moved = True
                # Change direction - sometimes go left to make it interesting
                if x > ex and random.random() < 0.3:
                    direction = 'left'
                else:
                    direction = random.choice(['right', 'left']) if x != ex else 'right'
                    
            elif direction == 'up' and y > sy + 2:
                # Move up for a random distance
                steps = random.randint(2, 4)
                for _ in range(steps):
                    if y > sy + 2:
                        self.grid[x][y].is_wall = False
                        self.grid[x][y].is_dead_end = False
                        self.grid[x][y].is_trap = False
                        path_cells.append((x, y))
                        y -= 1
                        moved = True
                # Change direction
                direction = random.choice(['right', 'down'])
            
            # If stuck, move directly toward goal
            if not moved:
                if x < ex:
                    self.grid[x][y].is_wall = False
                    self.grid[x][y].is_dead_end = False
                    self.grid[x][y].is_trap = False
                    path_cells.append((x, y))
                    x += 1
                    direction = 'right'
                elif y < ey:
                    self.grid[x][y].is_wall = False
                    self.grid[x][y].is_dead_end = False
                    self.grid[x][y].is_trap = False
                    path_cells.append((x, y))
                    y += 1
                    direction = 'down'
                elif x > ex:
                    self.grid[x][y].is_wall = False
                    self.grid[x][y].is_dead_end = False
                    self.grid[x][y].is_trap = False
                    path_cells.append((x, y))
                    x -= 1
                    direction = 'left'
                elif y > ey:
                    self.grid[x][y].is_wall = False
                    self.grid[x][y].is_dead_end = False
                    self.grid[x][y].is_trap = False
                    path_cells.append((x, y))
                    y -= 1
                    direction = 'up'
                else:
                    break
        
        # Ensure exit is reachable
        self.grid[ex][ey].is_wall = False
        self.grid[ex][ey].is_dead_end = False
        self.grid[ex][ey].is_trap = False
        path_cells.append((ex, ey))
        
        # Clear cells around the path to make corridors (but keep it narrow)
        for px, py in path_cells:
            # Only clear one random adjacent cell to keep it challenging
            if random.random() < 0.4:
                direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                dx, dy = direction
                nx, ny = px + dx, py + dy
                if 1 < nx < self.width - 2 and 1 < ny < self.height - 2:
                    self.grid[nx][ny].is_wall = False
                    self.grid[nx][ny].is_dead_end = False
                    self.grid[nx][ny].is_trap = False
    
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