"""
Multiplayer server using python-socketio.

Handles client connections and game state synchronization.
"""

import socketio
import eventlet
import time
from typing import Dict, Any, Optional
import json


class GameServer:
    """
    Multiplayer game server using Socket.IO.
    
    Manages client connections and synchronizes game state across clients.
    
    Security Note: This implementation uses CORS with allowed_origins='*' for 
    development convenience. In production, configure CORS to only allow 
    trusted origins by passing a specific list or domain pattern.
    """
    
    def __init__(self, host: str = "localhost", port: int = 5000, cors_origins: str = '*'):
        """
        Initialize game server.
        
        Args:
            host: Server host address
            port: Server port
            cors_origins: CORS allowed origins ('*' for all, or specific origins)
        """
        self.host = host
        self.port = port
        self.sio = socketio.Server(cors_allowed_origins=cors_origins)
        self.app = socketio.WSGIApp(self.sio)
        
        # Game state
        self.clients: Dict[str, Dict[str, Any]] = {}
        self.ai_players: Dict[str, Dict[str, Any]] = {}
        self.game_state: Dict[str, Any] = {
            'entities': {},
            'resources': {},
            'players': {},
            'tick': 0
        }
        self.ai_counter = 0
        
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up Socket.IO event handlers."""
        
        @self.sio.event
        def connect(sid, environ):
            """Handle client connection."""
            print(f"Client connected: {sid}")
            self.clients[sid] = {
                'player_id': sid,
                'connected_at': time.time(),
                'player_name': None
            }
            # Send current game state to new client
            self.sio.emit('game_state', self.game_state, room=sid)
        
        @self.sio.event
        def join(sid, data):
            """Handle player join with name."""
            # Validate data
            if not isinstance(data, dict):
                print(f"Invalid join data from {sid}: not a dictionary")
                return
            
            player_name = data.get('player_name', f'Player_{sid[:8]}')
            
            # Validate and sanitize player name
            if not isinstance(player_name, str):
                player_name = f'Player_{sid[:8]}'
            player_name = player_name[:50].strip()  # Limit length and trim whitespace
            if not player_name:
                player_name = f'Player_{sid[:8]}'
            
            # Check if player already joined
            if sid in self.game_state['players']:
                print(f"Player {sid} already joined, ignoring duplicate join")
                return
            
            print(f"Player joined: {player_name} (sid: {sid})")
            
            # Verify client exists (handle race condition)
            if sid not in self.clients:
                print(f"Client {sid} not found in clients list, cannot join")
                return
            
            # Update client info
            self.clients[sid]['player_name'] = player_name
            
            # Add player to game state
            self.game_state['players'][sid] = {
                'player_id': sid,
                'player_name': player_name,
                'joined_at': time.time(),
                'is_ai': False
            }
            
            # Broadcast player join event (always include is_ai for consistency)
            self.sio.emit('player_joined', {
                'player_id': sid,
                'player_name': player_name,
                'is_ai': False
            })
            
            # Send updated game state
            self.broadcast_state()
        
        @self.sio.event
        def disconnect(sid):
            """Handle client disconnection."""
            player_name = self.clients.get(sid, {}).get('player_name', 'Unknown')
            print(f"Client disconnected: {player_name} (sid: {sid})")
            
            # Check if player was actually in the game (had joined)
            was_in_game = sid in self.game_state['players']
            
            # Remove player from game state
            if was_in_game:
                del self.game_state['players'][sid]
            
            # Remove client
            if sid in self.clients:
                del self.clients[sid]
            
            # Only broadcast player_left if player had officially joined
            if was_in_game:
                self.sio.emit('player_left', {
                    'player_id': sid,
                    'player_name': player_name,
                    'is_ai': False
                })
                
                # Send updated game state
                self.broadcast_state()
        
        @self.sio.event
        def player_action(sid, data):
            """Handle player actions."""
            # Validate data
            if not isinstance(data, dict):
                print(f"Invalid action data from {sid}: not a dictionary")
                return
            
            print(f"Action from {sid}: {data}")
            # Process action and update game state
            self._process_action(sid, data)
            # Broadcast updated state to all clients
            self.broadcast_state()
        
        @self.sio.event
        def chat_message(sid, data):
            """Handle chat messages."""
            # Validate data
            if not isinstance(data, dict):
                print(f"Invalid chat data from {sid}: not a dictionary")
                return
            
            # Validate and limit message length
            message_text = data.get('message', '')
            if not isinstance(message_text, str):
                print(f"Invalid message type from {sid}")
                return
            
            # Limit message length to 500 characters
            message_text = message_text[:500]
            
            message = {
                'player_id': sid,
                'message': message_text,
                'timestamp': time.time()
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
            
            # Validate entity_id
            if not entity_id or not isinstance(entity_id, str):
                print(f"Invalid entity_id in action from {player_id}")
                return
            
            # Limit entity_id length
            entity_id = entity_id[:100]
            
            if entity_data and isinstance(entity_data, dict):
                self.game_state['entities'][entity_id] = entity_data
        
        elif action_type == 'remove_entity':
            entity_id = action.get('entity_id')
            
            # Validate entity_id
            if not entity_id or not isinstance(entity_id, str):
                print(f"Invalid entity_id in remove action from {player_id}")
                return
            
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
    
    def spawn_ai_player(self, ai_name: Optional[str] = None) -> str:
        """
        Spawn an AI player (placeholder logic).
        
        Args:
            ai_name: Optional name for the AI player
        
        Returns:
            AI player ID
        """
        self.ai_counter += 1
        ai_id = f"ai_{self.ai_counter}"
        
        if ai_name is None:
            ai_name = f"AI_Bot_{self.ai_counter}"
        
        print(f"Spawning AI player: {ai_name} (id: {ai_id})")
        
        # Add AI player to tracking
        self.ai_players[ai_id] = {
            'player_id': ai_id,
            'player_name': ai_name,
            'created_at': time.time()
        }
        
        # Add AI player to game state
        self.game_state['players'][ai_id] = {
            'player_id': ai_id,
            'player_name': ai_name,
            'joined_at': time.time(),
            'is_ai': True
        }
        
        # Broadcast AI player join
        self.sio.emit('player_joined', {
            'player_id': ai_id,
            'player_name': ai_name,
            'is_ai': True
        })
        
        # Send updated game state
        self.broadcast_state()
        
        return ai_id
    
    def remove_ai_player(self, ai_id: str) -> bool:
        """
        Remove an AI player.
        
        Args:
            ai_id: AI player ID to remove
        
        Returns:
            True if AI player was removed, False otherwise
        """
        if ai_id not in self.ai_players:
            return False
        
        ai_name = self.ai_players[ai_id]['player_name']
        print(f"Removing AI player: {ai_name} (id: {ai_id})")
        
        # Remove from tracking
        del self.ai_players[ai_id]
        
        # Remove from game state
        if ai_id in self.game_state['players']:
            del self.game_state['players'][ai_id]
        
        # Broadcast AI player leave
        self.sio.emit('player_left', {
            'player_id': ai_id,
            'player_name': ai_name,
            'is_ai': True
        })
        
        # Send updated game state
        self.broadcast_state()
        
        return True
    
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
    parser.add_argument(
        '--cors-origins', 
        default='*', 
        help='CORS allowed origins (default: * for development, use specific origins in production)'
    )
    
    args = parser.parse_args()
    
    server = GameServer(host=args.host, port=args.port, cors_origins=args.cors_origins)
    server.run()


if __name__ == '__main__':
    main()
