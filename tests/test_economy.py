"""
Tests for economy system.
"""

import pytest
from tycoon_engine.entities.economy import EconomyConfig, EconomySystem


def test_economy_config_default():
    """Test default economy configuration."""
    config = EconomyConfig()
    assert config.tick_interval == 1.0
    assert config.base_income_rate == 10.0
    assert config.base_expense_rate == 5.0
    assert len(config.income_modifiers) == 0
    assert len(config.expense_modifiers) == 0


def test_economy_config_custom():
    """Test custom economy configuration."""
    config = EconomyConfig(
        tick_interval=2.0,
        base_income_rate=100.0,
        base_expense_rate=50.0,
        income_modifiers={'bonus': 1.5},
        expense_modifiers={'discount': 0.8}
    )
    assert config.tick_interval == 2.0
    assert config.base_income_rate == 100.0
    assert config.base_expense_rate == 50.0
    assert config.income_modifiers['bonus'] == 1.5
    assert config.expense_modifiers['discount'] == 0.8


def test_economy_config_serialization():
    """Test economy config serialization."""
    config = EconomyConfig(
        tick_interval=1.5,
        base_income_rate=50.0,
        base_expense_rate=25.0,
        income_modifiers={'bonus': 1.2},
        expense_modifiers={'tax': 1.1}
    )
    
    # Serialize
    data = config.to_dict()
    assert data['tick_interval'] == 1.5
    assert data['base_income_rate'] == 50.0
    assert data['base_expense_rate'] == 25.0
    
    # Deserialize
    config2 = EconomyConfig.from_dict(data)
    assert config2.tick_interval == 1.5
    assert config2.base_income_rate == 50.0
    assert config2.base_expense_rate == 25.0
    assert config2.income_modifiers['bonus'] == 1.2
    assert config2.expense_modifiers['tax'] == 1.1


def test_economy_system_creation():
    """Test economy system creation."""
    system = EconomySystem()
    assert system.config is not None
    assert system.tick_count == 0
    assert system.total_income == 0.0
    assert system.total_expenses == 0.0


def test_economy_system_no_tick():
    """Test economy system with time less than tick interval."""
    system = EconomySystem(EconomyConfig(tick_interval=2.0))
    
    income, expenses = system.update(1.0)
    
    assert income == 0.0
    assert expenses == 0.0
    assert system.tick_count == 0


def test_economy_system_single_tick():
    """Test economy system with one tick."""
    config = EconomyConfig(
        tick_interval=1.0,
        base_income_rate=100.0,
        base_expense_rate=30.0
    )
    system = EconomySystem(config)
    
    income, expenses = system.update(1.0)
    
    assert income == 100.0
    assert expenses == 30.0
    assert system.tick_count == 1
    assert system.total_income == 100.0
    assert system.total_expenses == 30.0


def test_economy_system_multiple_ticks():
    """Test economy system with multiple ticks."""
    config = EconomyConfig(
        tick_interval=1.0,
        base_income_rate=50.0,
        base_expense_rate=20.0
    )
    system = EconomySystem(config)
    
    # First tick
    income1, expenses1 = system.update(1.0)
    assert income1 == 50.0
    assert expenses1 == 20.0
    assert system.tick_count == 1
    
    # Second tick
    income2, expenses2 = system.update(1.0)
    assert income2 == 50.0
    assert expenses2 == 20.0
    assert system.tick_count == 2
    
    # Verify totals
    assert system.total_income == 100.0
    assert system.total_expenses == 40.0


def test_economy_system_accumulated_time():
    """Test accumulated time handling."""
    config = EconomyConfig(tick_interval=2.0)
    system = EconomySystem(config)
    
    # Not enough time for a tick
    income, expenses = system.update(1.0)
    assert income == 0.0
    assert expenses == 0.0
    assert system.tick_count == 0
    
    # Now enough time for a tick
    income, expenses = system.update(1.5)
    assert income == 10.0  # base income rate
    assert expenses == 5.0  # base expense rate
    assert system.tick_count == 1
    assert system.accumulated_time == 0.5  # 1.0 + 1.5 - 2.0


