"""
Main game engine module.

Provides the core game loop and initialization using pygame.
"""

import pygame
import sys
from typing import Optional
from tycoon_engine.core.config import GameConfig
from tycoon_engine.core.state_manager import StateManager


class Game:
    """
    Main game engine class.
    
    Handles initialization, game loop, and cleanup for pygame-based tycoon games.
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """
        Initialize the game engine.
        
        Args:
            config: Game configuration. If None, uses default config.
        """
        self.config = config or GameConfig()
        self.running = False
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.state_manager: Optional[StateManager] = None
        
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption(self.config.game_title)
    
    def initialize(self) -> None:
        """Initialize game systems."""
        # Set up display
        if self.config.fullscreen:
            self.screen = pygame.display.set_mode(
                self.config.get_resolution(),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                self.config.get_resolution()
            )
        
        # Create clock for frame rate control
        self.clock = pygame.time.Clock()
        
        # Initialize state manager
        self.state_manager = StateManager(self.config)
    
    def run(self) -> None:
        """
        Start the main game loop.
        
        This method runs the game loop until the game is quit.
        """
        if not self.screen or not self.clock or not self.state_manager:
            raise RuntimeError("Game not initialized. Call initialize() first.")
        
        self.running = True
        
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(self.config.fps) / 1000.0  # Convert to seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.state_manager.handle_event(event)
            
            # Update game state
            self.state_manager.update(dt)
            
            # Render
            self.screen.fill((0, 0, 0))  # Clear screen
            self.state_manager.render(self.screen)
            pygame.display.flip()
        
        # Cleanup
        self.quit()
    
    def quit(self) -> None:
        """Clean up and quit the game."""
        pygame.quit()
        sys.exit()
    
    def get_state_manager(self) -> StateManager:
        """Get the state manager instance."""
        if not self.state_manager:
            raise RuntimeError("State manager not initialized")
        return self.state_manager
