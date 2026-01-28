"""
Economy system for tycoon games.

Provides a basic resource model with income/expense tracking and configurable parameters.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Callable, Optional, List
from ..entities.resources import ResourceManager


@dataclass
class EconomyConfig:
    """
    Configuration for the economy system.
    
    This allows parameterization of economic behavior for different game types.
    """
    
    # Base rates
    base_income_rate: float = 100.0  # Money per tick
    base_expense_rate: float = 50.0  # Money per tick
    
    # Tax and interest rates
    tax_rate: float = 0.1  # 10% tax on income
    interest_rate: float = 0.05  # 5% interest per tick
    
    # Tick configuration
    tick_interval: float = 1.0  # Time between ticks in seconds
    
    # Custom parameters for game-specific economic rules
    custom_params: Dict[str, Any] = field(default_factory=dict)
    
    def get_custom_param(self, key: str, default: Any = None) -> Any:
        """Get a custom parameter with optional default value."""
        return self.custom_params.get(key, default)
    
    def set_custom_param(self, key: str, value: Any) -> None:
        """Set a custom parameter."""
        self.custom_params[key] = value


class EconomySystem:
    """
    Manages the game economy with income/expense tracking.
    
    This is a placeholder system that provides basic economic simulation
    with hooks for expansion.
    """
    
    def __init__(self, resource_manager: ResourceManager, config: Optional[EconomyConfig] = None):
        """
        Initialize the economy system.
        
        Args:
            resource_manager: The resource manager to apply economic changes to
            config: Economy configuration (uses default if not provided)
        """
        self.resource_manager = resource_manager
        self.config = config or EconomyConfig()
        
        # Track time for tick-based updates
        self._accumulated_time = 0.0
        
        # Hooks for custom income/expense calculations
        self._income_modifiers: List[Callable[[float], float]] = []
        self._expense_modifiers: List[Callable[[float], float]] = []
        
        # Statistics tracking
        self.total_income = 0.0
        self.total_expenses = 0.0
        self.tick_count = 0
    
    def update(self, dt: float) -> None:
        """
        Update the economy system.
        
        Args:
            dt: Delta time in seconds
        """
        self._accumulated_time += dt
        
        # Process economic ticks
        while self._accumulated_time >= self.config.tick_interval:
            self._accumulated_time -= self.config.tick_interval
            self._process_tick()
    
    def _process_tick(self) -> None:
        """Process a single economic tick."""
        # Calculate income
        income = self._calculate_income()
        
        # Calculate expenses
        expenses = self._calculate_expenses()
        
        # Apply to resource manager
        net_change = income - expenses
        self.resource_manager.add_money(net_change)
        
        # Update statistics
        self.total_income += income
        self.total_expenses += expenses
        self.tick_count += 1
    
    def _calculate_income(self) -> float:
        """
        Calculate income for this tick.
        
        Returns:
            Income amount after taxes and modifiers
        """
        # Start with base income
        income = self.config.base_income_rate
        
        # Apply income modifiers (e.g., from buildings, upgrades)
        for modifier in self._income_modifiers:
            income = modifier(income)
        
        # Apply tax
        income *= (1.0 - self.config.tax_rate)
        
        # Apply interest on current savings (interest_rate is per tick)
        current_money = self.resource_manager.get_money()
        interest = current_money * self.config.interest_rate
        income += interest
        
        return income
    
    def _calculate_expenses(self) -> float:
        """
        Calculate expenses for this tick.
        
        Returns:
            Expense amount after modifiers
        """
        # Start with base expenses
        expenses = self.config.base_expense_rate
        
        # Apply expense modifiers (e.g., maintenance costs)
        for modifier in self._expense_modifiers:
            expenses = modifier(expenses)
        
        return expenses
    
    def add_income_modifier(self, modifier: Callable[[float], float]) -> None:
        """
        Add a function to modify income calculation.
        
        The modifier should take the current income value and return the modified value.
        This provides a hook for game-specific income calculations.
        
        Args:
            modifier: Function that takes income float and returns modified income float
        """
        self._income_modifiers.append(modifier)
    
    def add_expense_modifier(self, modifier: Callable[[float], float]) -> None:
        """
        Add a function to modify expense calculation.
        
        The modifier should take the current expense value and return the modified value.
        This provides a hook for game-specific expense calculations.
        
        Args:
            modifier: Function that takes expense float and returns modified expense float
        """
        self._expense_modifiers.append(modifier)
    
    def remove_income_modifier(self, modifier: Callable[[float], float]) -> bool:
        """
        Remove an income modifier.
        
        Args:
            modifier: The modifier function to remove
            
        Returns:
            True if removed, False if not found
        """
        try:
            self._income_modifiers.remove(modifier)
            return True
        except ValueError:
            return False
    
    def remove_expense_modifier(self, modifier: Callable[[float], float]) -> bool:
        """
        Remove an expense modifier.
        
        Args:
            modifier: The modifier function to remove
            
        Returns:
            True if removed, False if not found
        """
        try:
            self._expense_modifiers.remove(modifier)
            return True
        except ValueError:
            return False
    
    def get_net_income_rate(self) -> float:
        """
        Get the current net income rate (income - expenses per tick).
        
        Returns:
            Net income rate
        """
        income = self._calculate_income()
        expenses = self._calculate_expenses()
        return income - expenses
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get economy statistics.
        
        Returns:
            Dictionary with economic statistics
        """
        avg_income = self.total_income / self.tick_count if self.tick_count > 0 else 0.0
        avg_expenses = self.total_expenses / self.tick_count if self.tick_count > 0 else 0.0
        
        return {
            'total_income': self.total_income,
            'total_expenses': self.total_expenses,
            'net_income': self.total_income - self.total_expenses,
            'tick_count': self.tick_count,
            'average_income_per_tick': avg_income,
            'average_expenses_per_tick': avg_expenses,
            'current_balance': self.resource_manager.get_money()
        }
    
    def reset_statistics(self) -> None:
        """Reset economy statistics."""
        self.total_income = 0.0
        self.total_expenses = 0.0
        self.tick_count = 0
