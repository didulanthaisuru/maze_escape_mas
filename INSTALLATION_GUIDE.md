# Installation Guide - Multi-Agent Maze Escape Simulation

Complete step-by-step guide to get your project running locally from scratch.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Option 1: Automated Setup](#option-1-automated-setup)
3. [Option 2: Manual Setup](#option-2-manual-setup)
4. [Creating Python Files](#creating-python-files)
5. [Running the Simulation](#running-the-simulation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Git** (optional) - For version control

### Verify Installation
Open terminal/command prompt and run:
```bash
python --version
pip --version
```

You should see version numbers. If not, reinstall Python.

---

## Option 1: Automated Setup

### Linux/Mac

1. **Download the setup script** (setup.sh from artifacts)

2. **Make it executable:**
```bash
chmod +x setup.sh
```

3. **Run the script:**
```bash
./setup.sh
```

4. **Follow the prompts** - choose whether to create a virtual environment

### Windows

1. **Download the setup script** (setup.bat from artifacts)

2. **Run it:**
```cmd
setup.bat
```

3. **Follow the prompts**

---

## Option 2: Manual Setup

### Step 1: Create Project Directory

```bash
# Create main project folder
mkdir maze_escape_mas
cd maze_escape_mas
```

### Step 2: Create Folder Structure

```bash
# Linux/Mac
mkdir -p environment agents coordination simulation visualization utils

# Windows (in cmd)
mkdir environment agents coordination simulation visualization utils
```

### Step 3: Create __init__.py Files

**Linux/Mac:**
```bash
touch environment/__init__.py
touch agents/__init__.py
touch coordination/__init__.py
touch simulation/__init__.py
touch visualization/__init__.py
touch utils/__init__.py
```

**Windows (in PowerShell):**
```powershell
New-Item -ItemType File -Path environment/__init__.py
New-Item -ItemType File -Path agents/__init__.py
New-Item -ItemType File -Path coordination/__init__.py
New-Item -ItemType File -Path simulation/__init__.py
New-Item -ItemType File -Path visualization/__init__.py
New-Item -ItemType File -Path utils/__init__.py
```

**Windows (in cmd):**
```cmd
type nul > environment\__init__.py
type nul > agents\__init__.py
type nul > coordination\__init__.py
type nul > simulation\__init__.py
type nul > visualization\__init__.py
type nul > utils\__init__.py
```

### Step 4: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Linux/Mac:
source venv/bin/activate

# Windows (cmd):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt.

### Step 5: Install Dependencies

Create `requirements.txt`:
```bash
# Linux/Mac
cat > requirements.txt << EOF
pygame==2.5.2
numpy==1.24.3
matplotlib==3.7.1
EOF

# Windows - create file manually or:
echo pygame==2.5.2 > requirements.txt
echo numpy==1.24.3 >> requirements.txt
echo matplotlib==3.7.1 >> requirements.txt
```

Install packages:
```bash
pip install -r requirements.txt
```

Verify installation:
```bash
python -c "import pygame, numpy, matplotlib; print('Success!')"
```

---

## Creating Python Files

Now you need to create all the Python files. Here's the complete list:

### Root Directory Files
1. `main.py` - Main entry point
2. `config.py` - Configuration settings
3. `requirements.txt` - Dependencies
4. `README.md` - Documentation

### Environment Package
1. `environment/__init__.py` - Package init
2. `environment/cell.py` - Cell class
3. `environment/maze.py` - Maze generation

### Agents Package
1. `agents/__init__.py` - Package init
2. `agents/robot_agent.py` - Robot agent class

### Coordination Package
1. `coordination/__init__.py` - Package init
2. `coordination/blackboard.py` - Shared knowledge
3. `coordination/negotiation.py` - Conflict resolution

### Simulation Package
1. `simulation/__init__.py` - Package init
2. `simulation/simulator.py` - Simulation logic
3. `simulation/metrics.py` - Performance metrics

### Visualization Package
1. `visualization/__init__.py` - Package init
2. `visualization/renderer.py` - Pygame rendering

### Utils Package
1. `utils/__init__.py` - Package init (can be empty)

### How to Create Files

**Method 1: Copy from Artifacts**
I've provided all file contents in separate artifacts above. Copy each one into its respective file.

**Method 2: Using Text Editor**
1. Open your favorite text editor (VS Code, PyCharm, Sublime, etc.)
2. Create each file in the correct location
3. Paste the content from the artifacts

**Method 3: Command Line**
```bash
# Example for creating and editing a file
nano environment/cell.py  # Linux/Mac
notepad environment\cell.py  # Windows
```

### File Checklist
Use this checklist to ensure all files are created:

```
maze_escape_mas/
├── [✓] main.py
├── [✓] config.py
├── [✓] requirements.txt
├── [✓] README.md
├── environment/
│   ├── [✓] __init__.py
│   ├── [✓] cell.py
│   └── [✓] maze.py
├── agents/
│   ├── [✓] __init__.py
│   └── [✓] robot_agent.py
├── coordination/
│   ├── [✓] __init__.py
│   ├── [✓] blackboard.py
│   └── [✓] negotiation.py
├── simulation/
│   ├── [✓] __init__.py
│   ├── [✓] simulator.py
│   └── [✓] metrics.py
├── visualization/
│   ├── [✓] __init__.py
│   └── [✓] renderer.py
└── utils/
    └── [✓] __init__.py
```

---

## Running the Simulation

### 1. Verify Your Setup

```bash
# Check Python can find all modules
python -c "from environment import Maze; print('Environment: OK')"
python -c "from agents import RobotAgent; print('Agents: OK')"
python -c "from coordination import Blackboard; print('Coordination: OK')"
python -c "from simulation import Simulator; print('Simulation: OK')"
python -c "from visualization import Renderer; print('Visualization: OK')"
```

All should print "OK".

### 2. Run Visual Mode

```bash
python main.py
```

A pygame window should open showing the simulation.

### 3. Run Benchmark Mode

```bash
python main.py --mode benchmark
```

This will run performance tests and generate a comparison chart.

### 4. View Help

```bash
python main.py --help
```

---

## Troubleshooting

### Problem: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'pygame'
```

**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall:
pip install --upgrade pygame numpy matplotlib
```

### Problem: Import Error for Local Modules

**Error:**
```
ModuleNotFoundError: No module named 'environment'
```

**Solution:**
```bash
# Make sure you're in the maze_escape_mas directory
cd maze_escape_mas

# Check __init__.py files exist
ls */__init__.py  # Linux/Mac
dir *\__init__.py  # Windows

# Run from project root
python main.py
```

### Problem: Pygame Window Doesn't Appear

**Solution 1 - Reinstall pygame:**
```bash
pip uninstall pygame
pip install pygame==2.5.2
```

**Solution 2 - Check display (Linux):**
```bash
export DISPLAY=:0
```

**Solution 3 - Try headless mode:**
Run benchmark instead:
```bash
python main.py --mode benchmark --no-plot
```

### Problem: Permission Denied on Linux/Mac

**Solution:**
```bash
chmod +x setup.sh
chmod +x main.py
```

### Problem: Python Not Found

**Windows - Add Python to PATH:**
1. Search for "Environment Variables"
2. Edit PATH
3. Add Python installation directory
4. Restart terminal

**Mac - Use Python 3:**
```bash
python3 main.py
pip3 install -r requirements.txt
```

### Problem: Virtual Environment Issues

**Deactivate and recreate:**
```bash
deactivate  # If activated
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## Verification Checklist

Before running, verify:

- [ ] Python 3.8+ installed
- [ ] All folders created
- [ ] All `.py` files created with correct content
- [ ] All `__init__.py` files exist
- [ ] `requirements.txt` exists
- [ ] Dependencies installed (`pip list` shows pygame, numpy, matplotlib)
- [ ] Virtual environment activated (if using)
- [ ] Current directory is `maze_escape_mas`

---

## Next Steps

Once everything is working:

1. ✅ **Run visual mode** - See the simulation in action
2. ✅ **Run benchmark mode** - Compare performance
3. ✅ **Modify config.py** - Experiment with different parameters
4. ✅ **Read the code** - Understand the implementation
5. ✅ **Extend the project** - Add your own features

---

## Getting Help

If you're still stuck:

1. **Check file contents** - Make sure all code is copied correctly
2. **Read error messages** - They usually point to the problem
3. **Google the error** - Someone likely had the same issue
4. **Check Python version** - Must be 3.8 or higher

---

## Success! 🎉

If you see the pygame window with moving agents, congratulations! You've successfully set up a multi-agent system simulation.

**What you've built:**
- A complete multi-agent system
- Visual simulation with pygame
- Performance benchmarking tools
- Extensible architecture for future enhancements

Now you can demonstrate:
- Agent communication
- Coordination strategies
- Negotiation protocols
- Emergent behavior
- Performance analysis

Good luck with your assignment! 🚀