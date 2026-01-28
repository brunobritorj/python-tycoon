# Multiplayer Protocol Documentation

This document describes the Socket.IO-based multiplayer protocol used in the Tycoon Engine.

## Overview

The multiplayer system uses Socket.IO for real-time bidirectional communication between the server and clients. The protocol supports player management, game state synchronization, actions, and chat messaging.

## Connection Flow

1. Client connects to server using Socket.IO
2. Server sends initial `game_state` to the client
3. Client sends `join` message with player information
4. Server broadcasts `player_joined` event to all clients
5. Clients and server exchange messages during gameplay
6. On disconnect, server broadcasts `player_left` event

## Message Types

### 1. connect (Built-in Socket.IO Event)

**Direction:** Client → Server (automatic)

**Description:** Fired automatically when a client establishes a connection to the server.

**Server Response:**
- Assigns a session ID (sid) to the client
- Sends current `game_state` to the new client
- Stores client in internal client list

### 2. join

**Direction:** Client → Server

**Description:** Sent by client after connecting to provide player information and officially join the game.

**Payload:**
```json
{
    "player_name": "string"
}
```

**Fields:**
- `player_name` (string): Display name for the player

**Server Actions:**
- Updates client information with player name
- Adds player to game state's `players` dictionary
- Broadcasts `player_joined` event to all clients
- Sends updated `game_state` to all clients

**Example:**
```python
client.join("PlayerOne")
# or during connect:
client.connect(player_name="PlayerOne")
```

### 3. state_update (game_state)

**Direction:** Server → Client(s)

**Description:** Broadcasts the current game state to connected clients. Sent initially on connection and whenever game state changes.

**Payload:**
```json
{
    "entities": {},
    "resources": {},
    "players": {
        "player_id": {
            "player_id": "string",
            "player_name": "string",
            "joined_at": "timestamp",
            "is_ai": "boolean"
        }
    },
    "tick": "number"
}
```

**Fields:**
- `entities` (dict): Game entities (buildings, units, etc.)
- `resources` (dict): Game resources (money, materials, etc.)
- `players` (dict): Connected players and AI players
- `tick` (number): Game tick counter

**Client Callback:**
```python
def on_state_update(state):
    print(f"Players online: {len(state['players'])}")

client.on_state_update = on_state_update
```

### 4. player_action

**Direction:** Client → Server

**Description:** Sends a player action to the server for processing.

**Payload:**
```json
{
    "type": "string",
    "entity_id": "string",
    "data": {}
}
```

**Fields:**
- `type` (string): Action type (e.g., "update_entity", "remove_entity")
- `entity_id` (string): ID of the entity being affected
- `data` (dict): Action-specific data

**Action Types:**

#### update_entity
Creates or updates an entity in the game state.

```json
{
    "type": "update_entity",
    "entity_id": "building_1",
    "data": {
        "owner": "player_1",
        "type": "factory",
        "level": 2,
        "health": 100
    }
}
```

#### remove_entity
Removes an entity from the game state.

```json
{
    "type": "remove_entity",
    "entity_id": "building_1"
}
```

**Server Actions:**
- Processes the action
- Updates game state accordingly
- Increments tick counter
- Broadcasts updated `game_state` to all clients

**Example:**
```python
client.send_action({
    'type': 'update_entity',
    'entity_id': 'my_building',
    'data': {'level': 2}
})
```

### 5. chat

**Direction:** Bidirectional

**Client → Server (chat_message):**
```json
{
    "message": "string"
}
```

**Server → Client(s) (chat_message):**
```json
{
    "player_id": "string",
    "message": "string",
    "timestamp": "number"
}
```

**Description:** Sends and receives chat messages between players.

**Fields:**
- `message` (string): Chat message text
- `player_id` (string): ID of the player who sent the message
- `timestamp` (number): Unix timestamp of when the message was sent

**Example:**
```python
# Sending
client.send_chat("Hello, everyone!")

# Receiving
def on_chat_message(data):
    print(f"{data['player_id']}: {data['message']}")

client.on_chat_message = on_chat_message
```

### 6. disconnect (Built-in Socket.IO Event)

**Direction:** Client → Server (automatic)

**Description:** Fired automatically when a client disconnects from the server.

**Server Actions:**
- Removes player from game state's `players` dictionary
- Removes client from internal client list
- Broadcasts `player_left` event to all remaining clients
- Sends updated `game_state` to all clients

### 7. player_joined

**Direction:** Server → Client(s)

**Description:** Broadcast when a new player (human or AI) joins the game.

**Payload:**
```json
{
    "player_id": "string",
    "player_name": "string",
    "is_ai": "boolean"
}
```

**Fields:**
- `player_id` (string): Unique ID for the player
- `player_name` (string): Display name
- `is_ai` (boolean, optional): True if this is an AI player

**Example:**
```python
def on_player_joined(data):
    player_type = "AI" if data.get('is_ai') else "Player"
    print(f"{player_type} joined: {data['player_name']}")

client.on_player_joined = on_player_joined
```

### 8. player_left

**Direction:** Server → Client(s)

**Description:** Broadcast when a player (human or AI) leaves the game.

**Payload:**
```json
{
    "player_id": "string",
    "player_name": "string",
    "is_ai": "boolean"
}
```

**Fields:**
- `player_id` (string): Unique ID for the player who left
- `player_name` (string): Display name
- `is_ai` (boolean, optional): True if this was an AI player