def test_economy_system_income_modifiers():
    """Test income modifiers."""
    config = EconomyConfig(
        tick_interval=1.0,
        base_income_rate=100.0,
        base_expense_rate=0.0
    )
    system = EconomySystem(config)
    
    # Add modifiers
    system.add_income_modifier('bonus', 1.5)  # 50% increase
    system.add_income_modifier('special', 2.0)  # 100% increase
    
    income, expenses = system.update(1.0)
    
    # 100 * 1.5 * 2.0 = 300
    assert income == 300.0
    assert expenses == 0.0


def test_economy_system_expense_modifiers():
    """Test expense modifiers."""
    config = EconomyConfig(
        tick_interval=1.0,
        base_income_rate=0.0,
        base_expense_rate=100.0
    )
    system = EconomySystem(config)
    
    # Add modifiers
    system.add_expense_modifier('discount', 0.8)  # 20% reduction
    system.add_expense_modifier('efficiency', 0.5)  # 50% reduction
    
    income, expenses = system.update(1.0)
    
    # 100 * 0.8 * 0.5 = 40
    assert income == 0.0
    assert expenses == 40.0


def test_economy_system_net_income():
    """Test net income calculation."""
    config = EconomyConfig(
        tick_interval=1.0,
        base_income_rate=100.0,
        base_expense_rate=30.0
    )
    system = EconomySystem(config)
    
    net = system.get_net_income_per_tick()
    assert net == 70.0
    
    # Add modifiers
    system.add_income_modifier('bonus', 2.0)
    system.add_expense_modifier('tax', 1.5)
    
    net = system.get_net_income_per_tick()
    # (100 * 2.0) - (30 * 1.5) = 200 - 45 = 155
    assert net == 155.0


def test_economy_system_remove_modifiers():
    """Test removing modifiers."""
    system = EconomySystem()
    
    # Add modifiers
    system.add_income_modifier('bonus', 1.5)
    system.add_expense_modifier('tax', 1.2)
    
    # Remove modifiers
    assert system.remove_income_modifier('bonus') is True
    assert system.remove_income_modifier('nonexistent') is False
    
    assert system.remove_expense_modifier('tax') is True
    assert system.remove_expense_modifier('nonexistent') is False


def test_economy_system_reset():
    """Test resetting economy system."""
    system = EconomySystem()
    
    # Do some ticks
    system.update(1.0)
    system.update(1.0)
    
    assert system.tick_count == 2
    assert system.total_income > 0
    assert system.total_expenses > 0
    
    # Reset
    system.reset_tick_count()
    
    assert system.tick_count == 0
    assert system.total_income == 0.0
    assert system.total_expenses == 0.0
    assert system.accumulated_time == 0.0


def test_economy_system_callbacks():
    """Test economy system callbacks."""
    system = EconomySystem()
    
    income_values = []
    expense_values = []
    tick_values = []
    
    def on_income(income):
        income_values.append(income)
    
    def on_expense(expense):
        expense_values.append(expense)
    
    def on_tick(tick, income, expense):
        tick_values.append((tick, income, expense))
    
    system.on_income_tick = on_income
    system.on_expense_tick = on_expense
    system.on_tick = on_tick
    
    # Trigger a tick
    system.update(1.0)
    
    assert len(income_values) == 1
    assert income_values[0] == 10.0
    
    assert len(expense_values) == 1
    assert expense_values[0] == 5.0
    
    assert len(tick_values) == 1
    assert tick_values[0] == (1, 10.0, 5.0)


def test_economy_system_serialization():
    """Test economy system serialization."""
    config = EconomyConfig(
        tick_interval=1.5,
        base_income_rate=75.0,
        base_expense_rate=25.0
    )
    system = EconomySystem(config)
    
    # Do some updates
    system.update(1.0)
    system.update(1.0)
    
    # Serialize
    data = system.to_dict()
    assert data['tick_count'] == 1
    assert data['total_income'] == 75.0
    assert data['total_expenses'] == 25.0
    
    # Deserialize
    system2 = EconomySystem.from_dict(data)
    assert system2.tick_count == 1
    assert system2.total_income == 75.0
    assert system2.total_expenses == 25.0
    assert system2.config.tick_interval == 1.5
    assert system2.config.base_income_rate == 75.0
