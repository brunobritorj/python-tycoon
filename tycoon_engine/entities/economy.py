"""
Economy system for tycoon games.

Provides income/expense tick mechanisms and configurable economy parameters.
"""

from typing import Dict, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class EconomyConfig:
    """
    Configuration for economy system.
    
    Defines configurable parameters for the economy tick system.
    """
    
    tick_interval: float = 1.0  # Time between ticks in seconds
    base_income_rate: float = 10.0  # Base income per tick
    base_expense_rate: float = 5.0  # Base expenses per tick
    income_modifiers: Dict[str, float] = field(default_factory=dict)  # Multipliers for income
    expense_modifiers: Dict[str, float] = field(default_factory=dict)  # Multipliers for expenses
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            'tick_interval': self.tick_interval,
            'base_income_rate': self.base_income_rate,
            'base_expense_rate': self.base_expense_rate,
            'income_modifiers': self.income_modifiers.copy(),
            'expense_modifiers': self.expense_modifiers.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "EconomyConfig":
        """Deserialize from dictionary."""
        return cls(
            tick_interval=data.get('tick_interval', 1.0),
            base_income_rate=data.get('base_income_rate', 10.0),
            base_expense_rate=data.get('base_expense_rate', 5.0),
            income_modifiers=data.get('income_modifiers', {}).copy(),
            expense_modifiers=data.get('expense_modifiers', {}).copy()
        )


class EconomySystem:
    """
    Economy system with income/expense tick mechanism.
    
    Handles periodic income and expenses for game economy.
    """
    
    def __init__(self, config: Optional[EconomyConfig] = None):
        """
        Initialize economy system.
        
        Args:
            config: Economy configuration, uses default if None
        """
        self.config = config or EconomyConfig()
        self.accumulated_time = 0.0
        self.total_income = 0.0
        self.total_expenses = 0.0
        self.tick_count = 0
        
        # Callbacks for custom behavior
        self.on_income_tick: Optional[Callable[[float], None]] = None
        self.on_expense_tick: Optional[Callable[[float], None]] = None
        self.on_tick: Optional[Callable[[int, float, float], None]] = None
    
    def update(self, dt: float) -> tuple[float, float]:
        """
        Update economy system.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            Tuple of (income, expenses) for this update, or (0, 0) if no tick occurred
        """
        self.accumulated_time += dt
        
        if self.accumulated_time >= self.config.tick_interval:
            self.accumulated_time -= self.config.tick_interval
            return self._process_tick()
        
        return (0.0, 0.0)
    
    def _process_tick(self) -> tuple[float, float]:
        """
        Process an economy tick.
        
        Returns:
            Tuple of (income, expenses) for this tick
        """
        self.tick_count += 1
        
        # Calculate income with modifiers
        income = self.config.base_income_rate
        for modifier_value in self.config.income_modifiers.values():
            income *= modifier_value
        
        # Calculate expenses with modifiers
        expenses = self.config.base_expense_rate
        for modifier_value in self.config.expense_modifiers.values():
            expenses *= modifier_value
        
        # Track totals
        self.total_income += income
        self.total_expenses += expenses
        
        # Trigger callbacks
        if self.on_income_tick:
            self.on_income_tick(income)
        
        if self.on_expense_tick:
            self.on_expense_tick(expenses)
        
        if self.on_tick:
            self.on_tick(self.tick_count, income, expenses)
        
        return (income, expenses)
    
    def get_net_income_per_tick(self) -> float:
        """
        Calculate net income per tick (income - expenses).
        
        Returns:
            Net income per tick
        """
        income = self.config.base_income_rate
        for modifier_value in self.config.income_modifiers.values():
            income *= modifier_value
        
        expenses = self.config.base_expense_rate
        for modifier_value in self.config.expense_modifiers.values():
            expenses *= modifier_value
        
        return income - expenses
    
    def add_income_modifier(self, name: str, multiplier: float) -> None:
        """
        Add or update an income modifier.
        
        Args:
            name: Name of the modifier
            multiplier: Multiplier value (e.g., 1.5 for 50% increase)
        """
        self.config.income_modifiers[name] = multiplier
    
    def add_expense_modifier(self, name: str, multiplier: float) -> None:
        """
        Add or update an expense modifier.
        
        Args:
            name: Name of the modifier
            multiplier: Multiplier value (e.g., 0.8 for 20% reduction)
        """
        self.config.expense_modifiers[name] = multiplier
    
    def remove_income_modifier(self, name: str) -> bool:
        """
        Remove an income modifier.
        
        Args:
            name: Name of the modifier
            
        Returns:
            True if removed, False if not found
        """
        if name in self.config.income_modifiers:
            del self.config.income_modifiers[name]
            return True
        return False
    
    def remove_expense_modifier(self, name: str) -> bool:
        """
        Remove an expense modifier.
        
        Args:
            name: Name of the modifier
            
        Returns:
            True if removed, False if not found
        """
        if name in self.config.expense_modifiers:
            del self.config.expense_modifiers[name]
            return True
        return False
    
    def reset_tick_count(self) -> None:
        """Reset tick counter and totals."""
        self.tick_count = 0
        self.total_income = 0.0
        self.total_expenses = 0.0
        self.accumulated_time = 0.0
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            'config': self.config.to_dict(),
            'accumulated_time': self.accumulated_time,
            'total_income': self.total_income,
            'total_expenses': self.total_expenses,
            'tick_count': self.tick_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "EconomySystem":
        """Deserialize from dictionary."""
        config = EconomyConfig.from_dict(data.get('config', {}))
        system = cls(config)
        system.accumulated_time = data.get('accumulated_time', 0.0)
        system.total_income = data.get('total_income', 0.0)
        system.total_expenses = data.get('total_expenses', 0.0)
        system.tick_count = data.get('tick_count', 0)
        return system
