# Multi-Agent Maze Escape Simulation 🤖🔍

A comprehensive Multi-Agent System (MAS) demonstration simulating cooperative robots navigating an underground maze. This project showcases key MAS principles including communication, coordination, negotiation, and emergent behavior.

## 🎯 Project Overview

**Objective**: Simulate a team of cooperative robots navigating an underground maze to reach an exit while avoiding dead ends and optimizing the path collectively.

### Key Features

- ✅ **Communication**: Agents share information about dead ends and discovered paths via a shared blackboard
- ✅ **Coordination**: Dynamic task allocation to avoid redundant exploration
- ✅ **Negotiation**: Conflict resolution when multiple agents target the same path
- ✅ **Emergent Behavior**: Collective optimization through agent interaction
- ✅ **Real-time Visualization**: Pygame-based visual representation
- ✅ **Performance Metrics**: Compare single vs multi-agent efficiency

## 🏗️ Architecture

```
maze_escape_mas/
├── environment/      # Maze generation and representation
├── agents/          # Robot agent implementation
├── coordination/    # Blackboard and negotiation mechanisms
├── simulation/      # Simulation logic and metrics
├── visualization/   # Pygame rendering
└── utils/          # Helper functions
```

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

### 1. Clone or Create the Project

```bash
# Create the folder structure
mkdir -p maze_escape_mas/{environment,agents,coordination,simulation,visualization,utils}
cd maze_escape_mas

# Create __init__.py files
touch environment/__init__.py
touch agents/__init__.py
touch coordination/__init__.py
touch simulation/__init__.py
touch visualization/__init__.py
touch utils/__init__.py
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install pygame numpy matplotlib
```

### 3. Verify Installation

```bash
python -c "import pygame, numpy, matplotlib; print('All dependencies installed!')"
```

## 🎮 Usage

### Visual Mode (Default)

Run the simulation with real-time pygame visualization:

```bash
python main.py
```

**Interactive Controls:**
- `SPACE`: Pause/Resume simulation
- `↑/↓ Arrow Keys`: Increase/Decrease simulation speed (1-10 steps/sec)
- `S`: Single step (when paused) - execute one step at a time
- `R`: Reset simulation to beginning
- `ESC` or Close Window: Exit simulation

**Features:**
- Real-time agent communication visualization (expanding circles)
- Message log showing agent activities
- Communication range indicators
- Path trails and target indicators
- Agent status and statistics

### Using Random Maze (Optional)

By default, the simulation uses a fixed, guaranteed-solvable maze. To use random generation:

```bash
python main.py --random-maze
```

### Benchmark Mode

Compare performance across different agent counts:

```bash
# Test with default agent counts [1, 2, 3, 5, 7]
python main.py --mode benchmark

# Test specific agent counts
python main.py --mode benchmark --agents 1 3 5 10

# Run more trials for accuracy
python main.py --mode benchmark --agents 1 5 10 --trials 10

# Disable plotting
python main.py --mode benchmark --no-plot

# Use random maze for benchmarking
python main.py --mode benchmark --random-maze
````

## ⚙️ Configuration

Edit `config.py` to customize simulation parameters:

```python
# Maze Configuration
MAZE_WIDTH = 20          # Maze width
MAZE_HEIGHT = 20         # Maze height
WALL_DENSITY = 0.3       # Wall probability (0.0-1.0)

# Agent Configuration
NUM_AGENTS = 5           # Number of robot agents
AGENT_ENERGY = 100       # Starting energy per agent
AGENT_VISION_RANGE = 2   # Vision radius
COMMUNICATION_RANGE = 5  # Communication radius

