# config.py - Configuration for Multi-Agent Maze Escape Simulation

# Maze Configuration
MAZE_WIDTH = 30  # Increased for more complexity
MAZE_HEIGHT = 30  # Increased for more complexity
WALL_DENSITY = 0.3  # Probability of a cell being a wall

# Agent Configuration
NUM_AGENTS = 5
AGENT_ENERGY = 150  # Increased for larger maze
AGENT_VISION_RANGE = 2  # How far agents can see
COMMUNICATION_RANGE = 8  # Increased for larger maze

# Simulation Configuration
MAX_STEPS = 2000  # Increased for larger maze
SIMULATION_SPEED = 3  # Faster default speed for larger maze

# Visualization Configuration
CELL_SIZE = 25  # Smaller cells to fit larger maze
WINDOW_WIDTH = MAZE_WIDTH * CELL_SIZE
WINDOW_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 100  # Extra space for info panel
FPS = 60

# Colors (RGB)
COLOR_WALL = (50, 50, 50)
COLOR_PATH = (255, 255, 255)
COLOR_START = (100, 200, 100)
COLOR_EXIT = (200, 100, 100)
COLOR_EXPLORED = (200, 200, 255)
COLOR_AGENT = (0, 100, 255)
COLOR_DEAD_END = (150, 150, 150)
COLOR_TRAP = (100, 50, 50)  # Dark red for trap cells (no escape)
COLOR_TEXT = (0, 0, 0)

# Agent colors for differentiation (supports up to 20 agents)
AGENT_COLORS = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    (255, 128, 0),    # Orange
    (128, 0, 255),    # Purple
    (255, 128, 128),  # Light Red
    (128, 255, 128),  # Light Green
    (128, 128, 255),  # Light Blue
    (255, 200, 0),    # Gold
    (200, 0, 200),    # Dark Magenta
    (0, 200, 200),    # Dark Cyan
    (255, 100, 100),  # Salmon
    (100, 255, 100),  # Lime
    (100, 100, 255),  # Sky Blue
    (255, 150, 50),   # Dark Orange
    (150, 50, 255),   # Blue Violet
    (50, 255, 150),   # Spring Green
]