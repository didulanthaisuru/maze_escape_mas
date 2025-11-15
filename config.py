# config.py - Configuration for Multi-Agent Maze Escape Simulation

# Maze Configuration
MAZE_WIDTH = 20
MAZE_HEIGHT = 20
WALL_DENSITY = 0.3  # Probability of a cell being a wall

# Agent Configuration
NUM_AGENTS = 5
AGENT_ENERGY = 100
AGENT_VISION_RANGE = 2  # How far agents can see
COMMUNICATION_RANGE = 5  # How far agents can communicate

# Simulation Configuration
MAX_STEPS = 1000
SIMULATION_SPEED = 10  # Steps per second

# Visualization Configuration
CELL_SIZE = 30
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
COLOR_TEXT = (0, 0, 0)

# Agent colors for differentiation
AGENT_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 128, 0),  # Orange
    (128, 0, 255),  # Purple
]