# Simulation
MAX_STEPS = 1000         # Maximum simulation steps
SIMULATION_SPEED = 10    # Steps per second
```

## 🧠 Multi-Agent System Features

### 1. Communication
Agents communicate through a **shared blackboard** that stores:
- Explored cells
- Known dead ends
- Discovered paths
- Agent positions and targets

### 2. Coordination
- **Dynamic Task Allocation**: Agents negotiate to explore different branches
- **Redundancy Avoidance**: Shared knowledge prevents duplicate exploration
- **Resource Management**: Energy tracking and path optimization

### 3. Negotiation
When conflicts occur (multiple agents targeting the same position):
- Priority based on **distance** and **energy levels**
- Fair resource allocation
- Dynamic reassignment

### 4. Emergent Behavior
- Collective path optimization
- Faster solution discovery through parallel exploration
- Adaptive strategy based on shared knowledge

## 📊 Performance Metrics

The benchmark mode analyzes:
- **Steps to Completion**: Average number of steps to find exit
- **Exploration Coverage**: Percentage of maze explored
- **Success Rate**: Completion rate across trials
- **Computation Time**: Real-world execution time

### Sample Output:
```
============================================================
PERFORMANCE SUMMARY
============================================================

1 Agent(s):
  Average Steps:     487.2
  Average Explored:  156.4
  Success Rate:      100.0%
  Average Duration:  0.234s

5 Agent(s):
  Average Steps:     142.8
  Average Explored:  201.6
  Success Rate:      100.0%
  Average Duration:  0.198s

OPTIMAL CONFIGURATIONS:
  Fewest Steps:       5 agents (142.8 steps)
  Fastest Execution:  5 agents (0.198s)
============================================================
```

## 🎨 Visualization Legend

| Color | Meaning |
|-------|---------|
| Green | Start position |
| Red | Exit position |
| Light Blue | Explored cells |
| Gray | Dead ends |
| White | Unexplored paths |
| Dark Gray | Walls |
| Colored Circles | Robot agents |

## 🔬 Academic Relevance

This project demonstrates essential MAS concepts:

1. **Agent Architecture**: Reactive agents with memory and local perception
2. **Communication Protocols**: Blackboard pattern for shared knowledge
3. **Coordination Mechanisms**: Distributed task allocation
4. **Negotiation Strategies**: Priority-based conflict resolution
5. **Emergent Intelligence**: System-level optimization from individual behaviors

## 📈 Expected Outcomes

- **Single Agent**: Slower but thorough exploration
- **Multiple Agents**: 
  - Faster exit discovery (2-3x improvement)
  - Better coverage through parallel exploration
  - Efficient dead-end identification
  - Demonstrates synergy through cooperation

## 🛠️ Extending the Project

### Add New Agent Types
Edit `agents/robot_agent.py` to create specialized agents:
```python
class ScoutAgent(RobotAgent):
    """Fast agent with extended vision"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vision_range = 4  # Extended vision
```

### Implement New Negotiation Strategies
Modify `coordination/negotiation.py`:
```python
@staticmethod
def auction_based_allocation(agents, targets):
    """Auction-based task allocation"""
    # Your implementation
```

### Add Obstacles or Resources
Extend `environment/maze.py`:
```python
class Maze:
    def add_dynamic_obstacles(self):
        """Add moving obstacles"""
        # Your implementation
```

## 📝 Assignment Deliverables

This project is suitable for demonstrating:

1. ✅ Multi-agent communication
2. ✅ Coordination and cooperation
3. ✅ Negotiation protocols
4. ✅ Emergent behavior
5. ✅ Performance analysis
6. ✅ Scalability testing
7. ✅ Visual demonstration

## 🐛 Troubleshooting

### Pygame Window Not Appearing
```bash
# Install pygame properly
pip uninstall pygame
pip install pygame==2.5.2
```

### Matplotlib Errors
```bash
# Install matplotlib backend
pip install matplotlib pillow
```

### Permission Errors
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 References

- Wooldridge, M. (2009). An Introduction to MultiAgent Systems
- Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach
- Ferber, J. (1999). Multi-Agent Systems: An Introduction to Distributed Artificial Intelligence

## 📄 License

This project is created for educational purposes.

## 👥 Contributing

Feel free to extend this project with:
- New agent behaviors
- Advanced pathfinding algorithms
- Different maze generation techniques
- Additional visualization features
- More sophisticated negotiation protocols

## 📧 Contact

For questions or issues, please create an issue in the repository or contact the maintainer.

---

**Happy Simulating! 🤖✨**