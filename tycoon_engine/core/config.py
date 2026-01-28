"""
Game configuration module.

Provides a parameterized configuration system for building different tycoon games
on top of the same foundation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Tuple, Optional
import json


@dataclass
class GameConfig:
    """
    Configuration class for tycoon games.
    
    This class allows different tycoon games to be built on the same foundation
    by parameterizing game-specific settings.
    """
    
    # Game identity
    game_title: str = "Tycoon Game"
    game_version: str = "0.1.0"
    
    # Display settings
    screen_width: int = 1280
    screen_height: int = 720
    fps: int = 60
    fullscreen: bool = False
    
    # Multiplayer settings
    enable_multiplayer: bool = False
    server_host: str = "localhost"
    server_port: int = 5000
    
    # Game-specific settings (can be extended by subclasses)
    starting_money: float = 10000.0
    tick_rate: float = 1.0  # Game ticks per second
    max_entities: int = 1000
    
    # Custom game parameters (flexible dictionary for game-specific data)
    custom_params: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_json(cls, json_path: str) -> "GameConfig":
        """Load configuration from a JSON file."""
        with open(json_path, 'r') as f:
            data = json.load(f)
        return cls(**data)
    
    def to_json(self, json_path: str) -> None:
        """Save configuration to a JSON file."""
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
    
    def get_resolution(self) -> Tuple[int, int]:
        """Get screen resolution as tuple."""
        return (self.screen_width, self.screen_height)
    
    def get_custom_param(self, key: str, default: Any = None) -> Any:
        """Get a custom parameter with optional default value."""
        return self.custom_params.get(key, default)
    
    def set_custom_param(self, key: str, value: Any) -> None:
        """Set a custom parameter."""
        self.custom_params[key] = value
