"""
Multiplayer demo script showing server and client usage.

This example demonstrates:
1. Starting a server
2. Connecting clients
3. Spawning AI players
4. Sending actions
5. Chat messaging
"""

import time
import threading
from tycoon_engine.networking.server import GameServer
from tycoon_engine.networking.client import GameClient


def run_server():
    """Run the game server."""
    print("\n=== Starting Game Server ===")
    server = GameServer(host='localhost', port=5000)
    
    # Spawn some AI players after a delay
    def spawn_ai_delayed():
        time.sleep(2)
        print("\n[Server] Spawning AI players...")
        server.spawn_ai_player("AI_Trader")
        server.spawn_ai_player("AI_Builder")
    
    ai_thread = threading.Thread(target=spawn_ai_delayed, daemon=True)
    ai_thread.start()
    
    server.run()


def run_client(player_name: str, delay: float = 0):
    """
    Run a game client.
    
    Args:
        player_name: Name for the player
        delay: Delay before connecting (seconds)
    """
    if delay > 0:
        time.sleep(delay)
    
    print(f"\n=== Starting Client: {player_name} ===")
    client = GameClient(host='localhost', port=5000)
    
    # Set up event callbacks
    def on_state_update(state):
        players = state.get('players', {})
        print(f"[{player_name}] Game state updated. Players online: {len(players)}")
    
    def on_chat_message(data):
        sender = data.get('player_id', 'Unknown')[:8]
        message = data.get('message', '')
        print(f"[{player_name}] Chat from {sender}: {message}")
    
    def on_player_joined(data):
        joined_name = data.get('player_name', 'Unknown')
        is_ai = data.get('is_ai', False)
        player_type = "AI" if is_ai else "Player"
        print(f"[{player_name}] {player_type} joined: {joined_name}")
    
    def on_player_left(data):
        left_name = data.get('player_name', 'Unknown')
        print(f"[{player_name}] Player left: {left_name}")
    
    client.on_state_update = on_state_update
    client.on_chat_message = on_chat_message
    client.on_player_joined = on_player_joined
    client.on_player_left = on_player_left
    
    # Connect to server
    if client.connect(player_name=player_name):
        print(f"[{player_name}] Connected successfully!")
        
        # Perform some actions
        time.sleep(1)
        
        # Send a game action
        print(f"[{player_name}] Building a factory...")
        client.send_action({
            'type': 'update_entity',
            'entity_id': f'factory_{player_name}',
            'data': {
                'owner': player_name,
                'type': 'factory',
                'level': 1,
                'production': 10
            }
        })
        
        time.sleep(1)
        
        # Send a chat message
        print(f"[{player_name}] Sending chat message...")
        client.send_chat(f"Hello from {player_name}!")
        
        # Keep client running for a while
        time.sleep(3)
        
        # Send another action
        print(f"[{player_name}] Upgrading factory...")
        client.send_action({
            'type': 'update_entity',
            'entity_id': f'factory_{player_name}',
            'data': {
                'owner': player_name,
                'type': 'factory',
                'level': 2,
                'production': 20
            }
        })
        
        time.sleep(2)
        
        # Disconnect
        print(f"[{player_name}] Disconnecting...")
        client.disconnect()
        print(f"[{player_name}] Disconnected.")
    else:
        print(f"[{player_name}] Failed to connect to server.")


def main():
    """Main entry point for multiplayer demo."""
    print("=" * 60)
    print("Tycoon Engine - Multiplayer Demo")
    print("=" * 60)
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give server time to start
    time.sleep(1)
    
    # Start multiple clients
    client1_thread = threading.Thread(
        target=run_client, 
        args=("Player1", 1),
        daemon=True
    )
    client2_thread = threading.Thread(
        target=run_client, 
        args=("Player2", 2),
        daemon=True
    )
    
    client1_thread.start()
    client2_thread.start()
    
    # Wait for clients to finish
    client1_thread.join()
    client2_thread.join()
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
