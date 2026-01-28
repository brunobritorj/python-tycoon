"""
Complete menu system demo.

Demonstrates all the menu screens and UI components of the Python Tycoon engine.
"""

import pygame
from tycoon_engine.core.game import Game
from tycoon_engine.core.config import GameConfig
from tycoon_engine.core.state_manager import GameState
from tycoon_engine.ui.screens.main_menu import MainMenuScreen
from tycoon_engine.ui.screens.settings import SettingsScreen
from tycoon_engine.ui.screens.multiplayer import MultiplayerScreen
from tycoon_engine.ui.screens.hud import HUDScreen, PauseMenuState


class PlayingState(GameState):
    """
    Simple playing state with HUD.
    
    This demonstrates how to use the HUD component in a game state.
    """
    
    def enter(self, **kwargs):
        """Initialize playing state."""
        # Create HUD
        self.hud = HUDScreen(
            screen_width=self.config.screen_width,
            screen_height=self.config.screen_height,
            on_menu=self._handle_menu,
            show_menu_button=True
        )
        
        # Game data
        self.money = 1000.0
        self.score = 0
        self.time_elapsed = 0.0
        
        print("Playing state started. Press ESC for menu.")
    
    def exit(self):
        """Clean up playing state."""
        pass
    
    def update(self, dt: float):
        """Update game state."""
        self.time_elapsed += dt
        self.score = int(self.time_elapsed * 10)
        
        # Slowly increase money
        self.money += dt * 5
        
        # Update HUD
        self.hud.set_money(self.money)
        self.hud.set_resource('score', self.score, format_str="Score: {}")
        
        self.hud.update(dt)
    
    def render(self, screen: pygame.Surface):
        """Render game state."""
        # Draw game background
        screen.fill((30, 50, 70))
        
        # Draw some game content
        font = pygame.font.Font(None, 48)
        text = font.render("Game is Running!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2))
        screen.blit(text, text_rect)
        
        # Render HUD
        self.hud.render(screen)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle events."""
        # Let HUD handle events first
        if self.hud.handle_event(event):
            return
        
        # Handle ESC to pause
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._handle_menu()
    
    def _handle_menu(self):
        """Show pause menu."""
        if "pause" in self.state_manager.states:
            self.state_manager.change_state("pause", previous_state="playing")


def main():
    """
    Main entry point for the menu demo.
    
    This sets up a complete game with:
    - Main menu
    - Settings screen
    - Multiplayer lobby (if enabled)
    - Playing state with HUD
    - Pause menu
    """
    # Create configuration
    config = GameConfig(
        game_title="Menu System Demo",
        screen_width=1280,
        screen_height=720,
        fps=60,
        enable_multiplayer=True,  # Enable multiplayer menu
        starting_money=1000.0
    )
    
    # Create and initialize game
    game = Game(config)
    game.initialize()
    
    # Get state manager
    state_manager = game.get_state_manager()
    
    # Create playing state
    playing_state = PlayingState(state_manager)
    state_manager.add_state("playing", playing_state)
    
    # Create pause menu
    pause_state = PauseMenuState(
        state_manager,
        on_resume=lambda: state_manager.change_state("playing"),
        on_quit=lambda: state_manager.change_state("main_menu")
    )
    state_manager.add_state("pause", pause_state)
    
    # Create main menu
    main_menu = MainMenuScreen(
        state_manager,
        on_play=lambda: state_manager.change_state("playing"),
        background_color=(20, 20, 50)
    )
    state_manager.add_state("main_menu", main_menu)
    
    # Create settings screen
    settings_screen = SettingsScreen(
        state_manager,
        on_back=lambda: state_manager.change_state("main_menu")
    )
    state_manager.add_state("settings", settings_screen)
    
    # Create multiplayer screen (if enabled)
    if config.enable_multiplayer:
        multiplayer_screen = MultiplayerScreen(
            state_manager,
            on_back=lambda: state_manager.change_state("main_menu")
        )
        state_manager.add_state("multiplayer", multiplayer_screen)
    
    # Start at main menu
    state_manager.change_state("main_menu")
    
    # Run the game
    print("\n=== Menu System Demo ===")
    print("This demo showcases the menu system and UI components.")
    print("\nNavigation:")
    print("- Main Menu -> Play: Start the game")
    print("- Main Menu -> Settings: Configure game settings")
    print("- Main Menu -> Multiplayer: Host or join games")
    print("- In-Game: Press ESC or click Menu button to pause")
    print("- Pause Menu: Resume, Settings, or Quit to Menu")
    print("\nPress Ctrl+C to exit\n")
    
    game.run()


if __name__ == '__main__':
    main()
