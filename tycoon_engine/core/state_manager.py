"""
Game state management module.

Manages different game states (menu, playing, paused, etc.) and transitions between them.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import pygame


class GameState(ABC):
    """
    Abstract base class for game states.
    
    Subclasses should implement the abstract methods to define state-specific behavior.
    """
    
    def __init__(self, state_manager: "StateManager"):
        self.state_manager = state_manager
        self.config = state_manager.config
    
    @abstractmethod
    def enter(self, **kwargs) -> None:
        """Called when entering this state."""
        pass
    
    @abstractmethod
    def exit(self) -> None:
        """Called when exiting this state."""
        pass
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update state logic. dt is delta time in seconds."""
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the state to the screen."""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events."""
        pass


class StateManager:
    """
    Manages game states and transitions between them.
    
    Provides a centralized way to switch between different game states
    (e.g., menu, playing, paused, game over).
    """
    
    def __init__(self, config):
        self.config = config
        self.states: Dict[str, GameState] = {}
        self.current_state: Optional[GameState] = None
        self.current_state_name: Optional[str] = None
        self.state_data: Dict[str, Any] = {}  # Persistent data across states
    
    def add_state(self, name: str, state: GameState) -> None:
        """Register a new state."""
        self.states[name] = state
    
    def change_state(self, name: str, **kwargs) -> None:
        """
        Change to a different state.
        
        Args:
            name: Name of the state to change to
            **kwargs: Additional arguments passed to the state's enter method
        """
        if name not in self.states:
            raise ValueError(f"State '{name}' not found")
        
        # Exit current state
        if self.current_state:
            self.current_state.exit()
        
        # Enter new state
        self.current_state = self.states[name]
        self.current_state_name = name
        self.current_state.enter(**kwargs)
    
    def update(self, dt: float) -> None:
        """Update the current state."""
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the current state."""
        if self.current_state:
            self.current_state.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events in the current state."""
        if self.current_state:
            self.current_state.handle_event(event)
    
    def get_state_data(self, key: str, default: Any = None) -> Any:
        """Get persistent data that survives state transitions."""
        return self.state_data.get(key, default)
    
    def set_state_data(self, key: str, value: Any) -> None:
        """Set persistent data that survives state transitions."""
        self.state_data[key] = value
