# config.py - Configuration for Multi-Agent Maze Escape Simulation

# Maze Configuration
MAZE_WIDTH = 46  # Reduced by 4 (2 from each side) - was 50
MAZE_HEIGHT = 46  # Reduced by 4 (2 from each side) - was 50
WALL_DENSITY = 0.3  # Probability of a cell being a wall

# Agent Configuration
NUM_AGENTS = 5
AGENT_ENERGY = 250  # Increased for larger maze
AGENT_VISION_RANGE = 2  # How far agents can see
COMMUNICATION_RANGE = 10  # Increased for larger maze

# Simulation Configuration
MAX_STEPS = 5000  # Increased for larger maze
SIMULATION_SPEED = 3  # Faster default speed for larger maze

# Visualization Configuration
CELL_SIZE = 20  # Smaller cells to fit larger maze on screen
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

# Agent colors for differentiation (supports up to 50 agents)
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
    # Additional 30 colors for 50 total
    (200, 100, 0),    # Brown
    (0, 150, 100),    # Teal
    (150, 0, 150),    # Dark Purple
    (255, 200, 200),  # Pink
    (200, 255, 200),  # Mint
    (200, 200, 255),  # Lavender
    (255, 100, 0),    # Bright Orange
    (100, 0, 255),    # Indigo
    (0, 255, 100),    # Aquamarine
    (255, 50, 50),    # Crimson
    (50, 255, 50),    # Chartreuse
    (50, 50, 255),    # Royal Blue
    (200, 150, 0),    # Mustard
    (150, 0, 100),    # Plum
    (0, 100, 150),    # Steel Blue
    (255, 150, 150),  # Light Coral
    (150, 255, 150),  # Pale Green
    (150, 150, 255),  # Periwinkle
    (255, 180, 100),  # Peach
    (180, 100, 255),  # Orchid
    (100, 255, 180),  # Seafoam
    (255, 80, 80),    # Tomato
    (80, 255, 80),    # Lawn Green
    (80, 80, 255),    # Cornflower Blue
    (230, 180, 0),    # Goldenrod
    (180, 0, 230),    # Violet
    (0, 230, 180),    # Turquoise
    (255, 120, 200),  # Hot Pink
    (120, 200, 255),  # Baby Blue
    (200, 255, 120),  # Yellow Green
]