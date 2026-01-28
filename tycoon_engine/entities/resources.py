"""
Resource management system for tycoon games.

Handles money, resources, and other game economy elements.
"""

from typing import Dict, Optional


class ResourceManager:
    """
    Manages game resources like money, materials, etc.
    
    Provides a flexible system for tracking and managing different resource types.
    """
    
    def __init__(self, starting_money: float = 10000.0):
        """
        Initialize resource manager.
        
        Args:
            starting_money: Initial amount of money
        """
        self.money = starting_money
        self.resources: Dict[str, float] = {}
    
    def add_money(self, amount: float) -> None:
        """Add money to the player's balance."""
        self.money += amount
    
    def remove_money(self, amount: float) -> bool:
        """
        Remove money from the player's balance.
        
        Returns:
            True if successful, False if insufficient funds
        """
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def get_money(self) -> float:
        """Get current money balance."""
        return self.money
    
    def set_money(self, amount: float) -> None:
        """Set money to a specific amount."""
        self.money = max(0, amount)
    
    def can_afford(self, amount: float) -> bool:
        """Check if player can afford a certain amount."""
        return self.money >= amount
    
    def add_resource(self, resource_type: str, amount: float) -> None:
        """Add a resource."""
        if resource_type not in self.resources:
            self.resources[resource_type] = 0
        self.resources[resource_type] += amount
    
    def remove_resource(self, resource_type: str, amount: float) -> bool:
        """
        Remove a resource.
        
        Returns:
            True if successful, False if insufficient resources
        """
        if resource_type not in self.resources:
            return False
        
        if self.resources[resource_type] >= amount:
            self.resources[resource_type] -= amount
            return True
        return False
    
    def get_resource(self, resource_type: str) -> float:
        """Get amount of a specific resource."""
        return self.resources.get(resource_type, 0)
    
    def set_resource(self, resource_type: str, amount: float) -> None:
        """Set a resource to a specific amount."""
        self.resources[resource_type] = max(0, amount)
    
    def has_resource(self, resource_type: str, amount: float) -> bool:
        """Check if player has enough of a resource."""
        return self.get_resource(resource_type) >= amount
    
    def get_all_resources(self) -> Dict[str, float]:
        """Get all resources as a dictionary."""
        return self.resources.copy()
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary (for saving/networking)."""
        return {
            'money': self.money,
            'resources': self.resources.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "ResourceManager":
        """Deserialize from dictionary."""
        rm = cls(starting_money=data.get('money', 0))
        rm.resources = data.get('resources', {}).copy()
        return rm
