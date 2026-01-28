# Tutorial: Building a Simple Tycoon Game

This tutorial will walk you through creating a simple café tycoon game using the engine.

## Step 1: Set Up Configuration

First, create a configuration for your game:

```python
from tycoon_engine.core.config import GameConfig

config = GameConfig(
    game_title="Café Tycoon",
    screen_width=1024,
    screen_height=768,
    fps=60,
    starting_money=500.0,
    custom_params={
        'coffee_base_price': 3.0,
        'upgrade_cost': 150.0
    }
)
```

## Step 2: Create the Main Game State

Create your main game state that inherits from `GameState`:

```python
from tycoon_engine.core.state_manager import GameState
from tycoon_engine.entities.resources import ResourceManager
from tycoon_engine.ui.renderer import UIRenderer
import pygame

class CafeGameState(GameState):
    def enter(self, **kwargs):
        """Initialize the game state"""
        self.resources = ResourceManager(
            starting_money=self.config.starting_money
        )
        self.ui = UIRenderer()
        
        # Game variables
        self.coffee_price = self.config.get_custom_param('coffee_base_price')
        self.customers_per_minute = 10
        self.customer_timer = 0
        self.satisfaction = 100
        
    def exit(self):
        """Cleanup"""
        pass
    
    def update(self, dt: float):
        """Update game logic"""
        # Customer arrives every (60 / customers_per_minute) seconds
        self.customer_timer += dt
        interval = 60.0 / self.customers_per_minute
        
        if self.customer_timer >= interval:
            self.customer_timer = 0
            # Customer buys coffee
            self.resources.add_money(self.coffee_price)
            self.resources.add_resource('coffees_sold', 1)
    
    def render(self, screen: pygame.Surface):
        """Render the game"""
        screen.fill((139, 69, 19))  # Brown background
        
        # Title
        self.ui.draw_text(
            screen, "Café Tycoon", (20, 20),
            font_size=48, color=(255, 255, 255)
        )
        
        # Stats
        money = self.resources.get_money()
        sold = self.resources.get_resource('coffees_sold')
        
        self.ui.draw_text(
            screen, f"Money: ${money:.2f}", (20, 100),
            font_size=32, color=(255, 255, 255)
        )
        self.ui.draw_text(
            screen, f"Coffees Sold: {int(sold)}", (20, 140),
            font_size=32, color=(255, 255, 255)
        )
        self.ui.draw_text(
            screen, f"Coffee Price: ${self.coffee_price:.2f}", (20, 180),
            font_size=32, color=(255, 255, 255)
        )
    
    def handle_event(self, event: pygame.event.Event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
```

## Step 3: Initialize and Run the Game

```python
from tycoon_engine.core.game import Game

def main():
    # Create game
    game = Game(config)
    game.initialize()
    
    # Set up states
    state_manager = game.get_state_manager()
    cafe_state = CafeGameState(state_manager)
    state_manager.add_state("playing", cafe_state)
    state_manager.change_state("playing")
    
    # Run
    game.run()

if __name__ == '__main__':
    main()
```

## Step 4: Add Upgrades

Extend the `handle_event` method to add upgrade mechanics:

```python
def handle_event(self, event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            # Buy upgrade
            cost = self.config.get_custom_param('upgrade_cost')
            if self.resources.remove_money(cost):
                self.customers_per_minute += 5
                print(f"Upgrade! Customers: {self.customers_per_minute}/min")
            else:
                print("Not enough money!")
        
        elif event.key == pygame.K_UP:
            self.coffee_price += 0.25
        
        elif event.key == pygame.K_DOWN:
            self.coffee_price = max(0.5, self.coffee_price - 0.25)
```

## Step 5: Add Entities

Create custom entities for your game:

```python
from tycoon_engine.entities.entity import Entity
import pygame

class CoffeeMachine(Entity):
    def __init__(self, entity_id: str, x: float, y: float):
        super().__init__(entity_id, "coffee_machine", x, y)
        self.level = 1
        self.efficiency = 1.0
    
    def render(self, screen: pygame.Surface, camera_offset=(0, 0)):
        # Draw a simple rectangle for the machine
        rect = pygame.Rect(
            int(self.x - camera_offset[0]),
            int(self.y - camera_offset[1]),
            40, 40
        )
        pygame.draw.rect(screen, (100, 50, 0), rect)
```

Then add it to your game state:

```python
from tycoon_engine.entities.entity import EntityManager

def enter(self, **kwargs):
    # ... existing code ...
    self.entity_manager = EntityManager()
    
    # Add a coffee machine
    machine = CoffeeMachine("machine_1", 400, 300)
    self.entity_manager.add_entity(machine)
```

## Step 6: Add Multiplayer (Optional)

To add multiplayer support:

1. Enable multiplayer in config:
```python
config = GameConfig(
    # ... other params ...
    enable_multiplayer=True,
    server_host="localhost",
    server_port=5000
)
```

2. Start the server:
```bash
tycoon-server
```

3. Add networking to your game state:
```python
from tycoon_engine.networking.client import GameClient

def enter(self, **kwargs):
    # ... existing code ...
    
    if self.config.enable_multiplayer:
        self.client = GameClient(
            self.config.server_host,
            self.config.server_port
        )
        self.client.on_state_update = self.on_network_update
        self.client.connect()

def on_network_update(self, state):
    """Handle state updates from server"""
    # Sync game state with server
    pass
```

## Next Steps

- Add more entity types (tables, customers, staff)
- Implement a menu system
- Add save/load functionality
- Create multiple game states (menu, playing, paused)
- Add sound effects and music
- Implement achievements and progression

See the demo game in `examples/demo_tycoon` for a complete example.
