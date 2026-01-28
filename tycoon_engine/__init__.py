"""
Tycoon Engine - A modular 2D Tycoon/Management game engine.

This package provides the core functionality for building tycoon-style games
with pygame rendering and multiplayer support via python-socketio.
"""

__version__ = "0.1.0"
__author__ = "Python Tycoon Contributors"

from tycoon_engine.core.game import Game
from tycoon_engine.core.state_manager import StateManager
from tycoon_engine.core.config import GameConfig

__all__ = ["Game", "StateManager", "GameConfig"]
