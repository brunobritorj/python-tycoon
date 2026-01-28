"""
Tycoon Engine - A modular 2D Tycoon/Management game engine.

This package provides the core functionality for building tycoon-style games
with pygame rendering and multiplayer support via python-socketio.
"""

from tycoon_engine.version import __version__, __version_info__

__author__ = "Python Tycoon Contributors"

from tycoon_engine.core.game import Game
from tycoon_engine.core.state_manager import StateManager
from tycoon_engine.core.config import GameConfig

__all__ = ["Game", "StateManager", "GameConfig", "__version__", "__version_info__"]
