"""
Tests for resource management.
"""

import pytest
from tycoon_engine.entities.resources import ResourceManager


def test_initial_money():
    """Test initial money setting."""
    rm = ResourceManager(starting_money=5000.0)
    assert rm.get_money() == 5000.0


def test_add_money():
    """Test adding money."""
    rm = ResourceManager(starting_money=100.0)
    rm.add_money(50.0)
    assert rm.get_money() == 150.0


def test_remove_money():
    """Test removing money."""
    rm = ResourceManager(starting_money=100.0)
    
    # Successful removal
    assert rm.remove_money(50.0) is True
    assert rm.get_money() == 50.0
    
    # Failed removal (insufficient funds)
    assert rm.remove_money(100.0) is False
    assert rm.get_money() == 50.0


def test_can_afford():
    """Test can_afford check."""
    rm = ResourceManager(starting_money=100.0)
    
    assert rm.can_afford(50.0) is True
    assert rm.can_afford(100.0) is True
    assert rm.can_afford(150.0) is False


def test_resources():
    """Test resource management."""
    rm = ResourceManager()
    
    # Add resources
    rm.add_resource("wood", 100)
    rm.add_resource("stone", 50)
    
    assert rm.get_resource("wood") == 100
    assert rm.get_resource("stone") == 50
    assert rm.get_resource("iron") == 0  # Non-existent resource
    
    # Add more
    rm.add_resource("wood", 50)
    assert rm.get_resource("wood") == 150


def test_remove_resources():
    """Test removing resources."""
    rm = ResourceManager()
    rm.add_resource("wood", 100)
    
    # Successful removal
    assert rm.remove_resource("wood", 50) is True
    assert rm.get_resource("wood") == 50
    
    # Failed removal (insufficient resources)
    assert rm.remove_resource("wood", 100) is False
    assert rm.get_resource("wood") == 50
    
    # Failed removal (non-existent resource)
    assert rm.remove_resource("stone", 10) is False


def test_has_resource():
    """Test has_resource check."""
    rm = ResourceManager()
    rm.add_resource("wood", 100)
    
    assert rm.has_resource("wood", 50) is True
    assert rm.has_resource("wood", 100) is True
    assert rm.has_resource("wood", 150) is False
    assert rm.has_resource("stone", 1) is False


def test_serialization():
    """Test resource manager serialization."""
    rm = ResourceManager(starting_money=500.0)
    rm.add_resource("wood", 100)
    rm.add_resource("stone", 50)
    
    # Serialize
    data = rm.to_dict()
    assert data["money"] == 500.0
    assert data["resources"]["wood"] == 100
    assert data["resources"]["stone"] == 50
    
    # Deserialize
    rm2 = ResourceManager.from_dict(data)
    assert rm2.get_money() == 500.0
    assert rm2.get_resource("wood") == 100
    assert rm2.get_resource("stone") == 50
