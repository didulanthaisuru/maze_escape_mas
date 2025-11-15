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
# Make maze bigger
MAZE_WIDTH = 30
MAZE_HEIGHT = 30

# Add more agents
NUM_AGENTS = 10

# Make simulation faster
SIMULATION_SPEED = 20

# Increase agent vision
AGENT_VISION_RANGE = 3
```

## 🎮 Runtime Controls

| Key | Action |
|-----|--------|
| ESC | Exit |
| R | Reset |
| SPACE | Pause/Unpause |

## 📊 Benchmark Options

```bash
# Custom agent counts
python main.py --mode benchmark --agents 1 3 5 10

# More trials (more accurate)
python main.py --mode benchmark --trials 10

# Skip plotting
python main.py --mode benchmark --no-plot
```

## 🔍 Key Classes

### RobotAgent
```python
agent.perceive_environment(maze)    # See surroundings
agent.decide_next_move(maze, bb)    # Choose action
agent.move(target_pos)               # Execute move
agent.share_knowledge(blackboard)   # Communicate
```

### Blackboard
```python
bb.add_explored_cell(pos, agent_id)
bb.add_dead_end(pos, agent_id)
bb.is_explored(pos)
bb.get_best_path()
```

### Simulator
```python
sim.step()                  # One simulation step
sim.run_until_complete()    # Run to completion
sim.get_results()           # Get statistics
```

## 🐛 Common Issues & Fixes

### pygame not found
```bash
pip install pygame==2.5.2
```

### Module not found
```bash
# Make sure you're in maze_escape_mas/
cd maze_escape_mas
python main.py
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

## 📈 Performance Comparison

| Agents | Avg Steps | Improvement |
|--------|-----------|-------------|
| 1 | ~500 | Baseline |
| 3 | ~200 | 2.5x faster |
| 5 | ~150 | 3.3x faster |
| 7 | ~130 | 3.8x faster |

*Results vary based on maze configuration*

## 🧪 Experiment Ideas

1. **Vary agent count**: Test 1, 3, 5, 10, 15 agents
2. **Change maze size**: Try 10x10, 30x30, 50x50
3. **Adjust vision**: Test vision ranges 1, 2, 3, 5
4. **Modify wall density**: Try 0.2, 0.3, 0.4, 0.5
5. **Energy constraints**: Reduce agent energy

## 📝 Code Snippets

### Add New Agent Behavior
```python
# In agents/robot_agent.py
def decide_next_move(self, maze, blackboard):
    # Your custom strategy here
    pass
```

### Modify Negotiation
```python
# In coordination/negotiation.py
@staticmethod
def custom_negotiation(agents, targets):
    # Your negotiation logic
    pass
```

### Change Visualization
```python
# In config.py
COLOR_AGENT = (255, 0, 0)  # Change agent color
CELL_SIZE = 40             # Bigger cells
SIMULATION_SPEED = 5       # Slower/faster
```

## 🎯 Assignment Checklist

- [ ] Project runs successfully
- [ ] Demonstrates communication (blackboard)
- [ ] Shows coordination (task allocation)
- [ ] Implements negotiation (conflict resolution)
- [ ] Exhibits emergent behavior
- [ ] Performance comparison (1 vs multiple agents)
- [ ] Visual demonstration
- [ ] Metrics and analysis
- [ ] Documentation complete

## 💡 Tips

1. **Start small**: Test with 2-3 agents first
2. **Watch the visualization**: Understand agent behavior
3. **Run benchmarks**: Get quantitative results
4. **Modify gradually**: Change one parameter at a time
5. **Document changes**: Keep notes on experiments

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