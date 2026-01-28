"""
Tests for AI player system.
"""

import pytest
from tycoon_engine.entities.resources import ResourceManager
from tycoon_engine.systems.ai_player import AIPlayer, AIPlayerManager, AIPlayerState


def test_ai_player_initialization():
    """Test AI player initialization."""
    ai = AIPlayer("ai_1", "AI Player 1", difficulty="medium")
    
    assert ai.id == "ai_1"
    assert ai.name == "AI Player 1"
    assert ai.difficulty == "medium"
    assert ai.state == AIPlayerState.IDLE
    assert ai.actions_taken == 0
    assert ai.decisions_made == 0


def test_ai_player_with_resource_manager():
    """Test AI player with custom resource manager."""
    rm = ResourceManager(starting_money=5000.0)
    ai = AIPlayer("ai_1", "AI Player", resource_manager=rm)
    
    assert ai.resource_manager == rm
    assert ai.resource_manager.get_money() == 5000.0


def test_ai_player_decision_interval():
    """Test decision interval based on difficulty."""
    ai_easy = AIPlayer("ai_1", "Easy AI", difficulty="easy")
    ai_medium = AIPlayer("ai_2", "Medium AI", difficulty="medium")
    ai_hard = AIPlayer("ai_3", "Hard AI", difficulty="hard")
    
    assert ai_easy._decision_interval == 5.0
    assert ai_medium._decision_interval == 3.0
    assert ai_hard._decision_interval == 1.5


def test_ai_player_update_triggers_decision():
    """Test that update triggers decision making."""
    ai = AIPlayer("ai_1", "AI Player", difficulty="medium")
    
    # Update for less than decision interval
    ai.update(1.0)
    assert ai.decisions_made == 0
    
    # Update to exceed decision interval (3.0 seconds for medium)
    ai.update(2.5)
    assert ai.decisions_made == 1


def test_ai_player_decision_hook():
    """Test adding and calling decision hooks."""
    ai = AIPlayer("ai_1", "AI Player", difficulty="medium")
    
    hook_called = []
    
    def test_hook(game_state):
        hook_called.append(True)
        return {'type': 'test_action', 'cost': 0}
    
    ai.add_decision_hook(test_hook)
    
    # Trigger decision
    ai.update(3.0)
    
    assert len(hook_called) == 1
    assert ai.decisions_made == 1


def test_ai_player_action_queue():
    """Test action queueing from decision hooks."""
    ai = AIPlayer("ai_1", "AI Player", difficulty="medium")
    
    def hook_that_returns_action(game_state):
        return {'type': 'build', 'cost': 100}
    
    ai.add_decision_hook(hook_that_returns_action)
    
    # Trigger decision
    ai.update(3.0)
    
    # Action should have been executed (and money deducted)
    assert ai.actions_taken == 1
    assert ai.resource_manager.get_money() == 9900.0


def test_ai_player_manual_queue_action():
    """Test manually queueing an action."""
    ai = AIPlayer("ai_1", "AI Player")
    
    action = {'type': 'upgrade', 'cost': 50}
    ai.queue_action(action)
    
    stats = ai.get_statistics()
    assert stats['queued_actions'] == 1


def test_ai_player_clear_action_queue():
    """Test clearing the action queue."""
    ai = AIPlayer("ai_1", "AI Player")
    
    ai.queue_action({'type': 'action1', 'cost': 0})
    ai.queue_action({'type': 'action2', 'cost': 0})
    
    ai.clear_action_queue()
    
    stats = ai.get_statistics()
    assert stats['queued_actions'] == 0


def test_ai_player_action_execution_with_cost():
    """Test action execution with cost."""
    rm = ResourceManager(starting_money=1000.0)
    ai = AIPlayer("ai_1", "AI Player", resource_manager=rm)
    
    # Queue an affordable action
    ai.queue_action({'type': 'build', 'cost': 100})
    
    # Execute actions
    ai.update(0.1)
    
    # Money should be deducted
    assert rm.get_money() == 900.0
    assert ai.actions_taken == 1


def test_ai_player_action_execution_insufficient_funds():
    """Test action execution with insufficient funds."""
    rm = ResourceManager(starting_money=50.0)
    ai = AIPlayer("ai_1", "AI Player", resource_manager=rm)
    
    # Queue an unaffordable action
    ai.queue_action({'type': 'expensive', 'cost': 100})
    
    # Try to execute
    ai.update(0.1)
    
    # Action should not execute
    assert rm.get_money() == 50.0
    assert ai.actions_taken == 0