**Example:**
```python
def on_player_left(data):
    print(f"Player left: {data['player_name']}")

client.on_player_left = on_player_left
```

## AI Players

The server supports spawning AI players (bots) with placeholder logic.

### Spawning AI Players

**Server-side:**
```python
server = GameServer(host='localhost', port=5000)

# Spawn AI with default name
ai_id = server.spawn_ai_player()

# Spawn AI with custom name
ai_id = server.spawn_ai_player(ai_name="TradingBot")
```

**Behavior:**
- AI players are added to the `players` dictionary in game state
- AI players have `is_ai: True` flag
- `player_joined` event is broadcast to all clients
- AI players persist until explicitly removed

### Removing AI Players

```python
success = server.remove_ai_player(ai_id)
```

**Behavior:**
- Removes AI from game state
- Broadcasts `player_left` event
- Returns `True` if successful, `False` if AI not found

## Usage Examples

### Starting a Server

**Command Line:**
```bash
tycoon-server --host 0.0.0.0 --port 5000
```

**Python:**
```python
from tycoon_engine.networking.server import GameServer

server = GameServer(host='localhost', port=5000)

# Spawn AI players
server.spawn_ai_player("AI_Trader")
server.spawn_ai_player("AI_Builder")

# Run server
server.run()
```

### Connecting a Client

```python
from tycoon_engine.networking.client import GameClient

# Create client
client = GameClient(host='localhost', port=5000)

# Set up event callbacks
def on_state_update(state):
    print(f"State updated: {state['tick']} ticks")

def on_player_joined(data):
    print(f"Player joined: {data['player_name']}")

client.on_state_update = on_state_update
client.on_player_joined = on_player_joined

# Connect with player name
if client.connect(player_name="MyPlayer"):
    # Send actions
    client.send_action({
        'type': 'update_entity',
        'entity_id': 'my_factory',
        'data': {'level': 1, 'production': 10}
    })
    
    # Send chat
    client.send_chat("Hello, world!")
    
    # Later...
    client.disconnect()
```

### Full Example

See `examples/multiplayer_demo.py` for a complete working example with server, multiple clients, and AI players.

## Security Considerations

### CORS Configuration

By default, the server uses `cors_allowed_origins='*'` for development convenience. **This should be changed in production.**

**Development:**
```python
server = GameServer(host='localhost', port=5000, cors_origins='*')
```

**Production:**
```python
# Allow specific origins only
server = GameServer(
    host='0.0.0.0', 
    port=5000, 
    cors_origins='https://yourgame.com'
)
```

### Input Validation

The server performs minimal input validation on actions. For production use, you should:

1. Validate action types
2. Sanitize entity IDs and data
3. Implement authentication
4. Add rate limiting
5. Validate player permissions

### Example Validation

```python
def _process_action(self, player_id: str, action: Dict[str, Any]) -> None:
    """Process a player action with validation."""
    # Validate action type
    allowed_types = ['update_entity', 'remove_entity']
    action_type = action.get('type')
    
    if action_type not in allowed_types:
        print(f"Invalid action type: {action_type}")
        return
    
    # Validate entity ownership
    entity_id = action.get('entity_id')
    if not entity_id or not isinstance(entity_id, str):
        print(f"Invalid entity_id")
        return
    
    # Process action...
```

## Testing

Run the test suite:

```bash
pytest tests/test_networking.py -v
```

Tests cover:
- Server initialization
- Client connection and disconnection
- AI player spawning and removal
- Action processing
- Chat messaging
- All protocol message types
- Event callbacks

## Troubleshooting

### Connection Failed

**Issue:** Client cannot connect to server

**Solutions:**
- Ensure server is running
- Check host and port are correct
- Verify firewall settings allow the port
- Check for port conflicts

### State Not Syncing

**Issue:** Client not receiving state updates

**Solutions:**
- Verify `on_state_update` callback is set
- Check network connectivity
- Ensure client is properly connected
- Look for errors in server logs

### Chat Not Working

**Issue:** Chat messages not being received

**Solutions:**
- Verify `on_chat_message` callback is set
- Check client is connected
- Ensure server is broadcasting chat messages
- Look for socket.io version mismatches

## Performance Considerations

### State Broadcasting

The server broadcasts the entire game state on every update. For large games, consider:

1. **Delta Updates:** Only send changed data
2. **Throttling:** Limit broadcast frequency
3. **Selective Broadcasting:** Send state only to affected clients
4. **Compression:** Use message compression for large payloads

### Example Throttling

```python
import time

class GameServer:
    def __init__(self, ...):
        self.last_broadcast = 0
        self.broadcast_interval = 0.1  # 100ms
    
    def broadcast_state(self):
        now = time.time()
        if now - self.last_broadcast >= self.broadcast_interval:
            self.sio.emit('game_state', self.game_state)
            self.last_broadcast = now
```

## Future Enhancements

Potential improvements to the multiplayer system:

1. **Authentication:** Player login and session management
2. **Persistence:** Save game state to database
3. **Rooms:** Support multiple game rooms/instances
4. **Spectators:** Allow spectator mode
5. **Replays:** Record and replay game sessions
6. **AI Logic:** Implement actual AI player behavior
7. **Lobby System:** Pre-game lobby with ready checks
8. **Reconnection:** Handle client reconnection gracefully
9. **Admin Commands:** Server administration tools
10. **Metrics:** Performance monitoring and analytics
