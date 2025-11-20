# Multi-Agent Maze Escape System 🤖🔍

A comprehensive Multi-Agent System (MAS) demonstration featuring autonomous agents cooperatively exploring complex mazes. This project showcases essential MAS principles including autonomous decision-making, agent communication, distributed problem-solving, and emergent collective intelligence.

## 🎯 Project Overview

**Objective**: Simulate a team of autonomous agents navigating complex procedurally-generated mazes to find the exit while avoiding deadly dead-end traps and sharing knowledge to ensure team survival.

### Key Features

- 🤖 **Autonomous Agents (1-50)**: Independent decision-making with BDI architecture
- 📡 **Real-time Communication**: Broadcast-based message passing (DEAD_END, WRONG_PATH, EXIT_FOUND)
- 🧠 **Emergent Intelligence**: Collective knowledge building from zero initial information
- 🗺️ **Procedural Maze Generation**: Infinite unique mazes using recursive backtracking algorithm
- ⚰️ **Dead End System**: 100+ automatically identified death traps per maze
- 🎯 **BFS Pathfinding**: Optimal path calculation and sharing on exit discovery
- 💀 **Zero Deaths Policy**: After exit found, ALL agents evacuate safely using shared path
- 🎮 **Interactive Controls**: Pause, speed control, single-step debugging, live maze regeneration
- 📊 **Real-time Visualization**: Agent trails, communication broadcasts, message logs
- 🔄 **Adaptive Coordination**: Agents survive failures and adapt to discoveries

## 🏗️ Architecture

```
multi_agent_system/
├── agents/
│   ├── robot_agent.py      # BDI agent with BFS pathfinding & oscillation detection
│   └── communication.py    # Broadcast message protocol (3 message types)
├── coordination/
│   ├── blackboard.py       # Shared knowledge repository
│   └── negotiation.py      # Priority-based conflict resolution
├── environment/
│   ├── maze.py            # Procedural generation + dead end identification
│   └── cell.py            # Cell properties (wall, dead_end, trap, etc.)
├── simulation/
│   ├── simulator.py       # Main game loop & agent lifecycle
│   └── metrics.py         # Performance tracking & statistics
├── visualization/
│   └── renderer.py        # Pygame GUI (46x46 maze, 50 agent colors)
├── config.py              # System configuration (46x46, 1-50 agents)
└── main.py               # Entry point with CLI arguments
```

## 🎮 Quick Start

### Installation

```bash
# Clone the repository
cd multi_agent_system

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pygame numpy matplotlib
```

### Run Simulation

```bash
python main.py
```

**First Launch:**
1. **Agent Selection Screen** appears
2. Use **+/- buttons** or **← → arrows** to select agent count (1-50)
3. Click **START** or press **ENTER** to begin
4. Watch agents explore and communicate!

## ⌨️ Interactive Controls

### During Simulation

| Key | Action | Description |
|-----|--------|-------------|
| **SPACE** | Pause/Resume | Toggle simulation execution |
| **↑** | Speed Up | Increase to 10 steps/sec (max) |
| **↓** | Slow Down | Decrease to 0.5 steps/sec (min) |
| **S** | Single Step | Execute one step (when paused) |
| **R** | Reset | Restart with same maze, select agents again |
| **M** | New Maze | Generate completely new maze layout |
| **ESC** | Quit | Exit simulation |

### During Agent Selection

| Control | Action |
|---------|--------|
| **← →** or **+/- buttons** | Adjust agent count (1-50) |
| **ENTER** or **START button** | Begin simulation |
| **M** | Generate new maze before starting |

### Mouse Controls

- Click **+** button: Increase agents
- Click **-** button: Decrease agents  
- Click **START** button: Begin simulation

## 🎨 Visual Features

### Color Coding