def test_ai_player_remove_decision_hook():
    """Test removing decision hooks."""
    ai = AIPlayer("ai_1", "AI Player")
    
    def hook(game_state):
        return None
    
    ai.add_decision_hook(hook)
    assert ai.remove_decision_hook(hook) is True
    assert ai.remove_decision_hook(hook) is False


def test_ai_player_statistics():
    """Test AI player statistics."""
    rm = ResourceManager(starting_money=1000.0)
    ai = AIPlayer("ai_1", "Test AI", resource_manager=rm, difficulty="hard")
    
    stats = ai.get_statistics()
    
    assert stats['id'] == "ai_1"
    assert stats['name'] == "Test AI"
    assert stats['difficulty'] == "hard"
    assert stats['state'] == AIPlayerState.IDLE.value
    assert stats['actions_taken'] == 0
    assert stats['decisions_made'] == 0
    assert stats['money'] == 1000.0


def test_ai_player_manager_add_player():
    """Test adding AI players to manager."""
    manager = AIPlayerManager()
    ai1 = AIPlayer("ai_1", "AI 1")
    ai2 = AIPlayer("ai_2", "AI 2")
    
    assert manager.add_ai_player(ai1) is True
    assert manager.add_ai_player(ai2) is True
    
    # Try to add duplicate
    assert manager.add_ai_player(ai1) is False


def test_ai_player_manager_remove_player():
    """Test removing AI players from manager."""
    manager = AIPlayerManager()
    ai = AIPlayer("ai_1", "AI 1")
    
    manager.add_ai_player(ai)
    assert manager.remove_ai_player("ai_1") is True
    assert manager.remove_ai_player("ai_1") is False


def test_ai_player_manager_get_player():
    """Test getting AI player by ID."""
    manager = AIPlayerManager()
    ai = AIPlayer("ai_1", "AI 1")
    
    manager.add_ai_player(ai)
    
    retrieved = manager.get_ai_player("ai_1")
    assert retrieved == ai
    
    assert manager.get_ai_player("nonexistent") is None


def test_ai_player_manager_get_all():
    """Test getting all AI players."""
    manager = AIPlayerManager()
    ai1 = AIPlayer("ai_1", "AI 1")
    ai2 = AIPlayer("ai_2", "AI 2")
    
    manager.add_ai_player(ai1)
    manager.add_ai_player(ai2)
    
    all_players = manager.get_all_ai_players()
    assert len(all_players) == 2
    assert ai1 in all_players
    assert ai2 in all_players


def test_ai_player_manager_update_all():
    """Test updating all AI players."""
    manager = AIPlayerManager()
    
    ai1 = AIPlayer("ai_1", "AI 1", difficulty="easy")  # 5 second interval
    ai2 = AIPlayer("ai_2", "AI 2", difficulty="easy")
    
    manager.add_ai_player(ai1)
    manager.add_ai_player(ai2)
    
    # Update all for 5 seconds (should trigger decisions)
    manager.update_all(5.0)
    
    assert ai1.decisions_made == 1
    assert ai2.decisions_made == 1


def test_ai_player_manager_statistics():
    """Test manager statistics aggregation."""
    manager = AIPlayerManager()
    
    ai1 = AIPlayer("ai_1", "AI 1")
    ai2 = AIPlayer("ai_2", "AI 2")
    
    # Manually set some statistics
    ai1.actions_taken = 5
    ai1.decisions_made = 3
    ai2.actions_taken = 3
    ai2.decisions_made = 2
    
    manager.add_ai_player(ai1)
    manager.add_ai_player(ai2)
    
    stats = manager.get_statistics()
    
    assert stats['total_ai_players'] == 2
    assert stats['total_actions_taken'] == 8
    assert stats['total_decisions_made'] == 5
    assert 'players' in stats
    assert 'ai_1' in stats['players']
    assert 'ai_2' in stats['players']


def test_ai_player_manager_clear():
    """Test clearing all AI players."""
    manager = AIPlayerManager()
    
    manager.add_ai_player(AIPlayer("ai_1", "AI 1"))
    manager.add_ai_player(AIPlayer("ai_2", "AI 2"))
    
    manager.clear()
    
    assert len(manager.get_all_ai_players()) == 0


def test_ai_player_state_transitions():
    """Test AI player state transitions."""
    ai = AIPlayer("ai_1", "AI Player", difficulty="medium")
    
    assert ai.state == AIPlayerState.IDLE
    
    # Add a hook that returns an action
    def hook(game_state):
        return {'type': 'test', 'cost': 0}
    
    ai.add_decision_hook(hook)
    
    # Trigger decision (actions are executed in the same update call)
    ai.update(3.0)
    
    # After actions are executed, state should be IDLE
    assert ai.state == AIPlayerState.IDLE
    assert ai.decisions_made == 1
    assert ai.actions_taken == 1
