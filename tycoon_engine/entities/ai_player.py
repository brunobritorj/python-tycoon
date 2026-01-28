"""
AI player system for tycoon games.

Provides simple AI decision-making with hooks for expansion.
"""

from typing import Dict, Optional, Callable, Any, List
from dataclasses import dataclass, field
from enum import Enum
import random


class AIDecisionType(Enum):
    """Types of decisions AI can make."""
    IDLE = "idle"
    BUILD = "build"
    UPGRADE = "upgrade"
    SELL = "sell"
    TRADE = "trade"
    CUSTOM = "custom"


@dataclass
class AIDecision:
    """Represents a decision made by AI."""
    decision_type: AIDecisionType
    priority: float = 0.0
    data: Dict[str, Any] = field(default_factory=dict)


class AIPlayer:
    """
    AI player with simple decision loop.
    
    Provides basic AI behavior with extensible hooks for custom logic.
    """
    
    def __init__(
        self,
        player_id: str,
        name: str,
        difficulty: str = "medium",
        decision_interval: float = 5.0
    ):
        """
        Initialize AI player.
        
        Args:
            player_id: Unique identifier for this AI player
            name: Display name for the AI player
            difficulty: AI difficulty level ('easy', 'medium', 'hard')
            decision_interval: Time between decisions in seconds
        """
        self.player_id = player_id
        self.name = name
        self.difficulty = difficulty
        self.decision_interval = decision_interval
        
        self.accumulated_time = 0.0
        self.decision_count = 0
        self.last_decision: Optional[AIDecision] = None
        
        # State tracking
        self.properties: Dict[str, Any] = {}
        
        # Hooks for custom behavior
        self.on_decision_hook: Optional[Callable[[AIDecision], None]] = None
        self.decision_maker_hook: Optional[Callable[['AIPlayer'], AIDecision]] = None
    
    def update(self, dt: float) -> Optional[AIDecision]:
        """
        Update AI player and potentially make a decision.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            AIDecision if a decision was made, None otherwise
        """
        self.accumulated_time += dt
        
        if self.accumulated_time >= self.decision_interval:
            self.accumulated_time -= self.decision_interval
            return self._make_decision()
        
        return None
    
    def _make_decision(self) -> AIDecision:
        """
        Make a decision based on current state.
        
        Uses custom hook if provided, otherwise uses default logic.
        
        Returns:
            AIDecision object
        """
        self.decision_count += 1
        
        # Use custom decision maker if provided
        if self.decision_maker_hook:
            decision = self.decision_maker_hook(self)
        else:
            decision = self._default_decision_logic()
        
        self.last_decision = decision
        
        # Trigger decision callback
        if self.on_decision_hook:
            self.on_decision_hook(decision)
        
        return decision
    
    def _default_decision_logic(self) -> AIDecision:
        """
        Default decision-making logic.
        
        Simple random decision based on difficulty level.
        
        Returns:
            AIDecision object
        """
        # Difficulty affects decision probability
        difficulty_weights = {
            'easy': [0.5, 0.2, 0.15, 0.1, 0.05],
            'medium': [0.3, 0.25, 0.2, 0.15, 0.1],
            'hard': [0.1, 0.3, 0.25, 0.2, 0.15]
        }
        
        weights = difficulty_weights.get(self.difficulty, difficulty_weights['medium'])
        
        # Choose decision type randomly
        decision_types = [
            AIDecisionType.IDLE,
            AIDecisionType.BUILD,
            AIDecisionType.UPGRADE,
            AIDecisionType.SELL,
            AIDecisionType.TRADE
        ]
        
        decision_type = random.choices(decision_types, weights=weights)[0]
        
        # Calculate priority based on difficulty
        priority_ranges = {
            'easy': (0.3, 0.6),
            'medium': (0.5, 0.8),
            'hard': (0.7, 1.0)
        }
        
        priority_range = priority_ranges.get(self.difficulty, priority_ranges['medium'])
        priority = random.uniform(*priority_range)
        
        return AIDecision(
            decision_type=decision_type,
            priority=priority,
            data={'difficulty': self.difficulty, 'decision_num': self.decision_count}
        )
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a custom property."""
        self.properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property."""
        return self.properties.get(key, default)
    
    def force_decision(self, decision_type: AIDecisionType, **kwargs) -> AIDecision:
        """
        Force AI to make a specific type of decision.
        
        Args:
            decision_type: Type of decision to make
            **kwargs: Additional data for the decision
            
        Returns:
            AIDecision object
        """
        decision = AIDecision(
            decision_type=decision_type,
            priority=kwargs.get('priority', 1.0),
            data=kwargs
        )
        
        self.last_decision = decision
        
        if self.on_decision_hook:
            self.on_decision_hook(decision)
        
        return decision
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'player_id': self.player_id,
            'name': self.name,
            'difficulty': self.difficulty,
            'decision_interval': self.decision_interval,
            'accumulated_time': self.accumulated_time,
            'decision_count': self.decision_count,
            'properties': self.properties.copy(),
            'last_decision': {
                'type': self.last_decision.decision_type.value,
                'priority': self.last_decision.priority,
                'data': self.last_decision.data
            } if self.last_decision else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AIPlayer":
        """Deserialize from dictionary."""
        ai = cls(
            player_id=data['player_id'],
            name=data['name'],
            difficulty=data.get('difficulty', 'medium'),
            decision_interval=data.get('decision_interval', 5.0)
        )
        ai.accumulated_time = data.get('accumulated_time', 0.0)
        ai.decision_count = data.get('decision_count', 0)
        ai.properties = data.get('properties', {}).copy()
        
        # Restore last decision if present
        if data.get('last_decision'):
            last_dec = data['last_decision']
            ai.last_decision = AIDecision(
                decision_type=AIDecisionType(last_dec['type']),
                priority=last_dec['priority'],
                data=last_dec['data']
            )
        
        return ai