| Element | Color | Meaning |
|---------|-------|---------|
| 🟢 Green Cell | Start | Agent spawn point |
| 🔴 Red/Orange Cell | Exit | Goal location (victims) |
| ⬜ White Cells | Unexplored | Unknown territory |
| 🟦 Light Blue | Explored | Visited by agents |
| ⬛ Dark Gray | Walls | Impassable barriers |
| 🟥 Darker Gray | Dead Ends | Death traps (1 neighbor only) |

### Agent Visualization

- **Colored Circles**: Each agent has unique color (50 colors available)
- **ID Numbers**: Agent identification displayed
- **Faint Trails**: Path history showing movement
- **White Ring**: Agent successfully reached exit
- **Red X + Dark Tint**: Agent died in dead end (☠️)

### Communication Indicators

- **Red Expanding Circle**: DEAD_END warning broadcast
- **Green Expanding Circle**: EXIT_FOUND success broadcast
- **Message Log** (top-right): Last 5 communications displayed

### UI Panels

**Left Sidebar:**
- Agent selection controls
- START button
- Keyboard shortcuts
- Status information (alive/dead/at exit)

**Statistics Display:**
- Step counter
- Simulation speed
- Pause state
- Dead end count

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

### Maze Parameters

The simulation operates on a **46×46 grid** (2,116 cells) with procedural generation:

```python
# config.py
MAZE_WIDTH = 46          # Grid columns
MAZE_HEIGHT = 46         # Grid rows
CELL_SIZE = 15           # Pixel size per cell
```

**Maze Generation:**
- **Fixed Maze**: Guaranteed solvable with verified path (default)
- **Random Maze**: Procedurally generated using recursive backtracking
- **Dead End Detection**: Automatic identification of cells with ≤1 neighbor
- **Typical Dead Ends**: 33 (fixed maze), 100+ (random mazes)

To use random generation:
```bash
python main.py --random-maze
```

### Agent Configuration

Select **1-50 agents** before simulation:

```python
# config.py
AGENT_SPEED = 0.2        # Default speed (overridden by user)
NUM_AGENTS = 1-50        # Selectable range
COLORS_AVAILABLE = 50    # Unique color palette
```

**Agent Capabilities:**
- **BDI Architecture**: Belief-Desire-Intention decision model
- **Communication Range**: Full maze broadcast (blackboard pattern)
- **Memory**: Visited cells, received messages, dead end warnings
- **Pathfinding**: BFS (Breadth-First Search) for optimal evacuation
- **Oscillation Detection**: 10-position sliding window to prevent loops

### Communication Protocol

```python
# Message types in communication.py
MESSAGE_TYPES = {
    'DEAD_END': Red circles,      # Warning broadcast
    'EXIT_FOUND': Green circles,  # Evacuation trigger  
    'WRONG_PATH': Path invalidation
}
```

**Shared Knowledge (Blackboard):**
- Confirmed dead ends
- Invalid paths  
- Exit location (once discovered)
- Optimal evacuation path (BFS-calculated)

### Visualization Settings

```python
# config.py
SCREEN_WIDTH = 1200       # Total window width
SCREEN_HEIGHT = 800       # Total window height
SIDEBAR_WIDTH = 250       # Left panel for controls
FPS = 60                  # Smooth rendering
```

**Performance Notes:**
- **1-10 agents**: Real-time analysis, clear visualization
- **11-30 agents**: Emergent patterns visible, some overlap
- **31-50 agents**: Maximum complexity, collective intelligence testing

## 🧠 Multi-Agent System Features

### 1. Emergent Intelligence
Agents exhibit **collective problem-solving** without central coordination:
- **Parallel Exploration**: Simultaneous searching of multiple paths
- **Information Propagation**: Instant sharing of discoveries via blackboard
- **Adaptive Strategies**: Behavior changes based on shared knowledge
- **Zero Deaths Policy**: Once exit found, all agents evacuate safely using BFS paths

### 2. BDI (Belief-Desire-Intention) Architecture

Each agent operates autonomously using:

