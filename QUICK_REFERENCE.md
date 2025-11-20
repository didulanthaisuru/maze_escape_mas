# Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Run
python main.py                    # Visual mode
python main.py --mode benchmark   # Performance testing
python main.py --help            # Show options
```

## 📁 File Structure Summary

```
maze_escape_mas/
├── config.py              # Configure maze size, agents, etc.
├── main.py               # Run this!
├── requirements.txt      # Dependencies
│
├── environment/          # Maze representation
│   ├── maze.py          # Maze generation
│   └── cell.py          # Grid cells
│
├── agents/               # Robot agents
│   └── robot_agent.py   # Agent behavior
│
├── coordination/         # MAS coordination
│   ├── blackboard.py    # Shared knowledge
│   └── negotiation.py   # Conflict resolution
│
├── simulation/           # Simulation engine
│   ├── simulator.py     # Main logic
│   └── metrics.py       # Performance analysis
│
└── visualization/        # Display
    └── renderer.py      # Pygame rendering
```

## ⚙️ Configuration Quick Edit

Edit `config.py`:

```python
# Maze size (46x46 default)
MAZE_WIDTH = 46
MAZE_HEIGHT = 46

# Agent selection (1-50 agents)
# Selected interactively before simulation

# Make simulation faster
SIMULATION_SPEED = 10  # Steps per second

# Cell size for visualization
CELL_SIZE = 15  # Pixels per cell
```

## 🎮 Runtime Controls

### During Simulation

| Key | Action |
|-----|--------|
| **ESC** | Exit simulation |
| **R** | Reset (reselect agents) |
| **M** | Generate new maze |
| **SPACE** | Pause/Resume |
| **↑** | Speed up (max 10 steps/sec) |
| **↓** | Slow down (min 0.5 steps/sec) |
| **S** | Single step (when paused) |

### During Agent Selection

| Control | Action |
|---------|--------|
| **← →** or **+/- buttons** | Adjust agent count (1-50) |
| **ENTER** or **START button** | Begin simulation |
| **M** | Generate new maze |

## 📊 Benchmark Options

```bash
# Custom agent counts
python main.py --mode benchmark --agents 1 10 25 50

# More trials (more accurate)
python main.py --mode benchmark --trials 10

# Skip plotting
python main.py --mode benchmark --no-plot

# Use random maze instead of fixed
python main.py --mode benchmark --random-maze
```

## 🔍 Key Classes

### RobotAgent (BDI Architecture)
```python
agent.perceive_environment(maze)    # Update beliefs
agent.decide_next_move(maze, bb)    # Choose intention based on desires
agent.move(target_pos)               # Execute move
agent.broadcast_message(msg_type)   # Communicate discovery
```

**Key Features:**
- **Beliefs**: Visited cells, dead ends, exit location
- **Desires**: Evacuate > Explore > Escape loops > Backtrack
- **Intentions**: BFS pathfinding, oscillation avoidance

### Blackboard (Shared Knowledge)
```python
bb.add_explored_cell(pos, agent_id)
bb.add_dead_end(pos, agent_id)
bb.mark_exit_found(pos)
bb.get_exit_path_bfs(start_pos)  # Calculate optimal evacuation route
```

### Maze
```python
maze.generate()                     # Create procedural maze
maze.get_dead_ends()               # Get identified dead ends
maze.is_valid_move(pos, direction) # Check if move allowed
```

### Simulator
```python
sim.step()                  # One simulation step
sim.run_until_complete()    # Run to completion
sim.get_metrics()           # Get statistics (steps, survival rate, etc.)
```

## 🐛 Common Issues & Fixes

### pygame not found
```bash
pip install pygame==2.6.1
```

### Agent selection not responding
- **Click on Pygame window first** to ensure it has focus
- Use mouse buttons or keyboard (← → ENTER)

### Maze generation seems stuck
```bash
# Use fixed maze (default - faster)
python main.py

