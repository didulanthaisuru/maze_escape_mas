# visualization/start_menu.py

import pygame
import sys

class StartMenu:
    """Start menu for selecting number of agents"""
    
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Multi-Agent Maze Escape - Setup")
        
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)
        
        # Agent selection
        self.min_agents = 1
        self.max_agents = 20
        self.selected_agents = 5
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.title_color = (100, 200, 255)
        self.text_color = (220, 220, 220)
        self.button_color = (50, 50, 80)
        self.button_hover_color = (70, 70, 120)
        self.button_text_color = (255, 255, 255)
        self.accent_color = (0, 255, 150)
        
        # Buttons
        self.decrease_button = pygame.Rect(250, 300, 60, 60)
        self.increase_button = pygame.Rect(490, 300, 60, 60)
        self.start_button = pygame.Rect(300, 450, 200, 70)
        
        self.hovered_button = None
        
    def draw(self):
        """Draw the start menu"""
        self.screen.fill(self.bg_color)
        
        # Title
        title_text = self.title_font.render("MAZE ESCAPE", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.small_font.render("Multi-Agent System", True, self.text_color)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 140))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instruction
        instruction_text = self.tiny_font.render("Select Number of Agents", True, self.text_color)
        instruction_rect = instruction_text.get_rect(center=(self.width // 2, 220))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Agent count display
        agent_text = self.font.render(str(self.selected_agents), True, self.accent_color)
        agent_rect = agent_text.get_rect(center=(self.width // 2, 330))
        self.screen.blit(agent_text, agent_rect)
        
        # Agent label
        agent_label = self.small_font.render("Agents", True, self.text_color)
        agent_label_rect = agent_label.get_rect(center=(self.width // 2, 380))
        self.screen.blit(agent_label, agent_label_rect)
        
        # Decrease button
        decrease_color = self.button_hover_color if self.hovered_button == 'decrease' else self.button_color
        pygame.draw.rect(self.screen, decrease_color, self.decrease_button, border_radius=10)
        pygame.draw.rect(self.screen, self.text_color, self.decrease_button, 2, border_radius=10)
        minus_text = self.font.render("-", True, self.button_text_color)
        minus_rect = minus_text.get_rect(center=self.decrease_button.center)
        self.screen.blit(minus_text, minus_rect)
        
        # Increase button
        increase_color = self.button_hover_color if self.hovered_button == 'increase' else self.button_color
        pygame.draw.rect(self.screen, increase_color, self.increase_button, border_radius=10)
        pygame.draw.rect(self.screen, self.text_color, self.increase_button, 2, border_radius=10)
        plus_text = self.font.render("+", True, self.button_text_color)
        plus_rect = plus_text.get_rect(center=self.increase_button.center)
        self.screen.blit(plus_text, plus_rect)
        
        # Start button
        start_color = self.button_hover_color if self.hovered_button == 'start' else self.button_color
        pygame.draw.rect(self.screen, start_color, self.start_button, border_radius=15)
        pygame.draw.rect(self.screen, self.accent_color, self.start_button, 3, border_radius=15)
        start_text = self.font.render("START", True, self.button_text_color)
        start_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_rect)
        
        # Info text at bottom
        info_lines = [
            "• Agents will cooperate to find the maze exit",
            "• One agent finds the path, others follow",
            "• Watch them communicate and navigate together!"
        ]
        
        y_offset = 530
        for line in info_lines:
            info_text = self.tiny_font.render(line, True, self.text_color)
            info_rect = info_text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(info_text, info_rect)
            y_offset += 22
        
        pygame.display.flip()
    
    def handle_mouse_motion(self, pos):
        """Handle mouse hover effects"""
        if self.decrease_button.collidepoint(pos):
            self.hovered_button = 'decrease'
        elif self.increase_button.collidepoint(pos):
            self.hovered_button = 'increase'
        elif self.start_button.collidepoint(pos):
            self.hovered_button = 'start'
        else:
            self.hovered_button = None
    
    def handle_click(self, pos):
        """Handle button clicks"""
        if self.decrease_button.collidepoint(pos):
            if self.selected_agents > self.min_agents:
                self.selected_agents -= 1
        elif self.increase_button.collidepoint(pos):
            if self.selected_agents < self.max_agents:
                self.selected_agents += 1
        elif self.start_button.collidepoint(pos):
            return True  # Start simulation
        return False
    
    def run(self):
        """Run the start menu and return selected number of agents"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.handle_click(event.pos):
                            # Start button clicked
                            return self.selected_agents
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return None
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Start with current selection
                        return self.selected_agents
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                        if self.selected_agents > self.min_agents:
                            self.selected_agents -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                        if self.selected_agents < self.max_agents:
                            self.selected_agents += 1
            
            self.draw()
            self.clock.tick(60)
        
        return None
