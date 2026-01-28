"""
Tests for economy system.
"""

import pytest
from tycoon_engine.entities.resources import ResourceManager
from tycoon_engine.systems.economy import EconomySystem, EconomyConfig


def test_economy_config_defaults():
    """Test economy config with default values."""
    config = EconomyConfig()
    assert config.base_income_rate == 100.0
    assert config.base_expense_rate == 50.0
    assert config.tax_rate == 0.1
    assert config.interest_rate == 0.05
    assert config.tick_interval == 1.0


def test_economy_config_custom_params():
    """Test economy config custom parameters."""
    config = EconomyConfig()
    config.set_custom_param("difficulty", "hard")
    assert config.get_custom_param("difficulty") == "hard"
    assert config.get_custom_param("nonexistent", "default") == "default"


def test_economy_system_initialization():
    """Test economy system initialization."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig()
    economy = EconomySystem(rm, config)
    
    assert economy.resource_manager == rm
    assert economy.config == config
    assert economy.total_income == 0.0
    assert economy.total_expenses == 0.0
    assert economy.tick_count == 0


def test_economy_system_tick():
    """Test economy system tick processing."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=100.0,
        base_expense_rate=50.0,
        tax_rate=0.0,  # No tax for simple test
        interest_rate=0.0,  # No interest for simple test
        tick_interval=1.0
    )
    economy = EconomySystem(rm, config)
    
    initial_money = rm.get_money()
    
    # Update for 1 second (should process 1 tick)
    economy.update(1.0)
    
    assert economy.tick_count == 1
    # Net income should be 100 - 50 = 50
    assert rm.get_money() == initial_money + 50.0


def test_economy_system_multiple_ticks():
    """Test economy system processing multiple ticks."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=100.0,
        base_expense_rate=50.0,
        tax_rate=0.0,
        interest_rate=0.0,
        tick_interval=0.5  # 2 ticks per second
    )
    economy = EconomySystem(rm, config)
    
    # Update for 1 second (should process 2 ticks)
    economy.update(1.0)
    
    assert economy.tick_count == 2
    assert rm.get_money() == 1000.0 + (50.0 * 2)  # 2 ticks of 50 net income


def test_economy_system_partial_tick():
    """Test economy system with partial tick accumulation."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(tick_interval=1.0)
    economy = EconomySystem(rm, config)
    
    # Update for 0.5 seconds (not enough for a tick)
    economy.update(0.5)
    assert economy.tick_count == 0
    
    # Update for another 0.5 seconds (should complete 1 tick)
    economy.update(0.5)
    assert economy.tick_count == 1


def test_economy_system_tax():
    """Test tax calculation."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=100.0,
        base_expense_rate=0.0,
        tax_rate=0.2,  # 20% tax
        interest_rate=0.0,
        tick_interval=1.0
    )
    economy = EconomySystem(rm, config)
    
    economy.update(1.0)
    
    # Income after 20% tax: 100 * 0.8 = 80
    assert rm.get_money() == 1000.0 + 80.0


def test_economy_system_interest():
    """Test interest calculation."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=0.0,
        base_expense_rate=0.0,
        tax_rate=0.0,
        interest_rate=0.1,  # 10% interest per tick
        tick_interval=1.0
    )
    economy = EconomySystem(rm, config)
    
    economy.update(1.0)
    
    # Interest: 1000 * 0.1 * 1.0 = 100
    assert rm.get_money() == 1000.0 + 100.0


def test_economy_system_income_modifier():
    """Test income modifier functionality."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=100.0,
        base_expense_rate=0.0,
        tax_rate=0.0,
        interest_rate=0.0,
        tick_interval=1.0
    )
    economy = EconomySystem(rm, config)
    
    # Add modifier that doubles income
    def double_income(income):
        return income * 2.0
    
    economy.add_income_modifier(double_income)
    economy.update(1.0)
    
    # Income should be doubled: 100 * 2 = 200
    assert rm.get_money() == 1000.0 + 200.0


def test_economy_system_expense_modifier():
    """Test expense modifier functionality."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=100.0,
        base_expense_rate=50.0,
        tax_rate=0.0,
        interest_rate=0.0,
        tick_interval=1.0
    )
    economy = EconomySystem(rm, config)
    
    # Add modifier that doubles expenses
    def double_expenses(expenses):
        return expenses * 2.0
    
    economy.add_expense_modifier(double_expenses)
    economy.update(1.0)
    
    # Net income: 100 - (50 * 2) = 0
    assert rm.get_money() == 1000.0


def test_economy_system_remove_modifiers():
    """Test removing modifiers."""
    rm = ResourceManager(starting_money=1000.0)
    economy = EconomySystem(rm)
    
    def modifier(value):
        return value * 2.0
    
    # Add and remove income modifier
    economy.add_income_modifier(modifier)
    assert economy.remove_income_modifier(modifier) is True
    assert economy.remove_income_modifier(modifier) is False
    
    # Add and remove expense modifier
    economy.add_expense_modifier(modifier)
    assert economy.remove_expense_modifier(modifier) is True
    assert economy.remove_expense_modifier(modifier) is False


def test_economy_system_net_income_rate():
    """Test net income rate calculation."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=100.0,
        base_expense_rate=50.0,
        tax_rate=0.0,
        interest_rate=0.0
    )
    economy = EconomySystem(rm, config)
    
    net_rate = economy.get_net_income_rate()
    assert net_rate == 50.0  # 100 - 50


def test_economy_system_statistics():
    """Test economy statistics tracking."""
    rm = ResourceManager(starting_money=1000.0)
    config = EconomyConfig(
        base_income_rate=100.0,
        base_expense_rate=50.0,
        tax_rate=0.0,
        interest_rate=0.0,
        tick_interval=1.0
    )
    economy = EconomySystem(rm, config)
    
    # Process 3 ticks
    economy.update(3.0)
    
    stats = economy.get_statistics()
    assert stats['tick_count'] == 3
    assert stats['total_income'] == 300.0
    assert stats['total_expenses'] == 150.0
    assert stats['net_income'] == 150.0
    assert stats['average_income_per_tick'] == 100.0
    assert stats['average_expenses_per_tick'] == 50.0
    assert stats['current_balance'] == 1150.0


def test_economy_system_reset_statistics():
    """Test resetting economy statistics."""
    rm = ResourceManager(starting_money=1000.0)
    economy = EconomySystem(rm)
    
    economy.update(2.0)
    
    assert economy.tick_count > 0
    
    economy.reset_statistics()
    
    assert economy.total_income == 0.0
    assert economy.total_expenses == 0.0
    assert economy.tick_count == 0


def test_economy_system_negative_balance():
    """Test economy system with expenses exceeding income."""
    rm = ResourceManager(starting_money=100.0)
    config = EconomyConfig(
        base_income_rate=10.0,
        base_expense_rate=50.0,
        tax_rate=0.0,
        interest_rate=0.0,
        tick_interval=1.0
    )
    economy = EconomySystem(rm, config)
    
    economy.update(1.0)
    
    # Net income: 10 - 50 = -40
    assert rm.get_money() == 60.0
    
    economy.update(1.0)
    assert rm.get_money() == 20.0
