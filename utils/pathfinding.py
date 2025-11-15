# Helper algorithms for pathfinding

from collections import deque
import heapq


def bfs(start, goal, maze):
    """
    Breadth-First Search pathfinding algorithm
    
    Args:
        start: Starting position (x, y)
        goal: Goal position (x, y)
        maze: Maze object
    
    Returns:
        List of positions representing the path, or None if no path exists
    """
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        # TODO: Explore neighbors
        # for neighbor in get_neighbors(current, maze):
        #     if neighbor not in visited:
        #         visited.add(neighbor)
        #         parent[neighbor] = current
        #         queue.append(neighbor)
    
    return None


def a_star(start, goal, maze):
    """
    A* pathfinding algorithm
    
    Args:
        start: Starting position (x, y)
        goal: Goal position (x, y)
        maze: Maze object
    
    Returns:
        List of positions representing the path, or None if no path exists
    """
    def heuristic(pos1, pos2):
        # Manhattan distance
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        # TODO: Explore neighbors
        # for neighbor in get_neighbors(current, maze):
        #     tentative_g_score = g_score[current] + 1
        #     
        #     if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
        #         came_from[neighbor] = current
        #         g_score[neighbor] = tentative_g_score
        #         f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
        #         heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None


def get_neighbors(position, maze):
    """
    Get valid neighboring positions
    
    Args:
        position: Current position (x, y)
        maze: Maze object
    
    Returns:
        List of valid neighboring positions
    """
    # TODO: Implement neighbor finding based on maze walls
    neighbors = []
    return neighbors