**Beliefs:**
- Visited cells (memory)
- Confirmed dead ends
- Received warnings from other agents
- Known exit location (after discovery)

**Desires (Priority System):**
1. **Evacuate** (highest) - Follow BFS path to exit when discovered
2. **Explore Unexplored** - Prioritize unknown territory
3. **Escape Oscillation** - Break out of loops
4. **Try Unvisited** - Search new cells
5. **Backtrack** - Retreat from dead ends
6. **Random Move** (last resort) - Prevent complete stagnation

**Intentions:**
- Pathfinding to chosen target
- Broadcasting discoveries
- Avoiding confirmed dead ends (except during evacuation)

### 3. Communication & Coordination

**Message Types:**
- 🔴 **DEAD_END**: Warning about death traps (1 neighbor cells)
- 🟢 **EXIT_FOUND**: Triggers immediate evacuation for all agents
- ⚠️ **WRONG_PATH**: Invalidates previously suggested routes

**Blackboard Pattern:**
- **Global Knowledge Base**: All agents read/write to shared memory
- **No Central Controller**: Fully distributed decision-making
- **Instant Propagation**: Exit discovery reaches all agents immediately
- **Conflict-Free**: Read operations concurrent, writes atomic

**Coordination Behaviors:**
- **No Redundancy**: Agents avoid re-exploring marked dead ends
- **Dynamic Reassignment**: Oscillation detection forces new target selection
- **Collective Memory**: Each exploration contributes to group knowledge

### 4. Advanced Pathfinding

**BFS Evacuation System:**
- **Activation**: Triggered when ANY agent finds exit
- **Path Calculation**: Optimal route computed from each agent's position to exit
- **Dead End Traversal**: During evacuation, agents CAN pass through dead ends to reach safe path
- **Guaranteed Safety**: Agents with exit path NEVER die, even if stuck

**Oscillation Prevention:**
- **Sliding Window**: Tracks last 10 positions
- **Loop Detection**: Identifies repeated position patterns
- **Stuck Counter**: Escalates to random moves after 5 loops
- **Forced Randomization**: Breaks infinite cycles

### 5. Emergent Behavior Examples

**Pattern Formation:**
- Agents naturally spread across unexplored regions
- Concentration increases near promising paths
- Rapid convergence after exit discovery

**Knowledge Cascade:**
1. Agent A discovers dead end → broadcasts warning
2. Agents B, C, D receive warning → avoid that path
3. Agent E finds exit → broadcasts location
4. All agents calculate BFS paths → synchronized evacuation
5. Zero deaths post-discovery (evacuation priority overrides death checks)

## 📊 Performance Metrics

The benchmark mode analyzes multi-agent system efficiency:

### Metrics Collected
- **Steps to Completion**: Total steps until all agents exit (or simulation ends)
- **Exploration Coverage**: Percentage of 2,116 cells visited
- **Success Rate**: Percentage of trials where exit was found
- **Computation Time**: Real-world execution time
- **Dead Ends Encountered**: Number of death traps discovered
- **Agent Survival Rate**: Percentage alive when exit found

### Running Benchmarks

```bash
# Test with default agent counts [1, 2, 3, 5, 7]
python main.py --mode benchmark

# Test specific agent counts
python main.py --mode benchmark --agents 1 10 25 50

# Run more trials for statistical accuracy
python main.py --mode benchmark --agents 1 5 10 --trials 10

# Disable plotting
python main.py --mode benchmark --no-plot

# Use random maze for benchmarking
python main.py --mode benchmark --random-maze
```