# Random maze may take longer
python main.py --random-maze
```

### Window doesn't appear
```bash
# Try benchmark mode instead
python main.py --mode benchmark
```

### Import errors
```bash
# Check all __init__.py files exist
ls */__init__.py  # Mac/Linux
dir *\__init__.py  # Windows
```

### M key not generating new maze
- Ensure Pygame window has focus (click on it)
- M works during agent selection AND during simulation

## 📈 Performance Comparison (46×46 Maze)

| Agents | Avg Steps | Exploration | Improvement |
|--------|-----------|-------------|-------------|
| 1 | ~1200 | ~20% | Baseline |
| 10 | ~400 | ~42% | 3x faster |
| 25 | ~220 | ~58% | 5.5x faster |
| 50 | ~150 | ~70% | 8x faster |

*Results vary based on maze configuration and dead end density*

**Key Observations:**
- **Diminishing returns** after 30 agents
- **More exploration** with larger teams
- **Zero deaths** after exit discovered (BFS evacuation)

## 🧪 Experiment Ideas

1. **Vary agent count**: Test 1, 5, 10, 25, 50 agents (performance curves)
2. **Compare mazes**: Fixed vs. random maze generation
3. **Dead end analysis**: Count how many dead ends each agent type encounters
4. **Evacuation efficiency**: Measure steps from EXIT_FOUND to all agents safe
5. **Oscillation frequency**: Track how often agents get stuck in loops
6. **Survival rates**: Compare agent survival across different team sizes
7. **Communication impact**: Disable/enable different message types

## 📝 Code Snippets

### Add New Agent Behavior
```python
# In agents/robot_agent.py
def decide_next_move(self, maze, blackboard):
    # Check evacuation first (highest priority)
    if self.should_evacuate and self.exit_path:
        return self._follow_evacuation_path()
    
    # Your custom exploration strategy here
    if self.custom_condition():
        return self.custom_behavior()
    
    # Fall back to default
    return super().decide_next_move(maze, blackboard)
```

### Modify Communication Protocol
```python
# In coordination/communication.py
def broadcast_custom_message(self, message_type, data):
    """Add new message types beyond DEAD_END, EXIT_FOUND, WRONG_PATH"""
    message = {
        'type': message_type,
        'sender_id': self.agent_id,
        'data': data,
        'timestamp': self.current_step
    }
    self.blackboard.add_message(message)
```

### Change Visualization
```python
# In config.py
# Agent colors (50 unique colors available)
# Dead end color
COLOR_DEAD_END = (80, 80, 80)

# Exploration color
COLOR_EXPLORED = (200, 220, 255)

# Cell size (smaller = fit more on screen)
CELL_SIZE = 15

# Simulation speed
SIMULATION_SPEED = 5  # Steps per second
```

### Custom Pathfinding
```python
# In agents/robot_agent.py
def custom_pathfinding(self, start, goal):
    """Replace BFS with A* or other algorithm"""
    from collections import deque
    
    # Implement A* with heuristic
    # h(n) = Manhattan distance to goal
    # f(n) = g(n) + h(n)
    pass
```

## 🎯 Assignment Checklist

- [ ] Project runs successfully (interactive mode)
- [ ] Agent selection works (1-50 agents, keyboard/mouse controls)
- [ ] Demonstrates communication (DEAD_END, EXIT_FOUND, WRONG_PATH messages)
- [ ] Shows coordination (BFS evacuation, blackboard pattern)
- [ ] Implements negotiation (BDI priority system)
- [ ] Exhibits emergent behavior (swarm exploration, knowledge cascade)
- [ ] Performance comparison (benchmark mode with multiple agent counts)
- [ ] Visual demonstration (M key for maze regeneration, live statistics)
- [ ] Metrics and analysis (steps, exploration %, survival rate)
- [ ] Documentation complete (README, QUICK_REFERENCE updated)
- [ ] Dead end detection (automatic identification and visualization)
- [ ] Zero deaths policy (evacuation priority after exit found)

## 💡 Tips

1. **Start small**: Test with 3-5 agents first to understand behavior
2. **Watch the visualization**: See dead ends (dark gray), explored cells (blue)
3. **Run benchmarks**: Compare 1, 10, 25, 50 agents for quantitative results
4. **Use M key**: Generate multiple mazes to see different dead end patterns
5. **Document changes**: Keep notes on performance differences
6. **Test evacuation**: Watch how all agents coordinate after exit discovery
7. **Monitor messages**: Top-right message log shows communication patterns

## 🔗 Related Files

- **README.md** - Full documentation
- **INSTALLATION_GUIDE.md** - Setup instructions
- **config.py** - All parameters
- **main.py** - Entry point

## 📞 Support

If stuck:
1. Check INSTALLATION_GUIDE.md
2. Read error messages carefully
3. Verify all files are created
4. Ensure dependencies installed
5. Check Python version (3.8+)

---

**Happy Coding! 🚀**