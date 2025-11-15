# Communication protocols for multi-agent system

class Message:
    """Message object for agent communication"""
    def __init__(self, sender_id, message_type, content, timestamp):
        self.sender_id = sender_id
        self.message_type = message_type
        self.content = content
        self.timestamp = timestamp
        self.read_by = set()
    
    def __repr__(self):
        return f"Message(from={self.sender_id}, type={self.message_type}, content={self.content})"


class CommunicationProtocol:
    """
    Communication protocol for agent-to-agent messaging
    """
    
    def __init__(self):
        """
        Initialize communication protocol
        """
        self.message_queue = []
        self.broadcast_messages = []  # Messages sent to all agents
        self.direct_messages = {}  # Direct messages to specific agents
        self.message_counter = 0
        
    def send_message(self, sender_id, receiver_id, message_type, content):
        """
        Send a direct message from one agent to another
        
        Args:
            sender_id: ID of sending agent
            receiver_id: ID of receiving agent
            message_type: Type of message
            content: Message content
        """
        message = Message(sender_id, message_type, content, self.message_counter)
        self.message_counter += 1
        
        if receiver_id not in self.direct_messages:
            self.direct_messages[receiver_id] = []
        self.direct_messages[receiver_id].append(message)
        
        return message
    
    def broadcast(self, sender_id, message_type, content):
        """
        Broadcast message to all agents
        
        Args:
            sender_id: ID of sending agent
            message_type: Type of message (DEAD_END, EXIT_FOUND, WRONG_PATH, etc.)
            content: Message content (position, path, etc.)
        """
        message = Message(sender_id, message_type, content, self.message_counter)
        self.message_counter += 1
        self.broadcast_messages.append(message)
        
        return message
    
    def receive_messages(self, agent_id):
        """
        Retrieve unread messages for a specific agent
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            List of messages for this agent
        """
        messages = []
        
        # Get broadcast messages not yet read by this agent
        for msg in self.broadcast_messages:
            if agent_id not in msg.read_by and msg.sender_id != agent_id:
                messages.append(msg)
                msg.read_by.add(agent_id)
        
        # Get direct messages
        if agent_id in self.direct_messages:
            messages.extend(self.direct_messages[agent_id])
            self.direct_messages[agent_id] = []
        
        return messages
    
    def get_recent_broadcasts(self, count=10):
        """Get recent broadcast messages"""
        return self.broadcast_messages[-count:] if self.broadcast_messages else []
    
    def clear_old_messages(self, max_age=100):
        """Clear old messages to prevent memory buildup"""
        if len(self.broadcast_messages) > max_age:
            self.broadcast_messages = self.broadcast_messages[-max_age:]
