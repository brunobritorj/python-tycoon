"""
AI player system for tycoon games.

Provides a simple decision loop with hooks for future expansion.
"""

from typing import Dict, Any, Callable, Optional, List
from enum import Enum
from ..entities.resources import ResourceManager


class AIPlayerState(Enum):
    """States for AI player behavior."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"


class AIPlayer:
    """
    Represents an AI-controlled player in the game.
    
    This is a placeholder system with a simple decision loop that can be
    extended with custom behavior.
    """
    
    def __init__(
        self,
        player_id: str,
        name: str,
        resource_manager: Optional[ResourceManager] = None,
        difficulty: str = "medium"
    ):
        """
        Initialize an AI player.
        
        Args:
            player_id: Unique identifier for this AI player
            name: Display name for the AI player
            resource_manager: Optional resource manager (creates new if not provided)
            difficulty: Difficulty level ("easy", "medium", "hard")
        """
        self.id = player_id
        self.name = name
        self.resource_manager = resource_manager or ResourceManager(starting_money=10000.0)
        self.difficulty = difficulty
        
        # AI state
        self.state = AIPlayerState.IDLE
        self._decision_timer = 0.0
        self._decision_interval = self._get_decision_interval()
        
        # Decision hooks - functions that can be called during decision making
        self._decision_hooks: List[Callable[[Any], Any]] = []
        
        # Action queue for planned actions
        self._action_queue: List[Dict[str, Any]] = []
        
        # Statistics
        self.actions_taken = 0
        self.decisions_made = 0
    
    def _get_decision_interval(self) -> float:
        """Get decision interval based on difficulty."""
        intervals = {
            "easy": 5.0,    # Decisions every 5 seconds
            "medium": 3.0,  # Decisions every 3 seconds
            "hard": 1.5     # Decisions every 1.5 seconds
        }
        return intervals.get(self.difficulty, 3.0)
    
    def update(self, dt: float, game_state: Optional[Dict[str, Any]] = None) -> None:
        """
        Update the AI player's decision loop.
        
        Args:
            dt: Delta time in seconds
            game_state: Optional game state information for decision making
        """
        self._decision_timer += dt
        
        # Check if it's time to make a decision
        if self._decision_timer >= self._decision_interval:
            self._decision_timer = 0.0
            self._make_decision(game_state)
        
        # Execute queued actions
        self._execute_actions(dt)
    
    def _make_decision(self, game_state: Optional[Dict[str, Any]] = None) -> None:
        """
        Make a decision based on current game state.
        
        This is a simple placeholder that calls registered hooks.
        Subclasses or custom hooks can implement actual AI logic.
        
        Args:
            game_state: Current game state for decision making
        """
        self.state = AIPlayerState.PLANNING
        
        # Call all decision hooks
        for hook in self._decision_hooks:
            action = hook(game_state)
            if action:
                self._action_queue.append(action)
        
        self.decisions_made += 1
        
        # Transition to executing if we have actions
        if self._action_queue:
            self.state = AIPlayerState.EXECUTING
        else:
            self.state = AIPlayerState.IDLE
    
    def _execute_actions(self, dt: float) -> None:
        """
        Execute queued actions.
        
        Args:
            dt: Delta time in seconds
        """
        if not self._action_queue:
            return
        
        # Process actions (this is a placeholder - actual execution would be game-specific)
        actions_to_remove = []
        
        for action in self._action_queue:
            # Check if action can be executed
            if self._can_execute_action(action):
                self._execute_action(action)
                actions_to_remove.append(action)
                self.actions_taken += 1
        
        # Remove executed actions
        for action in actions_to_remove:
            self._action_queue.remove(action)
        
        # Update state
        if not self._action_queue:
            self.state = AIPlayerState.IDLE
    
    def _can_execute_action(self, action: Dict[str, Any]) -> bool:
        """
        Check if an action can be executed.
        
        This is a placeholder that can be extended with actual logic.
        
        Args:
            action: Action dictionary to check
            
        Returns:
            True if action can be executed
        """
        # Check if action has a cost and if we can afford it
        cost = action.get('cost', 0)
        if cost > 0:
            return self.resource_manager.can_afford(cost)
        return True
    
    def _execute_action(self, action: Dict[str, Any]) -> bool:
        """
        Execute an action.
        
        This is a placeholder that can be extended with actual logic.
        
        Args:
            action: Action dictionary to execute
            
        Returns:
            True if execution was successful
        """
        # Deduct cost if any
        cost = action.get('cost', 0)
        if cost > 0:
            if not self.resource_manager.remove_money(cost):
                return False
        
        # Action execution would happen here (game-specific)
        return True
    
    def add_decision_hook(self, hook: Callable[[Any], Any]) -> None:
        """
        Add a decision-making hook.
        
        Hooks are called during the decision phase and can return actions
        to be added to the action queue.
        
        Args:
            hook: Function that takes game state and returns an action dict or None
        """
        self._decision_hooks.append(hook)
    
    def remove_decision_hook(self, hook: Callable[[Any], Any]) -> bool:
        """
        Remove a decision hook.
        
        Args:
            hook: The hook function to remove
            
        Returns:
            True if removed, False if not found
        """
        try:
            self._decision_hooks.remove(hook)
            return True
        except ValueError:
            return False
    
    def queue_action(self, action: Dict[str, Any]) -> None:
        """
        Manually queue an action for execution.
        
        Args:
            action: Action dictionary to queue
        """
        self._action_queue.append(action)
    
    def clear_action_queue(self) -> None:
        """Clear all queued actions."""
        self._action_queue.clear()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get AI player statistics.
        
        Returns:
            Dictionary with AI statistics
        """
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'state': self.state.value,
            'actions_taken': self.actions_taken,
            'decisions_made': self.decisions_made,
            'queued_actions': len(self._action_queue),
            'money': self.resource_manager.get_money()
        }