### Sample Output (46×46 Maze):
```
============================================================
PERFORMANCE SUMMARY
============================================================

1 Agent:
  Average Steps:     1247.3
  Average Explored:  423.7 (20.0%)
  Success Rate:      100.0%
  Average Duration:  1.234s
  Dead Ends Found:   12

10 Agents:
  Average Steps:     387.2
  Average Explored:  891.4 (42.1%)
  Success Rate:      100.0%
  Average Duration:  0.892s
  Dead Ends Found:   28
  Avg. Survival Rate: 87.5%

50 Agents:
  Average Steps:     142.8
  Average Explored:  1456.9 (68.8%)
  Success Rate:      100.0%
  Average Duration:  0.634s
  Dead Ends Found:   33
  Avg. Survival Rate: 76.3%

OPTIMAL CONFIGURATIONS:
  Fewest Steps:       50 agents (142.8 steps)
  Fastest Execution:  50 agents (0.634s)
  Best Coverage:      50 agents (68.8%)
============================================================
```

### Interpretation

**Scalability Analysis:**
- **More Agents → Faster Discovery**: Parallel exploration reduces steps exponentially
- **Coverage Trade-off**: Larger teams explore more but may converge prematurely
- **Survival Rate**: Higher agent counts → more dead end encounters before exit found

**Emergent Patterns:**
- **Diminishing Returns**: 30-50 agents show similar performance (saturation point)
- **Communication Overhead**: Minimal impact due to blackboard efficiency
- **Optimal Team Size**: 10-20 agents balance speed and visualization clarity

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

This project demonstrates essential Multi-Agent Systems (MAS) concepts for educational and research purposes:

### Core MAS Principles

**1. Distributed Intelligence**
- No central controller - fully autonomous agents
- Emergent problem-solving from local interactions
- Scalability testing with 1-50 agents

**2. Agent Architecture**
- **BDI Model**: Belief-Desire-Intention framework implementation
- **Reactive + Deliberative**: Combines reflex actions with goal-directed planning
- **Memory-Based**: Agents maintain visited cells, warnings, and shared knowledge

**3. Communication Protocols**
- **Blackboard Pattern**: Shared memory architecture for global coordination
- **Broadcast Messaging**: Instant information propagation across entire system
- **Three Message Types**: DEAD_END, EXIT_FOUND, WRONG_PATH

**4. Coordination Mechanisms**
- **Dynamic Task Allocation**: Agents self-organize to explore different branches
- **Redundancy Avoidance**: Collective memory prevents duplicate exploration
- **Priority-Based Decision**: 6-level intention hierarchy for conflict resolution

**5. Emergent Intelligence**
- **Swarm Behavior**: Parallel exploration patterns without explicit coordination
- **Knowledge Cascade**: Single discovery triggers system-wide response
- **Collective Optimization**: Group outperforms individual (50 agents → 10x faster than 1)

### Computational Models

**Search Strategies:**
- **Depth-First Exploration**: Individual agent behavior
- **Breadth-First Evacuation**: BFS pathfinding post-discovery
- **Hybrid Approach**: DFS for exploration + BFS for optimization

**Problem Complexity:**
- **State Space**: 2,116 cells × 50 agents = massive search space
- **Dead End Detection**: Topological analysis (neighbor counting)
- **Oscillation Prevention**: Pattern recognition in movement history

### Research Applications

**Testbed for:**
- Agent architecture comparison (BDI vs. reactive vs. utility-based)
- Communication protocol efficiency (blackboard vs. peer-to-peer)
- Scalability analysis (1-50 agents performance curves)
- Emergent behavior observation (swarm intelligence, collective decision-making)
- Coordination strategy testing (distributed vs. centralized approaches)

**Learning Outcomes:**
- Understanding agent autonomy vs. coordination trade-offs
- Implementing shared knowledge bases (blackboard pattern)
- Analyzing emergent intelligence from simple rules
- Measuring multi-agent system performance metrics
- Visualizing complex agent interactions in real-time

## 📈 Expected Outcomes

### Performance Characteristics

**Single Agent (Baseline):**
- **Steps to Exit**: 800-1500 steps (depends on maze complexity)
- **Exploration**: 15-25% of maze before finding exit
- **Strengths**: Deterministic, complete coverage if time allowed
- **Weaknesses**: Slow, prone to dead end loops

