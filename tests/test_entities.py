"""
Tests for entity system.
"""

import pytest
from tycoon_engine.entities.entity import Entity, EntityManager


def test_entity_creation():
    """Test entity creation."""
    entity = Entity("test_1", "test_type", 100.0, 200.0)
    assert entity.id == "test_1"
    assert entity.type == "test_type"
    assert entity.x == 100.0
    assert entity.y == 200.0
    assert entity.active is True


def test_entity_properties():
    """Test entity properties."""
    entity = Entity("test_1", "test_type", 0, 0)
    
    entity.set_property("health", 100)
    assert entity.get_property("health") == 100
    
    # Test default value
    assert entity.get_property("nonexistent", 0) == 0


def test_entity_serialization():
    """Test entity serialization."""
    entity = Entity("test_1", "building", 50.0, 100.0)
    entity.set_property("level", 2)
    
    # Serialize
    data = entity.to_dict()
    assert data["id"] == "test_1"
    assert data["type"] == "building"
    assert data["x"] == 50.0
    assert data["y"] == 100.0
    assert data["properties"]["level"] == 2
    
    # Deserialize
    entity2 = Entity.from_dict(data)
    assert entity2.id == entity.id
    assert entity2.type == entity.type
    assert entity2.x == entity.x
    assert entity2.y == entity.y
    assert entity2.get_property("level") == 2


def test_entity_manager():
    """Test entity manager."""
    manager = EntityManager(max_entities=10)
    
    # Add entities
    entity1 = Entity("e1", "type_a", 0, 0)
    entity2 = Entity("e2", "type_b", 10, 10)
    
    assert manager.add_entity(entity1) is True
    assert manager.add_entity(entity2) is True
    
    # Get entities
    assert manager.get_entity("e1") == entity1
    assert manager.get_entity("e2") == entity2
    
    # Get by type
    type_a_entities = manager.get_entities_by_type("type_a")
    assert len(type_a_entities) == 1
    assert type_a_entities[0] == entity1
    
    # Remove entity
    assert manager.remove_entity("e1") is True
    assert manager.get_entity("e1") is None


def test_entity_manager_max_entities():
    """Test entity manager max entities limit."""
    manager = EntityManager(max_entities=2)
    
    entity1 = Entity("e1", "type_a", 0, 0)
    entity2 = Entity("e2", "type_a", 0, 0)
    entity3 = Entity("e3", "type_a", 0, 0)
    
    assert manager.add_entity(entity1) is True
    assert manager.add_entity(entity2) is True
    assert manager.add_entity(entity3) is False  # Should fail


def test_entity_manager_generate_id():
    """Test ID generation."""
    manager = EntityManager()
    
    id1 = manager.generate_id("player")
    id2 = manager.generate_id("player")
    id3 = manager.generate_id("enemy")
    
    assert id1 == "player_0"
    assert id2 == "player_1"
    assert id3 == "enemy_2"
