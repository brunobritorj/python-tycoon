"""
Tests for configuration module.
"""

import pytest
import json
import tempfile
from pathlib import Path
from tycoon_engine.core.config import GameConfig


def test_default_config():
    """Test default configuration values."""
    config = GameConfig()
    assert config.game_title == "Tycoon Game"
    assert config.screen_width == 1280
    assert config.screen_height == 720
    assert config.fps == 60
    assert config.starting_money == 10000.0


def test_custom_config():
    """Test custom configuration values."""
    config = GameConfig(
        game_title="Test Game",
        screen_width=800,
        starting_money=5000.0
    )
    assert config.game_title == "Test Game"
    assert config.screen_width == 800
    assert config.starting_money == 5000.0


def test_resolution():
    """Test resolution getter."""
    config = GameConfig(screen_width=1920, screen_height=1080)
    assert config.get_resolution() == (1920, 1080)


def test_custom_params():
    """Test custom parameters."""
    config = GameConfig()
    
    config.set_custom_param("difficulty", "hard")
    assert config.get_custom_param("difficulty") == "hard"
    
    # Test default value
    assert config.get_custom_param("nonexistent", "default") == "default"


def test_json_serialization():
    """Test JSON save/load."""
    config = GameConfig(
        game_title="JSON Test",
        starting_money=7500.0
    )
    config.set_custom_param("test_key", "test_value")
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        config.to_json(temp_path)
        
        # Load back
        loaded_config = GameConfig.from_json(temp_path)
        assert loaded_config.game_title == "JSON Test"
        assert loaded_config.starting_money == 7500.0
        assert loaded_config.get_custom_param("test_key") == "test_value"
    finally:
        Path(temp_path).unlink()