**Small Teams (2-10 Agents):**
- **Steps to Exit**: 300-600 steps (2-3x improvement)
- **Exploration**: 30-50% coverage
- **Emergent Behavior**: Natural spreading across unexplored regions
- **Trade-offs**: Occasional dead end deaths, but collective success

**Medium Teams (11-30 Agents):**
- **Steps to Exit**: 150-350 steps (5-8x improvement)
- **Exploration**: 50-70% coverage
- **Emergent Behavior**: Rapid dead end identification, coordinated evacuation
- **Trade-offs**: Visual overlap, but emergent patterns clearly visible

**Large Teams (31-50 Agents):**
- **Steps to Exit**: 100-200 steps (8-15x improvement)
- **Exploration**: 65-85% coverage
- **Emergent Behavior**: Swarm-like exploration, instant information propagation
- **Trade-offs**: Complex visualization, but maximum collective intelligence

### Demonstrated MAS Properties

**Cooperation:**
- Exit discovery by ONE agent saves ALL agents (zero post-discovery deaths)
- Dead end warnings prevent teammates from repeating mistakes
- Shared blackboard eliminates redundant exploration

**Emergent Intelligence:**
- System-level optimization without central planning
- Parallel exploration reduces search time exponentially
- Knowledge cascade: single discovery → instant system-wide response

**Scalability:**
- Performance improves with agent count (diminishing returns after ~30)
- Communication overhead minimal (blackboard pattern efficiency)
- Graceful degradation: even if 50% die, remaining agents complete mission

**Synergy:**
- **10 agents ≠ 10x single agent**: Collective intelligence provides exponential gains
- Coordination benefits exceed individual capabilities
- Whole greater than sum of parts (classic emergent property)

## 🛠️ Extending the Project

### Add New Agent Types

Edit `agents/robot_agent.py` to create specialized agents:

```python
class ScoutAgent(RobotAgent):
    """Fast agent with extended perception"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vision_range = 4  # Extended vision
        self.speed_multiplier = 1.5  # Faster movement
```

### Implement Alternative Communication Protocols

Modify `coordination/communication.py`:

```python
class PeerToPeerCommunication:
    """Direct agent-to-agent messaging with range limits"""
    def __init__(self, range_limit=5):
        self.range_limit = range_limit
        
    def broadcast_in_range(self, sender, message, agents):
        """Send message only to nearby agents"""
        for agent in agents:
            if distance(sender, agent) <= self.range_limit:
                agent.receive_message(message)
```

### Add Dynamic Maze Elements

Extend `environment/maze.py`:

```python
class DynamicMaze(Maze):
    """Maze with moving walls or hazards"""
    def add_moving_obstacles(self):
        """Implement moving walls"""
        pass
        
    def add_fog_of_war(self):
        """Cells only visible when nearby"""
        pass
```

### Create Custom Coordination Strategies

Add to `coordination/negotiation.py`:

```python
@staticmethod
def auction_based_allocation(agents, targets):
    """Auction-based task allocation with bidding"""
    bids = {}
    for target in targets:
        bids[target] = [(agent, agent.calculate_bid(target)) 
                        for agent in agents]
        bids[target].sort(key=lambda x: x[1], reverse=True)
    return assign_winners(bids)
```

### Experiment with Alternative Pathfinding

Modify `agents/robot_agent.py`:

```python
def a_star_pathfinding(self, start, goal):
    """A* algorithm instead of BFS"""
    # Implement heuristic-based search
    # Useful for larger mazes or weighted paths
    pass
```

## 📝 Academic Use Cases

This project is suitable for demonstrating:

### Assignment Requirements
1. ✅ **Multi-agent communication** - Blackboard pattern with 3 message types
2. ✅ **Coordination and cooperation** - BFS evacuation, shared knowledge
3. ✅ **Negotiation protocols** - Priority-based decision-making
4. ✅ **Emergent behavior** - Swarm intelligence, knowledge cascades
5. ✅ **Performance analysis** - Benchmark mode with statistical metrics
6. ✅ **Scalability testing** - 1-50 agents with performance curves
7. ✅ **Visual demonstration** - Real-time Pygame visualization

