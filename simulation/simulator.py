# simulation/simulator.py

import time
from agents.robot_agent import RobotAgent
from coordination.blackboard import Blackboard
from coordination.negotiation import Negotiator

class Simulator:
    """Main simulation controller"""
    
    def __init__(self, maze, num_agents, agent_energy, vision_range, comm_range):
        self.maze = maze
        self.num_agents = num_agents
        self.blackboard = Blackboard()
        self.blackboard.maze = maze  # Give blackboard access to maze
        
        # Create agents at start position
        start_x, start_y = maze.start_pos
        self.agents = []
        for i in range(num_agents):
            agent = RobotAgent(
                agent_id=i,
                start_x=start_x,
                start_y=start_y,
                energy=agent_energy,
                vision_range=vision_range,
                comm_range=comm_range
            )
            self.agents.append(agent)
        
        self.step_count = 0
        self.simulation_complete = False
        self.winner_agent = None
        
    def step(self):
        """Execute one simulation step"""
        if self.simulation_complete:
            return False
        
        self.step_count += 1
        
        # Check if any agent reached exit
        for agent in self.agents:
            if agent.reached_exit and not self.winner_agent:
                self.winner_agent = agent
                self.simulation_complete = True
        
        # Each agent perceives and acts
        active_agents = [a for a in self.agents if a.is_active()]
        
        if not active_agents:
            self.simulation_complete = True
            return False
        
        # Coordinate exploration (negotiation phase)
        assignments = Negotiator.coordinate_exploration(active_agents, self.maze, self.blackboard)
        
        # Update agent targets based on negotiation
        for agent_id, target in assignments.items():
            for agent in active_agents:
                if agent.id == agent_id:
                    agent.current_target = target
        
        # Each agent takes action
        for agent in active_agents:
            # Perceive environment
            agent.perceive_environment(self.maze)
            
            # Decide next move
            next_pos = agent.decide_next_move(self.maze, self.blackboard)
            
            # Execute move
            if next_pos:
                agent.move(next_pos)
            
            # Share knowledge
            agent.share_knowledge(self.blackboard)
        
        return True
    
    def run_until_complete(self, max_steps=1000):
        """Run simulation until completion or max steps"""
        while self.step_count < max_steps and not self.simulation_complete:
            self.step()
        
        return self.get_results()
    
    def get_results(self):
        """Get simulation results"""
        results = {
            'steps': self.step_count,
            'completed': self.simulation_complete,
            'winner': self.winner_agent.id if self.winner_agent else None,
            'agents_reached_exit': sum(1 for a in self.agents if a.reached_exit),
            'total_cells_explored': len(self.blackboard.explored_cells),
            'dead_ends_found': len(self.blackboard.dead_ends),
            'paths_found': len(self.blackboard.paths_to_exit),
            'best_path_length': self.blackboard.get_best_path()['length'] if self.blackboard.get_best_path() else None,
            'agent_stats': []
        }
        
        for agent in self.agents:
            results['agent_stats'].append({
                'id': agent.id,
                'final_position': agent.get_position(),
                'energy_remaining': agent.energy,
                'path_length': len(agent.path_history),
                'reached_exit': agent.reached_exit
            })
        
        return results
    
    def reset(self):
        """Reset simulation"""
        self.blackboard.reset()
        start_x, start_y = self.maze.start_pos
        
        for agent in self.agents:
            agent.x = start_x
            agent.y = start_y
            agent.energy = agent.max_energy
            agent.path_history = [(start_x, start_y)]
            agent.local_map.clear()
            agent.current_target = None
            agent.reached_exit = False
            agent.stuck_counter = 0
        
        self.step_count = 0
        self.simulation_complete = False
        self.winner_agent = None