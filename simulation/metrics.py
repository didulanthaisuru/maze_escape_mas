# Performance metrics for simulation analysis

class Metrics:
    """
    Performance metrics tracker for the simulation
    """
    
    def __init__(self):
        """
        Initialize metrics tracker
        """
        self.total_steps = 0
        self.successful_agents = 0
        self.total_distance = 0
        self.messages_sent = 0
        
    def record_step(self):
        """
        Record a simulation step
        """
        self.total_steps += 1
    
    def record_success(self, agent_id):
        """
        Record successful goal completion by an agent
        
        Args:
            agent_id: ID of the successful agent
        """
        self.successful_agents += 1
    
    def record_distance(self, distance):
        """
        Record distance traveled
        
        Args:
            distance: Distance value
        """
        self.total_distance += distance
    
    def record_message(self):
        """
        Record a message sent between agents
        """
        self.messages_sent += 1
    
    def get_summary(self):
        """
        Get summary of metrics
        """
        return {
            'total_steps': self.total_steps,
            'successful_agents': self.successful_agents,
            'total_distance': self.total_distance,
            'messages_sent': self.messages_sent,
            'avg_distance': self.total_distance / max(self.successful_agents, 1)
        }
    
    def reset(self):
        """
        Reset all metrics
        """
        self.total_steps = 0
        self.successful_agents = 0
        self.total_distance = 0
        self.messages_sent = 0
