"""
Multiplayer client using python-socketio.

Handles connection to game server and state synchronization.
"""

import socketio
from typing import Dict, Any, Callable, Optional
import threading


class GameClient:
    """
    Multiplayer game client using Socket.IO.
    
    Connects to game server and handles state synchronization.
    """
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        """
        Initialize game client.
        
        Args:
            host: Server host address
            port: Server port
        """
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}"
        self.sio = socketio.Client()
        self.connected = False
        self.player_id: Optional[str] = None
        self.player_name: Optional[str] = None
        
        # Callbacks for events
        self.on_state_update: Optional[Callable[[Dict[str, Any]], None]] = None
        self.on_chat_message: Optional[Callable[[Dict[str, Any]], None]] = None
        self.on_player_joined: Optional[Callable[[Dict[str, Any]], None]] = None
        self.on_player_left: Optional[Callable[[Dict[str, Any]], None]] = None
        
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up Socket.IO event handlers."""
        
        @self.sio.event
        def connect():
            """Handle connection to server."""
            print(f"Connected to server at {self.url}")
            self.connected = True
        
        @self.sio.event
        def disconnect():
            """Handle disconnection from server."""
            print("Disconnected from server")
            self.connected = False
        
        @self.sio.event
        def game_state(data):
            """Handle game state updates from server."""
            if self.on_state_update:
                self.on_state_update(data)
        
        @self.sio.event
        def chat_message(data):
            """Handle chat messages."""
            if self.on_chat_message:
                self.on_chat_message(data)
        
        @self.sio.event
        def player_joined(data):
            """Handle player joined event."""
            if self.on_player_joined:
                self.on_player_joined(data)
        
        @self.sio.event
        def player_left(data):
            """Handle player left event."""
            if self.on_player_left:
                self.on_player_left(data)
    
    def connect(self, player_name: Optional[str] = None) -> bool:
        """
        Connect to the game server.
        
        Args:
            player_name: Optional player name to use when joining
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.sio.connect(self.url)
            self.player_name = player_name
            
            # Send join message if player name provided
            if player_name:
                self.join(player_name)
            
            return True
        except socketio.exceptions.ConnectionError as e:
            print(f"Failed to connect to {self.url}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error connecting to {self.url}: {e}")
            return False
    
    def join(self, player_name: str) -> None:
        """
        Send join message to server with player name.
        
        Args:
            player_name: Player name to use
        """
        if self.connected:
            self.player_name = player_name
            self.sio.emit('join', {'player_name': player_name})
    
    def disconnect(self) -> None:
        """Disconnect from the game server."""
        if self.connected:
            self.sio.disconnect()
    
    def send_action(self, action: Dict[str, Any]) -> None:
        """
        Send a player action to the server.
        
        Args:
            action: Action data dictionary
        """
        if self.connected:
            self.sio.emit('player_action', action)
    
    def send_chat(self, message: str) -> None:
        """
        Send a chat message.
        
        Args:
            message: Chat message text
        """
        if self.connected:
            self.sio.emit('chat_message', {'message': message})
    
    def is_connected(self) -> bool:
        """Check if connected to server."""
        return self.connected
