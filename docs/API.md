# API Documentation

## Core Modules

### tycoon_engine.core.game.Game

Main game engine class that manages the pygame loop.

**Constructor:**
```python
Game(config: Optional[GameConfig] = None)
```

**Methods:**
- `initialize()`: Initialize game systems (display, clock, state manager)
- `run()`: Start the main game loop
- `quit()`: Clean up and exit
- `get_state_manager() -> StateManager`: Get the state manager instance

**Example:**
```python
from tycoon_engine import Game, GameConfig

config = GameConfig(game_title="My Game")
game = Game(config)
game.initialize()
game.run()
```

### tycoon_engine.core.config.GameConfig

Configuration dataclass for parameterizing games.

**Attributes:**
- `game_title: str` - Game window title
- `screen_width: int` - Window width in pixels
- `screen_height: int` - Window height in pixels
- `fps: int` - Target frames per second
- `starting_money: float` - Initial money for player
- `enable_multiplayer: bool` - Enable network features
- `server_host: str` - Multiplayer server host
- `server_port: int` - Multiplayer server port
- `custom_params: Dict[str, Any]` - Game-specific parameters

**Methods:**
- `from_json(path: str) -> GameConfig`: Load from JSON file
- `to_json(path: str)`: Save to JSON file
- `get_custom_param(key: str, default: Any) -> Any`: Get custom parameter

### tycoon_engine.core.state_manager.StateManager

Manages game states and transitions.

**Methods:**
- `add_state(name: str, state: GameState)`: Register a state
- `change_state(name: str, **kwargs)`: Switch to a different state
- `update(dt: float)`: Update current state
- `render(screen: pygame.Surface)`: Render current state
- `handle_event(event: pygame.event.Event)`: Handle events in current state

### tycoon_engine.core.state_manager.GameState

Abstract base class for game states.

**Abstract Methods:**
- `enter(**kwargs)`: Called when entering state
- `exit()`: Called when exiting state
- `update(dt: float)`: Update state logic
- `render(screen: pygame.Surface)`: Render state
- `handle_event(event: pygame.event.Event)`: Handle input events

## Entity System

### tycoon_engine.entities.entity.Entity

Base class for game entities.

**Constructor:**
```python
Entity(entity_id: str, entity_type: str, x: float, y: float)
```

**Methods:**
- `update(dt: float)`: Update entity logic
- `render(screen: pygame.Surface, camera_offset: Tuple[int, int])`: Render entity
- `get_property(key: str, default: Any) -> Any`: Get custom property
- `set_property(key: str, value: Any)`: Set custom property
- `to_dict() -> Dict`: Serialize to dictionary
- `from_dict(data: Dict) -> Entity`: Deserialize from dictionary

### tycoon_engine.entities.entity.EntityManager

Manages all entities in the game.

**Methods:**
- `add_entity(entity: Entity) -> bool`: Add entity
- `remove_entity(entity_id: str) -> bool`: Remove entity
- `get_entity(entity_id: str) -> Optional[Entity]`: Get entity by ID
- `get_entities_by_type(entity_type: str) -> List[Entity]`: Get entities by type
- `update_all(dt: float)`: Update all entities
- `render_all(screen: pygame.Surface, camera_offset)`: Render all entities
- `generate_id(prefix: str) -> str`: Generate unique ID

### tycoon_engine.entities.resources.ResourceManager

Manages money and resources.

**Methods:**
- `add_money(amount: float)`: Add money
- `remove_money(amount: float) -> bool`: Remove money (returns False if insufficient)
- `get_money() -> float`: Get current money
- `can_afford(amount: float) -> bool`: Check if can afford
- `add_resource(type: str, amount: float)`: Add resource
- `remove_resource(type: str, amount: float) -> bool`: Remove resource
- `get_resource(type: str) -> float`: Get resource amount
- `has_resource(type: str, amount: float) -> bool`: Check if has enough

## Networking

### tycoon_engine.networking.server.GameServer

Multiplayer server using Socket.IO.

**Constructor:**
```python
GameServer(host: str = "localhost", port: int = 5000)
```

**Methods:**
- `run()`: Start the server
- `broadcast_state()`: Broadcast game state to all clients
- `update_state(state: Dict)`: Update and broadcast state

**Events:**
- `connect`: Client connected
- `disconnect`: Client disconnected
- `player_action`: Player action received
- `chat_message`: Chat message received

### tycoon_engine.networking.client.GameClient

Multiplayer client using Socket.IO.

**Constructor:**
```python
GameClient(host: str = "localhost", port: int = 5000)
```

**Methods:**
- `connect() -> bool`: Connect to server
- `disconnect()`: Disconnect from server
- `send_action(action: Dict)`: Send action to server
- `send_chat(message: str)`: Send chat message
- `is_connected() -> bool`: Check connection status

**Callbacks:**
- `on_state_update: Callable[[Dict], None]`: State update callback
- `on_chat_message: Callable[[Dict], None]`: Chat message callback

## UI Components

### tycoon_engine.ui.renderer.UIRenderer

Helper class for rendering UI elements.

**Static Methods:**
- `draw_text(screen, text, position, font_size, color)`: Draw text
- `draw_button(screen, text, rect, bg_color, text_color)`: Draw button
- `draw_panel(screen, rect, bg_color, border_color, alpha)`: Draw panel
- `draw_progress_bar(screen, rect, progress, colors...)`: Draw progress bar

## Utilities

### tycoon_engine.utils.helpers

Utility functions.

**Functions:**
- `clamp(value, min_value, max_value) -> float`: Clamp value
- `lerp(start, end, t) -> float`: Linear interpolation
- `distance(x1, y1, x2, y2) -> float`: Calculate distance

**Classes:**
- `Timer`: Simple timer with callbacks
