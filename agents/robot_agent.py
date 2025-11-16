# agents/robot_agent.py

import random
from collections import deque

class RobotAgent:
    """
    Individual robot agent that explores the maze.
    Features: local memory, energy management, communication capability.
    """
    
    def __init__(self, agent_id, start_x, start_y, energy, vision_range, comm_range):
        self.id = agent_id
        self.x = start_x
        self.y = start_y
        self.energy = energy
        self.max_energy = energy
        self.vision_range = vision_range
        self.communication_range = comm_range
        
        # Memory and state
        self.path_history = [(start_x, start_y)]
        self.local_map = {}  # Local knowledge of maze
        self.current_target = None
        self.reached_exit = False
        self.is_dead = False  # True when agent enters a dead end (permanent death)
        self.stuck_counter = 0
        self.backtrack_positions = set()  # Positions we've backtracked from (WRONG_PATH)
        self.last_position = None  # Track previous position to prevent immediate backtracking
        self.stuck_in_loop_counter = 0  # Count how many steps we've been in same area
        self.recent_positions = deque(maxlen=10)  # Track last 10 positions for loop detection
        
        # Communication
        self.known_dead_ends = set()  # Dead ends learned from messages (TRUE dead ends - can't go back)
        self.known_wrong_paths = set()  # Wrong paths learned from messages (can backtrack)
        self.known_traps = set()  # Trap locations learned from messages
        self.exit_location = None  # Exit location if discovered
        self.exit_path = None  # Path to exit shared by discovering agent
        self.should_evacuate = False  # True when exit is found by any agent
        self.received_messages = []  # Store received messages
        
    def get_position(self):
        """Get current position as tuple"""
        return (self.x, self.y)
    
    def manhattan_distance(self, target):
        """Calculate Manhattan distance to target"""
        return abs(self.x - target[0]) + abs(self.y - target[1])
    
    def can_communicate_with(self, other_agent):
        """Check if agent can communicate with another agent - unlimited range"""
        # All agents can communicate with each other regardless of distance
        return True
    
    def perceive_environment(self, maze):
        """
        Perceive the environment within vision range.
        Returns visible cells.
        """
        visible_cells = []
        
        for dx in range(-self.vision_range, self.vision_range + 1):
            for dy in range(-self.vision_range, self.vision_range + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < maze.width and 0 <= ny < maze.height:
                    cell = maze.get_cell(nx, ny)
                    if cell:
                        visible_cells.append(cell)
                        # Update local map
                        self.local_map[(nx, ny)] = {
                            'is_wall': cell.is_wall,
                            'is_exit': cell.is_exit
                        }
        
        return visible_cells
    
    def process_messages(self, communication_protocol):
        """
        Process incoming messages from other agents
        """
        messages = communication_protocol.receive_messages(self.id)
        
        for msg in messages:
            self.received_messages.append(msg)
            
            if msg.message_type == 'DEAD_END':
                # Another agent found a TRUE dead end (can't go back)
                dead_end_pos = msg.content.get('position')
                if dead_end_pos:
                    self.known_dead_ends.add(dead_end_pos)
                    if msg.content.get('is_trap'):
                        self.known_traps.add(dead_end_pos)
                    
            elif msg.message_type == 'WRONG_PATH':
                # Another agent found an unproductive path (CAN backtrack but wastes time)
                wrong_path_pos = msg.content.get('position')
                if wrong_path_pos:
                    self.known_wrong_paths.add(wrong_path_pos)
                    
            elif msg.message_type == 'EXIT_FOUND':
                # Another agent found the exit! Get the path!
                self.exit_location = msg.content.get('position')
                self.exit_path = msg.content.get('path')  # Get the successful path
                self.should_evacuate = True
                print(f"DEBUG: Agent {self.id} received EXIT_FOUND message! Path length: {len(self.exit_path) if self.exit_path else 0}")
                
            elif msg.message_type == 'PATH_SHARED':
                # Another agent shared a useful path
                pass  # Could use this to guide exploration
    
    def decide_next_move(self, maze, blackboard, communication_protocol):
        """
        Decide the next move based on:
        1. Check if at exit (ALWAYS CHECK FIRST!)
        2. EXIT_FOUND message with path (HIGHEST PRIORITY - follow the path!)
        3. Known information from blackboard
        4. Local perception
        5. Exploration strategy
        """
        current_pos = self.get_position()
        current_cell = maze.get_cell(self.x, self.y)
        
        # Track position for oscillation detection
        self.recent_positions.append(current_pos)
        
        # OSCILLATION DETECTION: If stuck in a loop, force a random move
        if len(self.recent_positions) == 10:
            # Check if we're oscillating between same 2-3 positions
            unique_recent = set(self.recent_positions)
            if len(unique_recent) <= 3:
                # We're stuck oscillating!
                self.stuck_in_loop_counter += 1
                print(f"Agent {self.id} oscillating between {unique_recent}! Counter: {self.stuck_in_loop_counter}")
                
                if self.stuck_in_loop_counter > 5:
                    # Force staying put to wait for rescue
                    print(f"Agent {self.id} stuck oscillating - STAYING PUT and waiting")
                    self.stuck_in_loop_counter = 0  # Reset counter
                    self.recent_positions.clear()  # Clear history
                    return None  # Stay put and wait
            else:
                # We're moving around OK, reset counter
                self.stuck_in_loop_counter = 0
        
        # PRIORITY 0: Check if at exit (ALWAYS CHECK FIRST!)
        if current_cell and current_cell.is_exit:
            if not self.reached_exit:
                self.reached_exit = True
                
                # Calculate CLEAN path from start to exit (no dead ends, no backtracking)
                clean_path = self._calculate_clean_path(maze)
                
                # BROADCAST: I found the exit AND share the CLEAN path!
                communication_protocol.broadcast(
                    self.id, 
                    'EXIT_FOUND', 
                    {
                        'position': current_pos, 
                        'agent_id': self.id,
                        'path': clean_path  # Share the CLEAN path without dead ends!
                    }
                )
                blackboard.add_path_to_exit(clean_path, self.id)
                blackboard.post_message(self.id, 'exit_found', {'position': current_pos})
            return None  # Stay at exit
        
        # CRITICAL FIX: If exit path is known, NO AGENT CAN DIE - EVER!
        # Even if on dead end, they MUST be able to escape using the shared path!
        if self.should_evacuate and self.exit_path:
            # Use BFS to find shortest path from current position to ANY point on the exit path
            # This is MUCH smarter than just moving towards closest point!
            from collections import deque
            
            def bfs_to_exit_path():
                """Find shortest path from current position to the exit path using BFS"""
                queue = deque([(current_pos, [current_pos])])
                visited = {current_pos}
                
                while queue:
                    pos, path = queue.popleft()
                    
                    # If we reached the exit path, return the next step!
                    if pos in self.exit_path:
                        # Return the SECOND element in path (first step to take)
                        if len(path) > 1:
                            return path[1]  # Next immediate step
                        return None  # Already on path
                    
                    # Explore neighbors
                    for neighbor in maze.get_neighbors(pos[0], pos[1]):
                        if neighbor in visited:
                            continue
                        
                        # Check if neighbor is safe (not wall)
                        cell = maze.get_cell(neighbor[0], neighbor[1])
                        if not cell or cell.is_wall:
                            continue
                        
                        # During evacuation, we can go ANYWHERE (even dead ends) to reach the path!
                        # This is rescue mode - survival is guaranteed if we reach the path!
                        
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
                
                return None  # No path found
            
            # Check if we're already on the exit path
            if current_pos in self.exit_path:
                # We're on the path! Follow it to exit
                current_index = self.exit_path.index(current_pos)
                if current_index < len(self.exit_path) - 1:
                    # Move to next step on the path
                    next_step = self.exit_path[current_index + 1]
                    
                    # Check if next step is accessible
                    neighbors = maze.get_neighbors(self.x, self.y)
                    if next_step in neighbors:
                        next_cell = maze.get_cell(next_step[0], next_step[1])
                        if next_cell and not next_cell.is_wall:
                            return next_step
                    
                    # Next step blocked! Use BFS to navigate around obstacle
                    print(f"Agent {self.id} on path but next step {next_step} blocked! Finding alternate route...")
                    alternate = bfs_to_exit_path()
                    if alternate:
                        return alternate
                    
                    # If BFS fails, just pick best available neighbor toward exit
                    safe_neighbors = [n for n in neighbors if not maze.get_cell(n[0], n[1]).is_wall]
                    if safe_neighbors:
                        # Move toward exit
                        exit_pos = self.exit_path[-1]
                        best = min(safe_neighbors, key=lambda n: abs(n[0] - exit_pos[0]) + abs(n[1] - exit_pos[1]))
                        return best
                    
                    print(f"Agent {self.id} STUCK on path! Staying put...")
                    return None  # Stay put - don't die
                else:
                    # We're at the end of path - should be at exit
                    return None
            
            # Not on path yet - use BFS to find shortest route TO the path
            print(f"Agent {self.id} at {current_pos} navigating TO exit path using BFS...")
            next_move = bfs_to_exit_path()
            if next_move:
                return next_move
            
            # BFS failed - fall back to simple navigation toward closest path point
            print(f"Agent {self.id} BFS failed! Using simple navigation...")
            closest_path_pos = min(self.exit_path, key=lambda p: abs(p[0] - self.x) + abs(p[1] - self.y))
            neighbors = maze.get_neighbors(self.x, self.y)
            safe_neighbors = [n for n in neighbors if not maze.get_cell(n[0], n[1]).is_wall]
            
            if closest_path_pos in safe_neighbors:
                return closest_path_pos
            
            if safe_neighbors:
                best_neighbor = min(safe_neighbors,
                                  key=lambda n: abs(n[0] - closest_path_pos[0]) + 
                                              abs(n[1] - closest_path_pos[1]))
                return best_neighbor
            
            # ABSOLUTE LAST RESORT: Even if truly stuck, DON'T DIE!
            # Stay put and wait for rescue or path to clear
            print(f"Agent {self.id} has exit path but NO moves available! STAYING PUT - will NOT die!")
            return None
        
        # CHECK: Are we on a TRUE DEAD END cell? (Cannot move at all!)
        # BUT ONLY DIE if exit path is NOT known yet!
        if current_cell and current_cell.is_dead_end:
            # We stepped on a dead end cell - we're DEAD! No escape, no rescue!
            # This agent is finished - permanently stuck
            if not self.reached_exit and not self.is_dead:
                print(f"Agent {self.id} DIED in dead end at {current_pos}! RIP ☠️")
                self.is_dead = True  # Mark as permanently dead
                
                # Broadcast that we died here - warn others!
                communication_protocol.broadcast(
                    self.id,
                    'DEAD_END',
                    {
                        'position': current_pos,
                        'agent_id': self.id,
                        'is_trap': True,
                        'message': f'Agent {self.id} DIED in dead end! AVOID THIS CELL!'
                    }
                )
                blackboard.add_dead_end(current_pos, self.id)
            
            # Cannot move - permanently stuck (DEAD)
            return None
        
        # PRIORITY 2: If exit found but no path yet, navigate toward exit location
        if self.should_evacuate and self.exit_location:
            neighbors = maze.get_neighbors(self.x, self.y)
            
            # CRITICAL: Filter out dead ends FIRST!
            safe_neighbors = []
            for n in neighbors:
                cell = maze.get_cell(n[0], n[1])
                if cell and cell.is_dead_end:
                    # Don't go to dead ends during evacuation!
                    continue
                safe_neighbors.append(n)
            
            if not safe_neighbors:
                # No safe neighbors - backtrack if possible
                print(f"Agent {self.id} stuck navigating to exit location! Attempting backtrack.")
                if len(self.path_history) > 1:
                    prev_pos = self.path_history[-2]
                    all_neighbors = maze.get_neighbors(self.x, self.y)
                    if prev_pos in all_neighbors:
                        prev_cell = maze.get_cell(prev_pos[0], prev_pos[1])
                        if prev_cell and not prev_cell.is_dead_end:
                            return prev_pos
                # Stay put instead of dying
                return None
            
            if self.exit_location in safe_neighbors:
                return self.exit_location
            
            if safe_neighbors:
                # Filter out last position to prevent oscillation
                available_neighbors = safe_neighbors
                if self.last_position and self.last_position in available_neighbors:
                    temp = [n for n in available_neighbors if n != self.last_position]
                    if temp:  # Only filter if we have other options
                        available_neighbors = temp
                
                # Also avoid cells we've visited very recently (last 3 positions)
                recent_positions = set(self.path_history[-3:]) if len(self.path_history) >= 3 else set()
                unvisited = [n for n in available_neighbors if n not in recent_positions]
                if unvisited:
                    available_neighbors = unvisited
                
                if available_neighbors:
                    best_neighbor = min(available_neighbors, 
                                      key=lambda n: abs(n[0] - self.exit_location[0]) + 
                                                  abs(n[1] - self.exit_location[1]))
                    return best_neighbor
            
            # No valid neighbors - return None
            return None
        
        # Check if we're in a trap (only broadcast once)
        if current_cell and current_cell.is_trap and current_pos not in self.known_traps:
            # BROADCAST: I'm in a trap!
            communication_protocol.broadcast(
                self.id,
                'DEAD_END',
                {
                    'position': current_pos, 
                    'agent_id': self.id,
                    'is_trap': True,
                    'message': f'Agent {self.id} found a trap zone!'
                }
            )
            blackboard.add_dead_end(current_pos, self.id)
            self.known_traps.add(current_pos)
        
        # Get ALL neighbors
        neighbors = maze.get_neighbors(self.x, self.y)
        
        # Filter out ONLY known dead ends from messages or blackboard
        # BUT: If we have the exit path (evacuation mode), also filter out actual dead end cells!
        safe_neighbors = []
        for n in neighbors:
            # Skip if in our known dead ends (from messages or experience)
            if n in self.known_dead_ends:
                continue
            # Skip if in our known traps (from messages)
            if n in self.known_traps:
                continue
            # Skip if blackboard knows it's a dead end (another agent reported it)
            if blackboard.is_dead_end(n):
                continue
            
            # CRITICAL: If we're evacuating (exit found), check the actual cell to avoid dead ends!
            if self.should_evacuate:
                cell = maze.get_cell(n[0], n[1])
                if cell and cell.is_dead_end:
                    # Don't go there! We know the exit path, no need to explore dead ends!
                    continue
            
            # This neighbor is safe (or unknown - which is fine for exploration!)
            safe_neighbors.append(n)
        
        # Further filter: deprioritize wrong paths (can still use if needed)
        preferred_neighbors = [n for n in safe_neighbors if n not in self.known_wrong_paths]
        
        # Also avoid cells we've already explored multiple times (unless necessary)
        # Count how many times we've visited each safe neighbor
        visit_counts = {}
        for n in safe_neighbors:
            visit_counts[n] = sum(1 for pos in self.path_history if pos == n)
        
        # Prefer unvisited or rarely visited cells
        fresh_neighbors = [n for n in safe_neighbors if visit_counts.get(n, 0) <= 1]
        
        # Use best available neighbors in priority order
        if fresh_neighbors:
            valid_neighbors = fresh_neighbors
        elif preferred_neighbors:
            valid_neighbors = preferred_neighbors
        else:
            valid_neighbors = safe_neighbors
        
        if not valid_neighbors:
            # This is a dead end! Tell everyone so they don't come here!
            blackboard.add_dead_end(current_pos, self.id)
            
            # Check if it's a trap
            is_trap = current_cell and current_cell.is_trap
            
            # BROADCAST: Dead end found here! DON'T COME HERE!
            communication_protocol.broadcast(
                self.id,
                'DEAD_END',
                {
                    'position': current_pos, 
                    'agent_id': self.id,
                    'is_trap': is_trap
                }
            )
            
            # Backtrack if possible
            if len(self.path_history) > 1:
                self.path_history.pop()
                backtrack_pos = self.path_history[-1]
                self.backtrack_positions.add(current_pos)
                
                # BROADCAST: Wrong path - had to backtrack
                communication_protocol.broadcast(
                    self.id,
                    'WRONG_PATH',
                    {
                        'position': current_pos,
                        'agent_id': self.id,
                        'message': f'Agent {self.id} backtracking from dead end'
                    }
                )
                
                return backtrack_pos
            return None
        
        # Strategy 1: Move toward exit if visible
        for nx, ny in valid_neighbors:
            cell = maze.get_cell(nx, ny)
            if cell and cell.is_exit:
                blackboard.post_message(self.id, 'exit_visible', {'position': (nx, ny)})
                return (nx, ny)
        
        # Strategy 2: Prioritize UNVISITED cells to avoid re-exploration
        unvisited = [n for n in valid_neighbors if n not in self.path_history]
        
        if unvisited:
            # Check if target is assigned via negotiation
            if self.current_target and self.current_target in unvisited:
                return self.current_target
            
            # Choose unvisited cell (prefer unexplored by blackboard too)
            unexplored_by_all = [n for n in unvisited if not blackboard.is_explored(n)]
            
            if unexplored_by_all:
                target = min(unexplored_by_all, key=lambda n: self.manhattan_distance(n))
            else:
                target = min(unvisited, key=lambda n: self.manhattan_distance(n))
            
            self.current_target = target
            blackboard.update_agent_target(self.id, target)
            blackboard.post_message(self.id, 'exploring', {'target': target})
            return target
        
        # Strategy 3: All neighbors visited - choose least visited
        # This means we're likely backtracking or in a complex area
        visit_counts = {}
        for n in valid_neighbors:
            visit_counts[n] = sum(1 for pos in self.path_history if pos == n)
        
        if visit_counts:
            # Check if we're going in circles
            max_visits = max(visit_counts.values())
            if max_visits > 3:  # Been here too many times - wrong path!
                # BROADCAST: This area seems unproductive (WRONG_PATH)
                communication_protocol.broadcast(
                    self.id,
                    'WRONG_PATH',
                    {
                        'position': current_pos,
                        'agent_id': self.id,
                        'message': f'Agent {self.id} going in circles, likely wrong path'
                    }
                )
                self.backtrack_positions.add(current_pos)
            
            target = min(visit_counts.items(), key=lambda x: x[1])[0]
            return target
        
        return None
    
    def _calculate_clean_path(self, maze):
        """
        Calculate clean path from start to current position (exit) using BFS.
        This avoids dead ends and gives the shortest path.
        """
        from collections import deque
        
        start = maze.start_pos
        goal = self.get_position()
        
        # BFS to find shortest path
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == goal:
                return path
            
            # Get neighbors
            neighbors = maze.get_neighbors(current[0], current[1])
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        # Fallback: if BFS fails, return path_history
        return self.path_history.copy()
    
    def move(self, target_pos):
        """Move to target position - no energy consumption"""
        if target_pos:
            self.last_position = (self.x, self.y)  # Remember where we came from
            self.x, self.y = target_pos
            self.path_history.append(target_pos)
            # No energy consumption - agents can explore indefinitely
            
    def share_knowledge(self, blackboard):
        """Share discovered information with the blackboard"""
        current_pos = self.get_position()
        blackboard.add_explored_cell(current_pos, self.id)
        blackboard.update_agent_position(self.id, current_pos)
        
        # Mark cell as explored in maze
        cell = None
        if hasattr(blackboard, 'maze'):
            cell = blackboard.maze.get_cell(self.x, self.y)
            if cell:
                cell.explored_by.add(self.id)
    
    def is_active(self):
        """Check if agent can still act - no energy limit, only death or exit matters"""
        return not self.reached_exit and not self.is_dead
    
    def __repr__(self):
        return f"Robot{self.id}@({self.x},{self.y})"