class AIPlayerManager:
    """
    Manages multiple AI players.
    
    Provides methods for adding, removing, and updating AI players.
    """
    
    def __init__(self, max_ai_players: int = 10):
        """
        Initialize AI player manager.
        
        Args:
            max_ai_players: Maximum number of AI players allowed
        """
        self.ai_players: Dict[str, AIPlayer] = {}
        self.max_ai_players = max_ai_players
        self._next_id = 0
    
    def add_ai_player(
        self,
        name: Optional[str] = None,
        difficulty: str = "medium",
        decision_interval: float = 5.0
    ) -> Optional[AIPlayer]:
        """
        Add a new AI player.
        
        Args:
            name: Optional name for the AI player
            difficulty: AI difficulty level
            decision_interval: Time between decisions
            
        Returns:
            AIPlayer object if successful, None if max players reached
        """
        if len(self.ai_players) >= self.max_ai_players:
            return None
        
        player_id = self.generate_id()
        if name is None:
            name = f"AI_{self._next_id}"
        
        ai_player = AIPlayer(
            player_id=player_id,
            name=name,
            difficulty=difficulty,
            decision_interval=decision_interval
        )
        
        self.ai_players[player_id] = ai_player
        return ai_player
    
    def remove_ai_player(self, player_id: str) -> bool:
        """
        Remove an AI player.
        
        Args:
            player_id: ID of the player to remove
            
        Returns:
            True if removed, False if not found
        """
        if player_id in self.ai_players:
            del self.ai_players[player_id]
            return True
        return False
    
    def get_ai_player(self, player_id: str) -> Optional[AIPlayer]:
        """Get an AI player by ID."""
        return self.ai_players.get(player_id)
    
    def get_all_ai_players(self) -> List[AIPlayer]:
        """Get all AI players."""
        return list(self.ai_players.values())
    
    def update_all(self, dt: float) -> List[tuple[str, AIDecision]]:
        """
        Update all AI players.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            List of tuples (player_id, decision) for AI players that made decisions
        """
        decisions = []
        for player_id, ai_player in self.ai_players.items():
            decision = ai_player.update(dt)
            if decision:
                decisions.append((player_id, decision))
        
        return decisions
    
    def clear(self) -> None:
        """Remove all AI players."""
        self.ai_players.clear()
    
    def generate_id(self, prefix: str = "ai") -> str:
        """Generate a unique AI player ID."""
        player_id = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return player_id
    
    def set_global_decision_hook(
        self,
        hook: Callable[[AIPlayer, AIDecision], None]
    ) -> None:
        """
        Set a decision hook for all AI players.
        
        Args:
            hook: Callback function to call when any AI makes a decision
        """
        def wrapped_hook(decision: AIDecision) -> None:
            # Find which AI made this decision
            for ai_player in self.ai_players.values():
                if ai_player.last_decision == decision:
                    hook(ai_player, decision)
                    break
        
        for ai_player in self.ai_players.values():
            ai_player.on_decision_hook = wrapped_hook
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'max_ai_players': self.max_ai_players,
            'next_id': self._next_id,
            'ai_players': {
                player_id: ai.to_dict()
                for player_id, ai in self.ai_players.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AIPlayerManager":
        """Deserialize from dictionary."""
        manager = cls(max_ai_players=data.get('max_ai_players', 10))
        manager._next_id = data.get('next_id', 0)
        
        for player_id, ai_data in data.get('ai_players', {}).items():
            ai = AIPlayer.from_dict(ai_data)
            manager.ai_players[player_id] = ai
        
        return manager
