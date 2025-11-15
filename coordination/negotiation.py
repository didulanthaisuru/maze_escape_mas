# coordination/negotiation.py

import random

class Negotiator:
    """Handles negotiation between agents for path conflicts"""
    
    @staticmethod
    def resolve_target_conflict(agents_in_conflict, targets, blackboard):
        """
        Resolve conflicts when multiple agents want the same target.
        Strategy: Priority based on distance and energy.
        """
        if not agents_in_conflict:
            return {}
        
        assignments = {}
        available_targets = list(targets)
        
        # Sort agents by priority (higher energy + closer distance)
        def priority(agent):
            if not available_targets:
                return 0
            min_dist = min(agent.manhattan_distance(t) for t in available_targets)
            return agent.energy - min_dist
        
        sorted_agents = sorted(agents_in_conflict, key=priority, reverse=True)
        
        for agent in sorted_agents:
            if not available_targets:
                break
                
            # Find best target for this agent
            best_target = min(
                available_targets,
                key=lambda t: agent.manhattan_distance(t)
            )
            
            assignments[agent.id] = best_target
            available_targets.remove(best_target)
        
        return assignments
    
    @staticmethod
    def coordinate_exploration(agents, maze, blackboard):
        """
        Coordinate exploration to minimize redundancy.
        Assigns unexplored areas to different agents.
        """
        unexplored_positions = set()
        
        # Find all unexplored adjacent positions
        for agent in agents:
            neighbors = maze.get_neighbors(agent.x, agent.y)
            for nx, ny in neighbors:
                if not blackboard.is_explored((nx, ny)) and not blackboard.is_dead_end((nx, ny)):
                    unexplored_positions.add((nx, ny))
        
        if not unexplored_positions:
            return {}
        
        # Find conflicts (multiple agents wanting same target)
        target_counts = {}
        for agent in agents:
            target = blackboard.get_agent_target(agent.id)
            if target and target in unexplored_positions:
                if target not in target_counts:
                    target_counts[target] = []
                target_counts[target].append(agent)
        
        # Resolve conflicts
        assignments = {}
        conflicted_agents = []
        conflicted_targets = []
        
        for target, agent_list in target_counts.items():
            if len(agent_list) > 1:
                # Conflict detected
                conflicted_agents.extend(agent_list)
                conflicted_targets.append(target)
        
        if conflicted_agents:
            # Use negotiator to resolve
            resolved = Negotiator.resolve_target_conflict(
                conflicted_agents,
                unexplored_positions,
                blackboard
            )
            assignments.update(resolved)
        
        return assignments
    
    @staticmethod
    def request_path_clearance(agent, target_pos, blackboard):
        """
        Check if another agent is blocking the path.
        Returns True if path is clear or cleared.
        """
        # Check if any other agent is at the target position
        for other_id, other_pos in blackboard.agent_positions.items():
            if other_id != agent.id and other_pos == target_pos:
                # Another agent is at target
                # Simple strategy: wait or find alternative
                return False
        
        return True