### Research Questions to Explore
- How does agent count affect exploration efficiency?
- What's the optimal communication range vs. full broadcast?
- Can different agent types (scouts, mappers) improve performance?
- How does maze complexity (dead end density) affect agent survival?
- What's the trade-off between exploration thoroughness and speed?

### Presentation Material
- 🎥 **Live Demo**: Interactive simulation with M key for regeneration
- 📊 **Benchmark Graphs**: Performance comparison across agent counts
- 🧮 **Metrics Dashboard**: Real-time statistics and message logs
- 📸 **Screenshots**: Dead end detection, evacuation visualization, emergent patterns

## 🐛 Troubleshooting

### Pygame Window Not Appearing

```bash
# Reinstall pygame with correct version
pip uninstall pygame
pip install pygame==2.6.1
```

**macOS-specific:**
```bash
# If window still doesn't appear
pip install --upgrade pygame
# Ensure Python is framework build
python -m pygame.examples.aliens
```

### Matplotlib Backend Errors

```bash
# Install required backends
pip install matplotlib pillow
# On macOS, use TkAgg backend
export MPLBACKEND=TkAgg
```

### Agent Selection Screen Issues

**Problem:** Can't see agent selection controls  
**Solution:** Ensure `SIDEBAR_WIDTH = 250` in `config.py`

**Problem:** Keyboard controls (← →) not working  
**Solution:** Click on Pygame window to focus it first

### Performance Issues

**Large agent counts slow down:**
```python
# In config.py, reduce rendering overhead
FPS = 30  # Default is 60
CELL_SIZE = 12  # Smaller cells for better performance
```

**Benchmark mode takes too long:**
```bash
# Reduce trials
python main.py --mode benchmark --trials 3
# Or test fewer agent counts
python main.py --mode benchmark --agents 1 10 25
```

### Common Errors

**ImportError: No module named 'pygame'**
```bash
pip install pygame numpy matplotlib
```

**Permission denied when saving benchmarks**
```bash
# Ensure write permissions
chmod +w benchmark_results/
# Or run from virtual environment
```

**Maze generation hangs**
```bash
# Use fixed maze instead of random
python main.py  # Default uses fixed maze
# Random generation may take longer for complex mazes
```

### Virtual Environment Setup (Recommended)

```bash
# Create isolated environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

## 📚 References

### Multi-Agent Systems Theory
- **Wooldridge, M. (2009).** *An Introduction to MultiAgent Systems (2nd ed.)*. Wiley.
  - Chapters on agent architectures, communication, and coordination
- **Russell, S., & Norvig, P. (2020).** *Artificial Intelligence: A Modern Approach (4th ed.)*. Pearson.
  - Sections on intelligent agents and multi-agent decision-making
- **Ferber, J. (1999).** *Multi-Agent Systems: An Introduction to Distributed Artificial Intelligence*. Addison-Wesley.

### Specific Techniques Implemented
- **BDI Architecture:** Rao, A. S., & Georgeff, M. P. (1995). "BDI Agents: From Theory to Practice."
- **Blackboard Pattern:** Corkill, D. D. (1991). "Blackboard Systems." *AI Expert*, 6(9), 40-47.
- **Pathfinding Algorithms:** Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for Heuristic Determination of Minimum Cost Paths." *IEEE Transactions on Systems Science and Cybernetics*.

### Maze Generation
- **Recursive Backtracking:** Based on depth-first search maze generation algorithms
- **Dead End Analysis:** Topological graph analysis for connectivity detection

### Python Libraries Used
- **Pygame 2.6.1**: Game development and visualization
- **NumPy**: Numerical computations and array operations
- **Matplotlib**: Performance benchmarking and plotting

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