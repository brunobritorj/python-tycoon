"""
Demo Tycoon Game - A simple lemonade stand tycoon game.

This demonstrates how to build a tycoon game using the engine.
"""

import pygame
from tycoon_engine.core.game import Game
from tycoon_engine.core.config import GameConfig
from tycoon_engine.core.state_manager import GameState
from tycoon_engine.entities.entity import EntityManager
from tycoon_engine.entities.resources import ResourceManager
from tycoon_engine.ui.renderer import UIRenderer


class PlayingState(GameState):
    """Main playing state for the demo game."""
    
    def enter(self, **kwargs):
        """Initialize playing state."""
        self.entity_manager = EntityManager()
        self.resource_manager = ResourceManager(starting_money=self.config.starting_money)
        self.ui = UIRenderer()
        
        # Game variables
        self.lemonade_price = 1.0
        self.production_rate = 1.0  # Lemonades per second
        self.production_timer = 0.0
        
        print("Demo Tycoon Game Started!")
        print("Press SPACE to buy production upgrade ($100)")
        print("Press UP/DOWN to adjust lemonade price")
        print("Press ESC to quit")
    
    def exit(self):
        """Clean up playing state."""
        pass
    
    def update(self, dt: float):
        """Update game logic."""
        # Produce lemonade
        self.production_timer += dt
        if self.production_timer >= 1.0 / self.production_rate:
            self.production_timer = 0.0
            # Sell one lemonade
            self.resource_manager.add_money(self.lemonade_price)
            self.resource_manager.add_resource('lemonades_sold', 1)
    
    def render(self, screen: pygame.Surface):
        """Render the game."""
        screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw title
        self.ui.draw_text(
            screen,
            "Lemonade Stand Tycoon",
            (20, 20),
            font_size=48,
            color=(255, 255, 0)
        )
        
        # Draw stats panel
        panel_rect = pygame.Rect(20, 100, 400, 300)
        self.ui.draw_panel(screen, panel_rect, bg_color=(0, 100, 0), alpha=200)
        
        # Draw stats
        money = self.resource_manager.get_money()
        sold = self.resource_manager.get_resource('lemonades_sold')
        
        self.ui.draw_text(screen, f"Money: ${money:.2f}", (40, 120), font_size=32)
        self.ui.draw_text(screen, f"Lemonades Sold: {int(sold)}", (40, 160), font_size=32)
        self.ui.draw_text(screen, f"Price: ${self.lemonade_price:.2f}", (40, 200), font_size=32)
        self.ui.draw_text(screen, f"Production: {self.production_rate:.1f}/sec", (40, 240), font_size=32)
        
        # Draw instructions
        self.ui.draw_text(screen, "SPACE: Buy Upgrade ($100)", (20, 450), font_size=24)
        self.ui.draw_text(screen, "UP/DOWN: Adjust Price", (20, 480), font_size=24)
        self.ui.draw_text(screen, "ESC: Quit", (20, 510), font_size=24)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            elif event.key == pygame.K_SPACE:
                # Buy production upgrade
                if self.resource_manager.remove_money(100):
                    self.production_rate += 0.5
                    print(f"Upgrade purchased! Production: {self.production_rate}/sec")
                else:
                    print("Not enough money!")
            
            elif event.key == pygame.K_UP:
                self.lemonade_price += 0.10
                print(f"Price increased to ${self.lemonade_price:.2f}")
            
            elif event.key == pygame.K_DOWN:
                self.lemonade_price = max(0.10, self.lemonade_price - 0.10)
                print(f"Price decreased to ${self.lemonade_price:.2f}")


def main():
    """Main entry point for the demo game."""
    # Create custom configuration
    config = GameConfig(
        game_title="Lemonade Stand Tycoon - Demo",
        screen_width=800,
        screen_height=600,
        fps=60,
        starting_money=50.0
    )
    
    # Create and initialize game
    game = Game(config)
    game.initialize()
    
    # Set up game state
    state_manager = game.get_state_manager()
    playing_state = PlayingState(state_manager)
    state_manager.add_state("playing", playing_state)
    state_manager.change_state("playing")
    
    # Run the game
    game.run()


if __name__ == '__main__':
    main()