class AIPlayerManager:
    """
    Manages multiple AI players in the game.
    
    Provides centralized management and update loop for all AI players.
    """
    
    def __init__(self):
        """Initialize the AI player manager."""
        self.ai_players: Dict[str, AIPlayer] = {}
    
    def add_ai_player(self, ai_player: AIPlayer) -> bool:
        """
        Add an AI player to the manager.
        
        Args:
            ai_player: The AI player to add
            
        Returns:
            True if added, False if ID already exists
        """
        if ai_player.id in self.ai_players:
            return False
        
        self.ai_players[ai_player.id] = ai_player
        return True
    
    def remove_ai_player(self, player_id: str) -> bool:
        """
        Remove an AI player by ID.
        
        Args:
            player_id: ID of the AI player to remove
            
        Returns:
            True if removed, False if not found
        """
        if player_id in self.ai_players:
            del self.ai_players[player_id]
            return True
        return False
    
    def get_ai_player(self, player_id: str) -> Optional[AIPlayer]:
        """
        Get an AI player by ID.
        
        Args:
            player_id: ID of the AI player
            
        Returns:
            AI player or None if not found
        """
        return self.ai_players.get(player_id)
    
    def get_all_ai_players(self) -> List[AIPlayer]:
        """
        Get all AI players.
        
        Returns:
            List of all AI players
        """
        return list(self.ai_players.values())
    
    def update_all(self, dt: float, game_state: Optional[Dict[str, Any]] = None) -> None:
        """
        Update all AI players.
        
        Args:
            dt: Delta time in seconds
            game_state: Optional game state for decision making
        """
        for ai_player in self.ai_players.values():
            ai_player.update(dt, game_state)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics for all AI players.
        
        Returns:
            Dictionary with aggregated statistics
        """
        total_actions = sum(ai.actions_taken for ai in self.ai_players.values())
        total_decisions = sum(ai.decisions_made for ai in self.ai_players.values())
        
        return {
            'total_ai_players': len(self.ai_players),
            'total_actions_taken': total_actions,
            'total_decisions_made': total_decisions,
            'players': {
                player_id: ai.get_statistics()
                for player_id, ai in self.ai_players.items()
            }
        }
    
    def clear(self) -> None:
        """Remove all AI players."""
        self.ai_players.clear()
