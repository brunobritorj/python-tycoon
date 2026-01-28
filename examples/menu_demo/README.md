# Menu Demo Example

This example demonstrates the complete menu system and UI components of the Python Tycoon engine.

## Features Demonstrated

### Menu Screens
- **Main Menu**: Title screen with Play, Multiplayer, Settings, and Quit buttons
- **Settings Menu**: Configure volume, resolution, and graphics settings
- **Multiplayer Menu**: Host or join multiplayer games
- **Pause Menu**: In-game menu for Resume, Settings, and Quit

### UI Components
- **Buttons**: Clickable buttons with hover states
- **Labels**: Text rendering with alignment options
- **Panels**: Container elements with backgrounds
- **TextInput**: Input fields for user text entry
- **HUD**: In-game heads-up display for stats and resources

### Event System
- Priority-based event handling
- Custom game events
- Keyboard and mouse event support

### Asset Loading
- Image loading with caching
- Font management
- Sound and music support (when audio is available)

## Running the Demo

```bash
# From the repository root
python -m examples.menu_demo.main

# Or if installed as a package
python -c "from examples.menu_demo.main import main; main()"
```

## Navigation

- **Main Menu**:
  - Click "Play" to start the game
  - Click "Multiplayer" to access multiplayer options
  - Click "Settings" to configure game options
  - Click "Quit" or press ESC to exit

- **In-Game**:
  - Press ESC or click the "Menu" button to pause
  - Watch the money and score increase over time

- **Settings Menu**:
  - Use +/- buttons to adjust volume levels
  - Use arrow buttons to change resolution
  - Toggle fullscreen mode
  - Click "Apply" to save changes
  - Click "Back" to return to main menu

- **Multiplayer Menu**:
  - Choose "Host Game" to start a server
  - Choose "Join Game" to connect to a server
  - Enter host and port information
  - Click "Back" to return to main menu

## Code Structure

The demo is organized as follows:

1. **Configuration**: Set up game config with title, resolution, FPS, etc.
2. **Game Initialization**: Create and initialize the game engine
3. **State Setup**: Create and register all game states
   - Main Menu
   - Settings
   - Multiplayer
   - Playing (with HUD)
   - Pause Menu
4. **State Management**: Define transitions between states
5. **Game Loop**: Run the game loop

## Key Concepts

### State Pattern
Each screen is a separate state that can be entered and exited independently. This allows for clean separation of concerns and easy navigation.

### UI Components
UI elements are managed by the `UIManager`, which handles rendering order, event routing, and focus management.

### HUD Integration
The in-game HUD is not a full state but a reusable component that can be integrated into any playing state.

### Event Handling
Events flow from pygame → Game Loop → State Manager → Active State → UI Manager → UI Components

## Customization

You can customize the demo by:

1. **Changing Colors**: Modify the `background_color` parameter for menu screens
2. **Adding Resources**: Display additional resources in the HUD
3. **Custom Callbacks**: Provide custom callbacks for button actions
4. **New States**: Add new game states by extending `GameState`
5. **UI Elements**: Create custom UI components by extending `UIComponent`

## Dependencies

- pygame >= 2.5.0
- PyYAML >= 6.0.0 (for YAML config support)

## Notes

- The demo runs in a window by default (1280x720)
- Audio features require a sound card (gracefully skipped if unavailable)
- The game loop runs at 60 FPS by default
- All menu screens support keyboard navigation (ESC to go back)
