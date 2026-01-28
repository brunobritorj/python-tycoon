"""
Multiplayer server using python-socketio.

Handles client connections and game state synchronization.
"""

import socketio
import eventlet
from typing import Dict, Any, Optional
import json


class GameServer:
    """
    Multiplayer game server using Socket.IO.
    
    Manages client connections and synchronizes game state across clients.
    """
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        """
        Initialize game server.
        
        Args:
            host: Server host address
            port: Server port
        """
        self.host = host
        self.port = port
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        
        # Game state
        self.clients: Dict[str, Dict[str, Any]] = {}
        self.game_state: Dict[str, Any] = {
            'entities': {},
            'resources': {},
            'tick': 0
        }
        
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up Socket.IO event handlers."""
        
        @self.sio.event
        def connect(sid, environ):
            """Handle client connection."""
            print(f"Client connected: {sid}")
            self.clients[sid] = {
                'player_id': sid,
                'connected_at': eventlet.time.time()
            }
            # Send current game state to new client
            self.sio.emit('game_state', self.game_state, room=sid)
        
        @self.sio.event
        def disconnect(sid):
            """Handle client disconnection."""
            print(f"Client disconnected: {sid}")
            if sid in self.clients:
                del self.clients[sid]
        
        @self.sio.event
        def player_action(sid, data):
            """Handle player actions."""
            print(f"Action from {sid}: {data}")
            # Process action and update game state
            self._process_action(sid, data)
            # Broadcast updated state to all clients
            self.broadcast_state()
        
        @self.sio.event
        def chat_message(sid, data):
            """Handle chat messages."""
            message = {
                'player_id': sid,
                'message': data.get('message', ''),
                'timestamp': eventlet.time.time()
            }
            self.sio.emit('chat_message', message)
    
    def _process_action(self, player_id: str, action: Dict[str, Any]) -> None:
        """
        Process a player action and update game state.
        
        Args:
            player_id: ID of the player performing the action
            action: Action data dictionary
        """
        action_type = action.get('type')
        
        if action_type == 'update_entity':
            entity_id = action.get('entity_id')
            entity_data = action.get('data')
            if entity_id and entity_data:
                self.game_state['entities'][entity_id] = entity_data
        
        elif action_type == 'remove_entity':
            entity_id = action.get('entity_id')
            if entity_id in self.game_state['entities']:
                del self.game_state['entities'][entity_id]
        
        # Increment tick counter
        self.game_state['tick'] += 1
    
    def broadcast_state(self) -> None:
        """Broadcast current game state to all connected clients."""
        self.sio.emit('game_state', self.game_state)
    
    def update_state(self, state: Dict[str, Any]) -> None:
        """Update server game state."""
        self.game_state.update(state)
        self.broadcast_state()
    
    def run(self) -> None:
        """Start the server."""
        print(f"Starting game server on {self.host}:{self.port}")
        eventlet.wsgi.server(eventlet.listen((self.host, self.port)), self.app)


def main():
    """Main entry point for running the server."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Tycoon Game Server')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=5000, help='Server port')
    
    args = parser.parse_args()
    
    server = GameServer(host=args.host, port=args.port)
    server.run()


if __name__ == '__main__':
    main()
