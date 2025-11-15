# coordination/blackboard.py

class Blackboard:
    """
    Shared knowledge base for agent communication.
    Agents can read and write information here.
    """
    
    def __init__(self):
        self.explored_cells = set()  # All cells explored by any agent
        self.dead_ends = set()       # Known dead ends
        self.paths_to_exit = []      # Successful paths found
        self.agent_positions = {}    # Current position of each agent
        self.agent_targets = {}      # Current target of each agent
        self.messages = []           # Communication messages
        
    def add_explored_cell(self, position, agent_id):
        """Mark a cell as explored by an agent"""
        self.explored_cells.add(position)
        
    def add_dead_end(self, position, agent_id):
        """Mark a position as a dead end"""
        self.dead_ends.add(position)
        self.messages.append({
            'type': 'dead_end',
            'agent_id': agent_id,
            'position': position
        })
        
    def add_path_to_exit(self, path, agent_id):
        """Add a successful path to the exit"""
        self.paths_to_exit.append({
            'path': path,
            'agent_id': agent_id,
            'length': len(path)
        })
        
    def update_agent_position(self, agent_id, position):
        """Update an agent's position"""
        self.agent_positions[agent_id] = position
        
    def update_agent_target(self, agent_id, target):
        """Update an agent's exploration target"""
        self.agent_targets[agent_id] = target
        
    def is_explored(self, position):
        """Check if a position has been explored"""
        return position in self.explored_cells
    
    def is_dead_end(self, position):
        """Check if a position is a known dead end"""
        return position in self.dead_ends
    
    def get_unexplored_neighbors(self, position, maze):
        """Get unexplored neighboring positions"""
        neighbors = maze.get_neighbors(position[0], position[1])
        return [n for n in neighbors if not self.is_explored(n) and not self.is_dead_end(n)]
    
    def get_agent_position(self, agent_id):
        """Get an agent's current position"""
        return self.agent_positions.get(agent_id)
    
    def get_agent_target(self, agent_id):
        """Get an agent's current target"""
        return self.agent_targets.get(agent_id)
    
    def get_best_path(self):
        """Get the shortest path to exit found so far"""
        if not self.paths_to_exit:
            return None
        return min(self.paths_to_exit, key=lambda p: p['length'])
    
    def post_message(self, agent_id, msg_type, data):
        """Post a message to the blackboard"""
        self.messages.append({
            'agent_id': agent_id,
            'type': msg_type,
            'data': data
        })
    
    def get_recent_messages(self, count=10):
        """Get recent messages"""
        return self.messages[-count:]
    
    def reset(self):
        """Reset the blackboard"""
        self.explored_cells.clear()
        self.dead_ends.clear()
        self.paths_to_exit.clear()
        self.agent_positions.clear()
        self.agent_targets.clear()
        self.messages.clear()