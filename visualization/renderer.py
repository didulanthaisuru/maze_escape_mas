# visualization/renderer.py

import pygame
import config
import math

class Renderer:
    """Handles visualization using pygame"""
    
    def __init__(self, maze, simulator):
        pygame.init()
        self.maze = maze
        self.simulator = simulator
        
        # Add sidebar for controls
        self.sidebar_width = 200
        self.maze_offset_x = self.sidebar_width
        
        # Increase window size for sidebar and bottom panel
        self.window_width = config.WINDOW_WIDTH + self.sidebar_width
        self.window_height = config.WINDOW_HEIGHT + 50
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Multi-Agent Maze Escape Simulation")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.tiny_font = pygame.font.Font(None, 14)
        self.title_font = pygame.font.Font(None, 32)
        
        # Simulation control
        self.paused = False
        self.step_by_step = False
        self.speed = 2  # Steps per second (slower)
        
        # Agent selection state
        self.selecting_agents = False
        self.selected_agent_count = 10  # Start with 10 agents
        self.min_agents = 1
        self.max_agents = 50  # Increased from 20 to 50
        
        # Message visualization
        self.message_display_time = {}
        self.active_communications = []
        self.message_log = []  # Store recent messages for display
        self.max_log_messages = 5
        
    def draw_maze(self):
        """Draw the maze grid"""
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.get_cell(x, y)
                rect = pygame.Rect(
                    self.maze_offset_x + x * config.CELL_SIZE,
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
                elif cell.is_trap:
                    color = config.COLOR_TRAP  # Show traps in dark red
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
        # NOTE: Exit path visualization removed to keep maze exploration challenging
        # Agents still share and follow the path internally, but it's not shown visually
        
        # Draw agents - show ALL agents, even stuck ones
        for i, agent in enumerate(self.simulator.agents):
            # Show all agents: active, dead, or at exit
            color = config.AGENT_COLORS[i % len(config.AGENT_COLORS)]
            
            center_x = self.maze_offset_x + agent.x * config.CELL_SIZE + config.CELL_SIZE // 2
            center_y = agent.y * config.CELL_SIZE + config.CELL_SIZE // 2
            
            # Don't draw communication range circles - too cluttered
            # (Communication range is still active, just not visualized)
            
            # Check if agent is dead
            is_dead = agent.is_dead
            
            # Dim the color if agent is dead
            if is_dead:
                # Agent is DEAD - draw with very dark color and red tint
                color = (max(100, color[0] // 3), color[1] // 4, color[2] // 4)  # Dark with red tint
            
            # Draw agent as circle
            pygame.draw.circle(
                self.screen,
                color,
                (center_x, center_y),
                config.CELL_SIZE // 3
            )
            
            # Draw special marker for dead agents
            if is_dead:
                # Draw red X over dead agent
                offset = config.CELL_SIZE // 4
                pygame.draw.line(
                    self.screen,
                    (255, 0, 0),
                    (center_x - offset, center_y - offset),
                    (center_x + offset, center_y + offset),
                    2
                )
                pygame.draw.line(
                    self.screen,
                    (255, 0, 0),
                    (center_x - offset, center_y + offset),
                    (center_x + offset, center_y - offset),
                    2
                )
            
            # Draw white border if at exit
            if agent.reached_exit:
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 255),
                    (center_x, center_y),
                    config.CELL_SIZE // 3,
                    2
                )
            
            # Draw agent ID
            id_text = self.small_font.render(str(agent.id), True, (255, 255, 255))
            text_rect = id_text.get_rect(center=(center_x, center_y))
            self.screen.blit(id_text, text_rect)
            
            # Draw current target indicator
            if agent.current_target and agent.is_active():
                target_x, target_y = agent.current_target
                target_center_x = self.maze_offset_x + target_x * config.CELL_SIZE + config.CELL_SIZE // 2
                target_center_y = target_y * config.CELL_SIZE + config.CELL_SIZE // 2
                pygame.draw.line(
                    self.screen,
                    (*color, 100),
                    (center_x, center_y),
                    (target_center_x, target_center_y),
                    1
                )
                pygame.draw.circle(
                    self.screen,
                    (*color, 100),
                    (target_center_x, target_center_y),
                    4
                )
            
            # Draw path trail (faint)
            if len(agent.path_history) > 1:
                for j in range(len(agent.path_history) - 1):
                    x1, y1 = agent.path_history[j]
                    x2, y2 = agent.path_history[j + 1]
                    
                    start_pos = (
                        self.maze_offset_x + x1 * config.CELL_SIZE + config.CELL_SIZE // 2,
                        y1 * config.CELL_SIZE + config.CELL_SIZE // 2
                    )
                    end_pos = (
                        self.maze_offset_x + x2 * config.CELL_SIZE + config.CELL_SIZE // 2,
                        y2 * config.CELL_SIZE + config.CELL_SIZE // 2
                    )
                    
                    pygame.draw.line(self.screen, (*color, 50), start_pos, end_pos, 2)
    
    def draw_communications(self):
        """Draw communication lines between agents"""
        current_time = pygame.time.get_ticks()
        
        # Check for NEW broadcast messages from communication protocol
        recent_broadcasts = self.simulator.communication.get_recent_broadcasts(10)
        for msg in recent_broadcasts:
            msg_id = f"comm_{msg.sender_id}_{msg.message_type}_{msg.timestamp}"
            if msg_id not in self.message_display_time:
                self.message_display_time[msg_id] = current_time
                
                # Add to message log
                msg_text = self._format_communication_message(msg)
                self.message_log.append({
                    'text': msg_text, 
                    'time': current_time, 
                    'agent_id': msg.sender_id,
                    'msg_type': msg.message_type
                })
                if len(self.message_log) > self.max_log_messages:
                    self.message_log.pop(0)
                
                # Add visual communication effect ONLY for important messages
                # Show circles only for DEAD_END and EXIT_FOUND
                if msg.message_type in ['DEAD_END', 'EXIT_FOUND']:
                    if msg.sender_id < len(self.simulator.agents):
                        agent = self.simulator.agents[msg.sender_id]
                        self.active_communications.append({
                            'from': agent.get_position(),
                            'type': msg.message_type,
                            'time': current_time,
                            'agent_id': msg.sender_id
                        })
        
        # Draw active communications (expanding circles)
        to_remove = []
        for comm in self.active_communications:
            elapsed = current_time - comm['time']
            if elapsed < 1500:  # Show for 1.5 seconds
                alpha = int(255 * (1 - elapsed / 1500))
                x, y = comm['from']
                center_x = self.maze_offset_x + x * config.CELL_SIZE + config.CELL_SIZE // 2
                center_y = y * config.CELL_SIZE + config.CELL_SIZE // 2
                
                # Draw expanding circle for message broadcast
                radius = int(config.CELL_SIZE * (1 + elapsed / 400))
                
                # Different colors for different message types
                if comm['type'] == 'EXIT_FOUND':
                    color = (0, 255, 0)  # Green for exit found
                elif comm['type'] == 'DEAD_END':
                    color = (255, 100, 100)  # Red for dead end
                else:
                    color = config.AGENT_COLORS[comm['agent_id'] % len(config.AGENT_COLORS)]
                
                pygame.draw.circle(
                    self.screen,
                    (*color, max(0, alpha // 2)),
                    (center_x, center_y),
                    radius,
                    3
                )
                
                # Draw message type text above the circle
                if elapsed < 800:
                    text = comm['type'].replace('_', ' ')
                    text_surface = self.tiny_font.render(text, True, color)
                    text_rect = text_surface.get_rect(center=(center_x, center_y - radius - 10))
                    self.screen.blit(text_surface, text_rect)
            else:
                to_remove.append(comm)
        
        # Clean up old communications
        for comm in to_remove:
            self.active_communications.remove(comm)
    
    def _format_communication_message(self, msg):
        """Format communication protocol message for display"""
        agent_id = msg.sender_id
        msg_type = msg.message_type
        content = msg.content
        
        if msg_type == 'DEAD_END':
            pos = content.get('position', 'unknown')
            is_trap = content.get('is_trap', False)
            if is_trap:
                return f"Agent {agent_id} → ALL: TRAP (no escape) at {pos}!"
            return f"Agent {agent_id} → ALL: Dead end at {pos}"
        elif msg_type == 'WRONG_PATH':
            pos = content.get('position', 'unknown')
            return f"Agent {agent_id} → ALL: Wrong path at {pos} (backtracking)"
        elif msg_type == 'EXIT_FOUND':
            pos = content.get('position', 'unknown')
            return f"Agent {agent_id} → ALL: EXIT FOUND at {pos}! Everyone evacuate!"
        elif msg_type == 'PATH_SHARED':
            return f"Agent {agent_id} → ALL: Sharing path information"
        else:
            return f"Agent {agent_id} → ALL: {msg_type}"
    
    def _format_message(self, agent_id, msg_type, data):
        """Format message for display (legacy blackboard messages)"""
        if msg_type == 'dead_end':
            return f"Agent {agent_id}: Found dead end"
        elif msg_type == 'exit_found':
            return f"Agent {agent_id}: REACHED EXIT!"
        elif msg_type == 'exit_visible':
            return f"Agent {agent_id}: Exit is visible!"
        elif msg_type == 'exploring':
            return f"Agent {agent_id}: Exploring new area"
        else:
            return f"Agent {agent_id}: {msg_type}"
    
    def draw_message_log(self):
        """Draw recent message log"""
        if not self.message_log:
            return
        
        # Draw message box
        msg_box_x = config.WINDOW_WIDTH - 280
        msg_box_y = 10
        msg_box_width = 270
        msg_box_height = 130
        
        # Semi-transparent background
        surface = pygame.Surface((msg_box_width, msg_box_height))
        surface.set_alpha(220)
        surface.fill((30, 30, 30))
        self.screen.blit(surface, (msg_box_x, msg_box_y))
        
        # Border
        pygame.draw.rect(self.screen, (100, 200, 255), 
                        (msg_box_x, msg_box_y, msg_box_width, msg_box_height), 2)
        
        # Title
        title_surface = self.small_font.render("Agent Communications", True, (100, 200, 255))
        self.screen.blit(title_surface, (msg_box_x + 5, msg_box_y + 5))
        
        # Draw messages with better formatting
        y_offset = msg_box_y + 28
        for msg_data in self.message_log[-5:]:  # Show last 5 messages
            # Color based on message type if available
            if msg_data.get('msg_type') == 'EXIT_FOUND':
                color = (100, 255, 100)  # Bright green
            elif msg_data.get('msg_type') == 'DEAD_END':
                color = (255, 100, 100)  # Red
            elif msg_data.get('msg_type') == 'WRONG_PATH':
                color = (255, 165, 0)  # Orange
            else:
                color = config.AGENT_COLORS[msg_data['agent_id'] % len(config.AGENT_COLORS)]
            
            # Truncate text if too long
            text = msg_data['text']
            if len(text) > 38:
                text = text[:35] + "..."
            
            text_surface = self.tiny_font.render(text, True, color)
            self.screen.blit(text_surface, (msg_box_x + 5, y_offset))
            y_offset += 19
    
    def draw_info_panel(self):
        """Draw information panel"""
        panel_y = self.maze.height * config.CELL_SIZE
        panel_height = self.window_height - panel_y
        panel_rect = pygame.Rect(0, panel_y, config.WINDOW_WIDTH, panel_height)
        pygame.draw.rect(self.screen, (240, 240, 240), panel_rect)
        
        # Draw status indicator
        status_color = (255, 100, 100) if self.paused else (100, 255, 100)
        status_text = "PAUSED" if self.paused else "RUNNING"
        status_surface = self.font.render(status_text, True, status_color)
        self.screen.blit(status_surface, (10, panel_y + 5))
        
        # Draw speed control
        speed_text = f"Speed: {self.speed} steps/sec"
        speed_surface = self.small_font.render(speed_text, True, config.COLOR_TEXT)
        self.screen.blit(speed_surface, (120, panel_y + 10))
        
        # Draw statistics
        y_offset = panel_y + 35
        total_broadcasts = len(self.simulator.communication.broadcast_messages)
        agents_at_exit = sum(1 for a in self.simulator.agents if a.reached_exit)
        info_texts = [
            f"Step: {self.simulator.step_count}",
            f"Active: {sum(1 for a in self.simulator.agents if a.is_active())}",
            f"At Exit: {agents_at_exit}/{len(self.simulator.agents)}",
            f"Explored: {len(self.simulator.blackboard.explored_cells)}",
            f"Dead Ends: {len(self.simulator.blackboard.dead_ends)}",
            f"Broadcasts: {total_broadcasts}",
        ]
        
        if self.simulator.winner_agent:
            info_texts.append(f"First: Agent {self.simulator.winner_agent.id}")
        
        if agents_at_exit == len(self.simulator.agents):
            success_text = self.font.render("ALL AGENTS ESCAPED!", True, (0, 255, 0))
            self.screen.blit(success_text, (config.WINDOW_WIDTH // 2 - 150, panel_y + 5))
        
        x_offset = 10
        for i, text in enumerate(info_texts):
            text_surface = self.small_font.render(text, True, config.COLOR_TEXT)
            self.screen.blit(text_surface, (x_offset, y_offset))
            x_offset += 120
            if (i + 1) % 3 == 0:
                x_offset = 10
                y_offset += 20
        
        # Draw legend
        legend_x = config.WINDOW_WIDTH - 200
        legend_y = panel_y + 10
        
        legend_items = [
            ("Start", config.COLOR_START),
            ("Exit", config.COLOR_EXIT),
            ("Explored", config.COLOR_EXPLORED),
            ("Dead End", config.COLOR_DEAD_END),
            ("Trap", config.COLOR_TRAP),
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
        self.draw_communications()
        self.draw_agents()
        self.draw_sidebar()
        pygame.display.flip()
    
    def draw_controls_help(self):
        """Draw control instructions"""
        panel_y = self.maze.height * config.CELL_SIZE
        help_y = panel_y + 85
        
        controls = [
            "SPACE: Pause/Resume",
            "↑/↓: Speed",
            "S: Step",
            "R: Reset",
            "ESC: Quit"
        ]
        
        x_offset = 10
        for control in controls:
            text_surface = self.tiny_font.render(control, True, (100, 100, 100))
            self.screen.blit(text_surface, (x_offset, help_y))
            x_offset += 110
    
    def draw_sidebar(self):
        """Draw left sidebar with controls and agent selection"""
        # Sidebar background
        sidebar_rect = pygame.Rect(0, 0, self.sidebar_width, self.window_height)
        pygame.draw.rect(self.screen, (30, 30, 40), sidebar_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (self.sidebar_width, 0), (self.sidebar_width, self.window_height), 2)
        
        y_offset = 20
        
        # Title
        title_text = self.font.render("CONTROLS", True, (100, 200, 255))
        self.screen.blit(title_text, (15, y_offset))
        y_offset += 40
        
        # Agent Selection Section
        pygame.draw.line(self.screen, (60, 60, 70), (10, y_offset), (self.sidebar_width - 10, y_offset))
        y_offset += 15
        
        agents_label = self.small_font.render("Agents:", True, (200, 200, 200))
        self.screen.blit(agents_label, (15, y_offset))
        y_offset += 25
        
        # Agent count with +/- buttons
        minus_rect = pygame.Rect(20, y_offset, 30, 30)
        count_rect = pygame.Rect(55, y_offset, 70, 30)
        plus_rect = pygame.Rect(130, y_offset, 30, 30)
        
        # Draw buttons
        pygame.draw.rect(self.screen, (50, 50, 70), minus_rect, border_radius=5)
        pygame.draw.rect(self.screen, (80, 80, 100), count_rect, border_radius=5)
        pygame.draw.rect(self.screen, (50, 50, 70), plus_rect, border_radius=5)
        
        # Button borders
        pygame.draw.rect(self.screen, (100, 100, 120), minus_rect, 1, border_radius=5)
        pygame.draw.rect(self.screen, (100, 200, 255), count_rect, 2, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 120), plus_rect, 1, border_radius=5)
        
        # Button text
        minus_text = self.font.render("-", True, (255, 255, 255))
        count_text = self.font.render(str(self.selected_agent_count), True, (0, 255, 150))
        plus_text = self.font.render("+", True, (255, 255, 255))
        
        self.screen.blit(minus_text, (minus_rect.centerx - 5, minus_rect.centery - 10))
        self.screen.blit(count_text, (count_rect.centerx - 8, count_rect.centery - 10))
        self.screen.blit(plus_text, (plus_rect.centerx - 6, plus_rect.centery - 10))
        
        # Store button rects for click detection
        self.minus_button = minus_rect
        self.plus_button = plus_rect
        
        y_offset += 45
        
        # START button
        start_button_rect = pygame.Rect(20, y_offset, 160, 35)
        button_color = (0, 150, 100) if self.selecting_agents else (60, 60, 70)
        pygame.draw.rect(self.screen, button_color, start_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (0, 255, 150) if self.selecting_agents else (100, 100, 120), start_button_rect, 2, border_radius=8)
        
        start_text = self.small_font.render("START", True, (255, 255, 255))
        self.screen.blit(start_text, (start_button_rect.centerx - 25, start_button_rect.centery - 8))
        
        self.start_button = start_button_rect
        y_offset += 40
        
        # Show keyboard hints when selecting agents
        if self.selecting_agents:
            hint_font = self.tiny_font
            hints = [
                "← → : Change agents",
                "ENTER : Start",
                "M : New maze"
            ]
            for hint in hints:
                hint_text = hint_font.render(hint, True, (150, 200, 255))
                self.screen.blit(hint_text, (20, y_offset))
                y_offset += 16
        
        y_offset += 10
        
        # Simulation Controls
        pygame.draw.line(self.screen, (60, 60, 70), (10, y_offset), (self.sidebar_width - 10, y_offset))
        y_offset += 15
        
        controls = [
            ("SPACE", "Pause"),
            ("↑/↓", "Speed"),
            ("S", "Step"),
            ("R", "Reset"),
            ("M", "New Maze"),
            ("ESC", "Quit")
        ]
        
        for key, action in controls:
            key_text = self.tiny_font.render(f"{key}:", True, (150, 150, 150))
            action_text = self.tiny_font.render(action, True, (200, 200, 200))
            self.screen.blit(key_text, (15, y_offset))
            self.screen.blit(action_text, (80, y_offset))
            y_offset += 20
        
        y_offset += 10
        
        # Status Section
        pygame.draw.line(self.screen, (60, 60, 70), (10, y_offset), (self.sidebar_width - 10, y_offset))
        y_offset += 15
        
        status_label = self.small_font.render("STATUS", True, (100, 200, 255))
        self.screen.blit(status_label, (15, y_offset))
        y_offset += 25
        
        # Step count
        step_text = self.tiny_font.render(f"Step: {self.simulator.step_count}", True, (200, 200, 200))
        self.screen.blit(step_text, (15, y_offset))
        y_offset += 18
        
        # Speed
        speed_text = self.tiny_font.render(f"Speed: {self.speed}x", True, (200, 200, 200))
        self.screen.blit(speed_text, (15, y_offset))
        y_offset += 18
        
        # Paused status
        if self.paused:
            paused_text = self.small_font.render("PAUSED", True, (255, 200, 0))
            self.screen.blit(paused_text, (15, y_offset))
            y_offset += 22
        
        # Agents at exit
        agents_at_exit = sum(1 for agent in self.simulator.agents if agent.reached_exit)
        exit_text = self.tiny_font.render(f"At Exit: {agents_at_exit}/{len(self.simulator.agents)}", True, (0, 255, 150))
        self.screen.blit(exit_text, (15, y_offset))
        y_offset += 18
        
        # Dead agents (using is_dead attribute)
        dead_agents = sum(1 for agent in self.simulator.agents if agent.is_dead)
        if dead_agents > 0:
            dead_text = self.tiny_font.render(f"Dead: {dead_agents} ☠️", True, (255, 50, 50))
            self.screen.blit(dead_text, (15, y_offset))
            y_offset += 18
        
        # Completion
        if self.simulator.simulation_complete:
            complete_text = self.small_font.render("COMPLETE!", True, (0, 255, 0))
            self.screen.blit(complete_text, (15, y_offset))
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = event.pos
                    
                    # Check minus button
                    if hasattr(self, 'minus_button') and self.minus_button.collidepoint(mouse_pos):
                        if self.selected_agent_count > self.min_agents:
                            self.selected_agent_count -= 1
                    
                    # Check plus button
                    elif hasattr(self, 'plus_button') and self.plus_button.collidepoint(mouse_pos):
                        if self.selected_agent_count < self.max_agents:
                            self.selected_agent_count += 1
                    
                    # Check start button
                    elif hasattr(self, 'start_button') and self.start_button.collidepoint(mouse_pos):
                        if self.selecting_agents:
                            self.selecting_agents = False
                            self.reset_simulation_with_agents(self.selected_agent_count)
                            print(f"Starting simulation with {self.selected_agent_count} agents")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    # Toggle pause
                    if not self.selecting_agents:
                        self.paused = not self.paused
                        print(f"Simulation {'PAUSED' if self.paused else 'RESUMED'}")
                elif event.key == pygame.K_s:
                    # Step by step mode
                    if self.paused and not self.selecting_agents:
                        self.step_by_step = True
                        print("Executing one step...")
                elif event.key == pygame.K_r:
                    # Show agent selection overlay
                    self.selecting_agents = True
                    self.paused = True
                    print("Press ← → to select agents, ENTER to start")
                elif event.key == pygame.K_m:
                    # Regenerate maze - works ANYTIME (even during agent selection!)
                    print("\n" + "="*50)
                    print("GENERATING NEW MAZE...")
                    print("="*50)
                    self.regenerate_maze()
                    print("New maze generated! Select agents to start.")
                elif event.key == pygame.K_LEFT:
                    # Decrease agent count during selection
                    if self.selecting_agents:
                        if self.selected_agent_count > self.min_agents:
                            self.selected_agent_count -= 1
                            print(f"Agents: {self.selected_agent_count}")
                elif event.key == pygame.K_RIGHT:
                    # Increase agent count during selection
                    if self.selecting_agents:
                        if self.selected_agent_count < self.max_agents:
                            self.selected_agent_count += 1
                            print(f"Agents: {self.selected_agent_count}")
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # Start simulation with selected agents
                    if self.selecting_agents:
                        self.selecting_agents = False
                        self.reset_simulation_with_agents(self.selected_agent_count)
                        print(f"Starting simulation with {self.selected_agent_count} agents")
                elif event.key == pygame.K_UP:
                    # Increase speed (only if not selecting agents)
                    if not self.selecting_agents:
                        self.speed = min(10, self.speed + 1)
                        print(f"Speed: {self.speed} steps/sec")
                elif event.key == pygame.K_DOWN:
                    # Decrease speed (only if not selecting agents)
                    if not self.selecting_agents:
                        self.speed = max(1, self.speed - 1)
                        print(f"Speed: {self.speed} steps/sec")
        return True
    
    def reset_simulation_with_agents(self, num_agents):
        """Reset simulation with a specific number of agents"""
        from simulation.simulator import Simulator
        
        # Create new simulator with selected number of agents
        self.simulator = Simulator(
            self.maze,
            num_agents,
            config.AGENT_ENERGY,
            config.AGENT_VISION_RANGE,
            config.COMMUNICATION_RANGE
        )
        
        # Reset visualization state
        self.message_display_time = {}
        self.active_communications = []
        self.message_log = []
        self.paused = False
        
        print(f"Simulation reset with {num_agents} agents!")
    
    def regenerate_maze(self):
        """Regenerate the entire maze and reset simulation"""
        from environment.maze import Maze
        from simulation.simulator import Simulator
        
        # Generate a brand new maze
        self.maze = Maze(
            config.MAZE_WIDTH,
            config.MAZE_HEIGHT,
            config.WALL_DENSITY,
            use_fixed_maze=False  # Always generate random maze on M key
        )
        self.maze.generate()
        
        print(f"New maze generated!")
        print(f"Start: {self.maze.start_pos}, Exit: {self.maze.exit_pos}")
        
        # Create new simulator with default number of agents
        self.simulator = Simulator(
            self.maze,
            config.NUM_AGENTS,
            config.AGENT_ENERGY,
            config.AGENT_VISION_RANGE,
            config.COMMUNICATION_RANGE
        )
        
        # Reset all visualization state
        self.message_display_time = {}
        self.active_communications = []
        self.message_log = []
        self.paused = True
        self.selecting_agents = True  # Show agent selection screen
        
        print("Ready to start! Select number of agents.")
    
    def run(self, max_steps=1000):
        """Run the visualization loop"""
        running = True
        last_step_time = pygame.time.get_ticks()
        
        print("\n=== SIMULATION CONTROLS ===")
        print("SPACE: Pause/Resume")
        print("↑/↓: Increase/Decrease Speed")
        print("S: Single Step (when paused)")
        print("R: Reset Simulation")
        print("M: New Maze (regenerate maze)")
        print("ESC: Quit")
        print("===========================\n")
        
        while running and self.simulator.step_count < max_steps:
            running = self.handle_events()
            current_time = pygame.time.get_ticks()
            
            # Control simulation speed
            time_per_step = 1000 / self.speed  # milliseconds per step
            
            # Execute simulation step (only if not selecting agents)
            if not self.selecting_agents and not self.simulator.simulation_complete:
                should_step = False
                
                if self.step_by_step:
                    should_step = True
                    self.step_by_step = False
                elif not self.paused and (current_time - last_step_time) >= time_per_step:
                    should_step = True
                    last_step_time = current_time
                
                if should_step:
                    self.simulator.step()
            
            self.render()
            self.clock.tick(60)  # 60 FPS for smooth rendering
        
        # Keep window open after completion
        print("\nSimulation Complete! Window will remain open...")
        print("Press ESC to quit or R to reset.")
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        return self.simulator.get_results()