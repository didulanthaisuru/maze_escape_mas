# visualization/renderer.py

import pygame
import config

class Renderer:
    """Handles visualization using pygame"""
    
    def __init__(self, maze, simulator):
        pygame.init()
        self.maze = maze
        self.simulator = simulator
        
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("Multi-Agent Maze Escape Simulation")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
    def draw_maze(self):
        """Draw the maze grid"""
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.get_cell(x, y)
                rect = pygame.Rect(
                    x * config.CELL_SIZE,
                    y * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE
                )
                
                # Determine cell color
                if cell.is_wall:
                    color = config.COLOR_WALL
                elif cell.is_exit:
                    color = config.COLOR_EXIT
                elif cell.is_start:
                    color = config.COLOR_START
                elif cell.is_dead_end:
                    color = config.COLOR_DEAD_END
                elif len(cell.explored_by) > 0:
                    color = config.COLOR_EXPLORED
                else:
                    color = config.COLOR_PATH
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
    
    def draw_agents(self):
        """Draw all agents"""
        for i, agent in enumerate(self.simulator.agents):
            if agent.is_active() or agent.reached_exit:
                color = config.AGENT_COLORS[i % len(config.AGENT_COLORS)]
                
                center_x = agent.x * config.CELL_SIZE + config.CELL_SIZE // 2
                center_y = agent.y * config.CELL_SIZE + config.CELL_SIZE // 2
                
                # Draw agent as circle
                pygame.draw.circle(
                    self.screen,
                    color,
                    (center_x, center_y),
                    config.CELL_SIZE // 3
                )
                
                # Draw agent ID
                id_text = self.small_font.render(str(agent.id), True, (255, 255, 255))
                text_rect = id_text.get_rect(center=(center_x, center_y))
                self.screen.blit(id_text, text_rect)
                
                # Draw path trail (faint)
                if len(agent.path_history) > 1:
                    for i in range(len(agent.path_history) - 1):
                        x1, y1 = agent.path_history[i]
                        x2, y2 = agent.path_history[i + 1]
                        
                        start_pos = (
                            x1 * config.CELL_SIZE + config.CELL_SIZE // 2,
                            y1 * config.CELL_SIZE + config.CELL_SIZE // 2
                        )
                        end_pos = (
                            x2 * config.CELL_SIZE + config.CELL_SIZE // 2,
                            y2 * config.CELL_SIZE + config.CELL_SIZE // 2
                        )
                        
                        pygame.draw.line(self.screen, (*color, 50), start_pos, end_pos, 2)
    
    def draw_info_panel(self):
        """Draw information panel"""
        panel_y = self.maze.height * config.CELL_SIZE
        panel_rect = pygame.Rect(0, panel_y, config.WINDOW_WIDTH, 100)
        pygame.draw.rect(self.screen, (240, 240, 240), panel_rect)
        
        # Draw statistics
        info_texts = [
            f"Step: {self.simulator.step_count}",
            f"Active Agents: {sum(1 for a in self.simulator.agents if a.is_active())}",
            f"Explored: {len(self.simulator.blackboard.explored_cells)}",
            f"Dead Ends: {len(self.simulator.blackboard.dead_ends)}",
        ]
        
        if self.simulator.winner_agent:
            info_texts.append(f"Winner: Agent {self.simulator.winner_agent.id}")
        
        y_offset = panel_y + 10
        for text in info_texts:
            text_surface = self.font.render(text, True, config.COLOR_TEXT)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
        # Draw legend
        legend_x = config.WINDOW_WIDTH - 200
        legend_y = panel_y + 10
        
        legend_items = [
            ("Start", config.COLOR_START),
            ("Exit", config.COLOR_EXIT),
            ("Explored", config.COLOR_EXPLORED),
            ("Dead End", config.COLOR_DEAD_END),
        ]
        
        for label, color in legend_items:
            pygame.draw.rect(
                self.screen,
                color,
                pygame.Rect(legend_x, legend_y, 15, 15)
            )
            text_surface = self.small_font.render(label, True, config.COLOR_TEXT)
            self.screen.blit(text_surface, (legend_x + 20, legend_y))
            legend_y += 20
    
    def render(self):
        """Render one frame"""
        self.screen.fill((255, 255, 255))
        self.draw_maze()
        self.draw_agents()
        self.draw_info_panel()
        pygame.display.flip()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    # Pause/unpause
                    pass
                elif event.key == pygame.K_r:
                    # Reset simulation
                    self.simulator.reset()
        return True
    
    def run(self, max_steps=1000):
        """Run the visualization loop"""
        running = True
        
        while running and self.simulator.step_count < max_steps:
            running = self.handle_events()
            
            if not self.simulator.simulation_complete:
                self.simulator.step()
            
            self.render()
            self.clock.tick(config.SIMULATION_SPEED)
        
        # Keep window open after completion
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(config.FPS)
        
        pygame.quit()
        return self.simulator.get_results()