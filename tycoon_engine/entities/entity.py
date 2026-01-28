"""
Base entity class for game objects.

Provides a foundation for all game entities in tycoon games.
"""

from typing import Tuple, Dict, Any, Optional
import pygame


class Entity:
    """
    Base class for all game entities.
    
    Entities represent game objects like buildings, resources, workers, etc.
    """
    
    def __init__(self, entity_id: str, entity_type: str, x: float, y: float):
        """
        Initialize an entity.
        
        Args:
            entity_id: Unique identifier for this entity
            entity_type: Type classification (e.g., 'building', 'worker', 'resource')
            x: X position in game world
            y: Y position in game world
        """
        self.id = entity_id
        self.type = entity_type
        self.x = x
        self.y = y
        self.active = True
        self.properties: Dict[str, Any] = {}
    
    def update(self, dt: float) -> None:
        """
        Update entity logic.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    def render(self, screen: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)) -> None:
        """
        Render the entity to screen.
        
        Args:
            screen: Pygame surface to render to
            camera_offset: Camera offset (x, y) for scrolling
        """
        pass
    
    def get_position(self) -> Tuple[float, float]:
        """Get entity position."""
        return (self.x, self.y)
    
    def set_position(self, x: float, y: float) -> None:
        """Set entity position."""
        self.x = x
        self.y = y
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property."""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a custom property."""
        self.properties[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize entity to dictionary (for networking)."""
        return {
            'id': self.id,
            'type': self.type,
            'x': self.x,
            'y': self.y,
            'active': self.active,
            'properties': self.properties
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        """Deserialize entity from dictionary."""
        entity = cls(
            entity_id=data['id'],
            entity_type=data['type'],
            x=data['x'],
            y=data['y']
        )
        entity.active = data.get('active', True)
        entity.properties = data.get('properties', {})
        return entity


class EntityManager:
    """
    Manages all entities in the game.
    
    Provides methods for adding, removing, and querying entities.
    """
    
    def __init__(self, max_entities: int = 1000):
        """
        Initialize entity manager.
        
        Args:
            max_entities: Maximum number of entities allowed
        """
        self.entities: Dict[str, Entity] = {}
        self.max_entities = max_entities
        self._next_id = 0
    
    def add_entity(self, entity: Entity) -> bool:
        """
        Add an entity to the manager.
        
        Returns:
            True if added successfully, False if max entities reached
        """
        if len(self.entities) >= self.max_entities:
            return False
        
        self.entities[entity.id] = entity
        return True
    
    def remove_entity(self, entity_id: str) -> bool:
        """
        Remove an entity by ID.
        
        Returns:
            True if removed, False if not found
        """
        if entity_id in self.entities:
            del self.entities[entity_id]
            return True
        return False
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID."""
        return self.entities.get(entity_id)
    
    def get_entities_by_type(self, entity_type: str) -> list:
        """Get all entities of a specific type."""
        return [e for e in self.entities.values() if e.type == entity_type]
    
    def get_all_entities(self) -> list:
        """Get all entities."""
        return list(self.entities.values())
    
    def update_all(self, dt: float) -> None:
        """Update all active entities."""
        for entity in self.entities.values():
            if entity.active:
                entity.update(dt)
    
    def render_all(self, screen: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)) -> None:
        """Render all active entities."""
        for entity in self.entities.values():
            if entity.active:
                entity.render(screen, camera_offset)
    
    def clear(self) -> None:
        """Remove all entities."""
        self.entities.clear()
    
    def generate_id(self, prefix: str = "entity") -> str:
        """Generate a unique entity ID."""
        entity_id = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return entity_id
