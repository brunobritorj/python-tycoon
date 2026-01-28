# Python Tycoon Engine

A fully structured template for building 2D Tycoon/Management games in Python, featuring:

- **pygame** for rendering and game loop
- **python-socketio** for multiplayer support
- **Modular, parameterized architecture** for building different tycoon games
- **Build pipeline** supporting Windows EXE packaging (PyInstaller)

## Features

### Core Engine
- **Game Loop**: Robust pygame-based game loop with delta time
- **State Management**: Flexible state system for menus, gameplay, pause screens, etc.
- **Configuration System**: Parameterized configs for different game types
- **Entity System**: Modular entity management with serialization support
- **Resource Management**: Economy system for money and resources

### Multiplayer
- **Socket.IO Server**: Python-socketio based server for real-time multiplayer
- **Socket.IO Client**: Built-in client with state synchronization
- **Action Broadcasting**: Automatic game state sync across clients

### UI & Rendering
- **UI Components**: Pre-built buttons, panels, progress bars, text rendering
- **Extensible**: Easy to add custom UI elements

### Build System
- **PyInstaller Integration**: One-command Windows EXE building
- **Clean Scripts**: Build artifact management

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/brunobritorj/python-tycoon.git
cd python-tycoon

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt

# For building executables
pip install -r requirements-build.txt
```

### Run the Demo Game

```bash
# Run the lemonade stand demo
python -m examples.demo_tycoon.main
```

Or if installed as a package:
```bash
tycoon-demo
```

### Controls (Demo Game)
- **SPACE**: Buy production upgrade ($100)
- **UP/DOWN**: Adjust lemonade price
- **ESC**: Quit game

## Project Structure

```
python-tycoon/
├── tycoon_engine/          # Core engine
│   ├── core/               # Game loop, state management, config
│   ├── networking/         # Multiplayer client/server
│   ├── entities/           # Entity system and resource management
│   ├── ui/                 # UI components and rendering
│   └── utils/              # Helper functions
├── examples/               # Example games
│   └── demo_tycoon/        # Lemonade stand demo
├── build_tools/            # Build scripts
├── tests/                  # Unit tests
└── docs/                   # Documentation

```

## Building Your Own Tycoon Game

### 1. Create a Configuration

```python
from tycoon_engine.core.config import GameConfig

config = GameConfig(
    game_title="My Tycoon Game",
    screen_width=1280,
    screen_height=720,
    starting_money=5000.0,
    custom_params={
        'difficulty': 'medium',
        'theme': 'space'
    }
)
```

### 2. Define Game States

```python
from tycoon_engine.core.state_manager import GameState
import pygame

class MyPlayingState(GameState):
    def enter(self, **kwargs):
        # Initialize your game state
        pass
    
    def exit(self):
        # Cleanup
        pass
    
    def update(self, dt: float):
        # Update game logic
        pass
    
    def render(self, screen: pygame.Surface):
        # Render your game
        pass
    
    def handle_event(self, event: pygame.event.Event):
        # Handle input
        pass
```

### 3. Initialize and Run

```python
from tycoon_engine.core.game import Game

game = Game(config)
game.initialize()

state_manager = game.get_state_manager()
state_manager.add_state("playing", MyPlayingState(state_manager))
state_manager.change_state("playing")

game.run()
```

## Multiplayer Setup

### Start Server

```bash
# Run server on localhost:5000
tycoon-server

# Or with custom host/port
tycoon-server --host 0.0.0.0 --port 8080
```

Or programmatically:
```python
from tycoon_engine.networking.server import GameServer

server = GameServer(host="localhost", port=5000)
server.run()
```

### Connect Client

```python
from tycoon_engine.networking.client import GameClient

client = GameClient(host="localhost", port=5000)

# Set up callbacks
def on_state_update(state):
    print(f"Received state update: {state}")

client.on_state_update = on_state_update

# Connect
if client.connect():
    # Send actions
    client.send_action({
        'type': 'update_entity',
        'entity_id': 'my_building',
        'data': {'level': 2}
    })
```

## Building Windows EXE

```bash
# Build executable
python build_tools/build_exe.py

# Clean build artifacts
python build_tools/build_exe.py --clean
```

The executable will be created in the `dist/` directory.

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# With coverage
pytest --cov=tycoon_engine
```

### Code Style

```bash
# Format code
black .

# Lint code
flake8 tycoon_engine/
```

## Architecture

### Modular Design

The engine is designed to be modular and extensible:

- **Core**: Fundamental game loop and state management
- **Entities**: Flexible entity system that can represent any game object
- **Resources**: Economy management applicable to any tycoon game
- **Networking**: Drop-in multiplayer support
- **UI**: Reusable UI components

### Parameterization

Games are parameterized through:
- `GameConfig` for game-wide settings
- Entity properties for per-object customization
- Custom parameters dictionary for game-specific data

This allows multiple different tycoon games to be built on the same foundation.

## Examples

### Lemonade Stand (Included)
A simple tycoon game demonstrating core concepts:
- Resource management (money)
- Production systems
- Pricing mechanics
- Upgrades

### Other Game Ideas
The engine supports various tycoon game types:
- Restaurant/Cafe management
- Factory/Manufacturing
- Theme park builder
- City builder
- Space station management
- Farm simulation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - see LICENSE file for details

## Credits

Built with:
- [Pygame](https://www.pygame.org/) - Game development library
- [python-socketio](https://python-socketio.readthedocs.io/) - WebSocket library
- [PyInstaller](https://www.pyinstaller.org/) - Packaging tool
