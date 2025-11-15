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
        self.stuck_counter = 0
        
    def get_position(self):
        """Get current position as tuple"""
        return (self.x, self.y)
    
    def manhattan_distance(self, target):
        """Calculate Manhattan distance to target"""
        return abs(self.x - target[0]) + abs(self.y - target[1])
    
    def can_communicate_with(self, other_agent):
        """Check if agent can communicate with another agent"""
        distance = self.manhattan_distance(other_agent.get_position())
        return distance <= self.communication_range
    
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
    
    def decide_next_move(self, maze, blackboard):
        """
        Decide the next move based on:
        1. Known information from blackboard
        2. Local perception
        3. Exploration strategy
        """
        current_pos = self.get_position()
        
        # Check if at exit
        if maze.get_cell(self.x, self.y).is_exit:
            self.reached_exit = True
            blackboard.add_path_to_exit(self.path_history, self.id)
            return None
        
        # Get valid neighbors
        neighbors = maze.get_neighbors(self.x, self.y)
        
        # Filter out dead ends and walls
        valid_neighbors = [
            n for n in neighbors 
            if not blackboard.is_dead_end(n)
        ]
        
        if not valid_neighbors:
            # Mark current position as dead end
            blackboard.add_dead_end(current_pos, self.id)
            # Backtrack
            if len(self.path_history) > 1:
                self.path_history.pop()
                return self.path_history[-1]
            return None
        
        # Strategy 1: Move toward exit if visible
        for nx, ny in valid_neighbors:
            if maze.get_cell(nx, ny).is_exit:
                return (nx, ny)
        
        # Strategy 2: Explore unexplored areas
        unexplored = [n for n in valid_neighbors if not blackboard.is_explored(n)]
        
        if unexplored:
            # Check if target is assigned via negotiation
            if self.current_target and self.current_target in unexplored:
                return self.current_target
            
            # Choose closest unexplored
            target = min(unexplored, key=lambda n: self.manhattan_distance(n))
            self.current_target = target
            blackboard.update_agent_target(self.id, target)
            return target
        
        # Strategy 3: Move to least visited neighbor
        visit_counts = {}
        for n in valid_neighbors:
            visit_counts[n] = sum(1 for pos in self.path_history if pos == n)
        
        target = min(visit_counts.items(), key=lambda x: x[1])[0]
        return target
    
    def move(self, target_pos):
        """Move to target position"""
        if target_pos:
            self.x, self.y = target_pos
            self.path_history.append(target_pos)
            self.energy -= 1
            
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
        """Check if agent can still act"""
        return self.energy > 0 and not self.reached_exit
    
    def __repr__(self):
        return f"Robot{self.id}@({self.x},{self.y})"