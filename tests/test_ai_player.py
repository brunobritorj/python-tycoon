"""
Tests for AI player system.
"""

import pytest
from tycoon_engine.entities.ai_player import (
    AIPlayer, AIPlayerManager, AIDecision, AIDecisionType
)


def test_ai_player_creation():
    """Test AI player creation."""
    ai = AIPlayer(player_id="ai_1", name="Test AI", difficulty="medium")
    assert ai.player_id == "ai_1"
    assert ai.name == "Test AI"
    assert ai.difficulty == "medium"
    assert ai.decision_count == 0


def test_ai_player_difficulties():
    """Test different AI difficulty levels."""
    easy_ai = AIPlayer(player_id="easy", name="Easy", difficulty="easy")
    medium_ai = AIPlayer(player_id="medium", name="Medium", difficulty="medium")
    hard_ai = AIPlayer(player_id="hard", name="Hard", difficulty="hard")
    
    assert easy_ai.difficulty == "easy"
    assert medium_ai.difficulty == "medium"
    assert hard_ai.difficulty == "hard"


def test_ai_player_no_decision_before_interval():
    """Test that AI doesn't make decision before interval."""
    ai = AIPlayer(player_id="ai_1", name="Test", decision_interval=5.0)
    
    decision = ai.update(2.0)
    assert decision is None
    assert ai.decision_count == 0


def test_ai_player_decision_after_interval():
    """Test that AI makes decision after interval."""
    ai = AIPlayer(player_id="ai_1", name="Test", decision_interval=1.0)
    
    decision = ai.update(1.0)
    assert decision is not None
    assert isinstance(decision, AIDecision)
    assert ai.decision_count == 1
    assert ai.last_decision == decision


def test_ai_player_multiple_decisions():
    """Test multiple decisions over time."""
    ai = AIPlayer(player_id="ai_1", name="Test", decision_interval=1.0)
    
    # First decision
    decision1 = ai.update(1.0)
    assert decision1 is not None
    assert ai.decision_count == 1
    
    # Second decision
    decision2 = ai.update(1.0)
    assert decision2 is not None
    assert ai.decision_count == 2


def test_ai_player_accumulated_time():
    """Test accumulated time handling."""
    ai = AIPlayer(player_id="ai_1", name="Test", decision_interval=2.0)
    
    # Not enough time
    decision = ai.update(1.0)
    assert decision is None
    
    # Now enough time
    decision = ai.update(1.5)
    assert decision is not None
    assert ai.decision_count == 1
    assert ai.accumulated_time == 0.5  # 1.0 + 1.5 - 2.0


def test_ai_decision_types():
    """Test that AI can make different decision types."""
    ai = AIPlayer(player_id="ai_1", name="Test", decision_interval=0.1)
    
    decision_types = set()
    for _ in range(20):  # Run multiple times to get variety
        decision = ai.update(0.1)
        if decision:
            decision_types.add(decision.decision_type)
    
    # Should have at least 2 different decision types
    assert len(decision_types) >= 2


def test_ai_player_properties():
    """Test AI player custom properties."""
    ai = AIPlayer(player_id="ai_1", name="Test")
    
    ai.set_property("money", 1000)
    ai.set_property("buildings", 5)
    
    assert ai.get_property("money") == 1000
    assert ai.get_property("buildings") == 5
    assert ai.get_property("nonexistent", "default") == "default"


def test_ai_player_force_decision():
    """Test forcing a specific decision."""
    ai = AIPlayer(player_id="ai_1", name="Test")
    
    decision = ai.force_decision(AIDecisionType.BUILD, priority=0.9, target="factory")
    
    assert decision.decision_type == AIDecisionType.BUILD
    assert decision.priority == 0.9
    assert decision.data["target"] == "factory"
    assert ai.last_decision == decision


def test_ai_player_decision_hook():
    """Test decision callback hook."""
    ai = AIPlayer(player_id="ai_1", name="Test", decision_interval=1.0)
    
    decisions = []
    
    def on_decision(decision):
        decisions.append(decision)
    
    ai.on_decision_hook = on_decision
    
    # Trigger decision
    ai.update(1.0)
    
    assert len(decisions) == 1
    assert isinstance(decisions[0], AIDecision)


def test_ai_player_custom_decision_maker():
    """Test custom decision maker hook."""
    ai = AIPlayer(player_id="ai_1", name="Test", decision_interval=1.0)
    
    def custom_decision_maker(ai_player):
        return AIDecision(
            decision_type=AIDecisionType.CUSTOM,
            priority=1.0,
            data={"custom": True}
        )
    
    ai.decision_maker_hook = custom_decision_maker
    
    decision = ai.update(1.0)
    
    assert decision.decision_type == AIDecisionType.CUSTOM
    assert decision.data["custom"] is True


def test_ai_player_serialization():
    """Test AI player serialization."""
    ai = AIPlayer(
        player_id="ai_1",
        name="Test AI",
        difficulty="hard",
        decision_interval=2.0
    )
    ai.set_property("money", 500)
    ai.update(2.0)  # Make a decision
    
    # Serialize
    data = ai.to_dict()
    assert data['player_id'] == "ai_1"
    assert data['name'] == "Test AI"
    assert data['difficulty'] == "hard"
    assert data['decision_count'] == 1
    
    # Deserialize
    ai2 = AIPlayer.from_dict(data)
    assert ai2.player_id == "ai_1"
    assert ai2.name == "Test AI"
    assert ai2.difficulty == "hard"
    assert ai2.decision_count == 1
    assert ai2.get_property("money") == 500


def test_ai_player_manager_creation():
    """Test AI player manager creation."""
    manager = AIPlayerManager(max_ai_players=5)
    assert manager.max_ai_players == 5
    assert len(manager.ai_players) == 0


def test_ai_player_manager_add_player():
    """Test adding AI players."""
    manager = AIPlayerManager()
    
    ai1 = manager.add_ai_player(name="AI 1", difficulty="easy")
    assert ai1 is not None
    assert ai1.name == "AI 1"
    assert len(manager.ai_players) == 1
    
    ai2 = manager.add_ai_player(name="AI 2", difficulty="hard")
    assert ai2 is not None
    assert len(manager.ai_players) == 2


def test_ai_player_manager_max_players():
    """Test max AI players limit."""
    manager = AIPlayerManager(max_ai_players=2)
    
    ai1 = manager.add_ai_player()
    ai2 = manager.add_ai_player()
    ai3 = manager.add_ai_player()
    
    assert ai1 is not None
    assert ai2 is not None
    assert ai3 is None  # Should fail due to max limit
    assert len(manager.ai_players) == 2


def test_ai_player_manager_remove_player():
    """Test removing AI players."""
    manager = AIPlayerManager()
    
    ai = manager.add_ai_player()
    player_id = ai.player_id
    
    assert manager.remove_ai_player(player_id) is True
    assert manager.remove_ai_player(player_id) is False  # Already removed
    assert len(manager.ai_players) == 0


def test_ai_player_manager_get_player():
    """Test getting AI players."""
    manager = AIPlayerManager()
    
    ai = manager.add_ai_player(name="Test AI")
    
    retrieved = manager.get_ai_player(ai.player_id)
    assert retrieved == ai
    assert retrieved.name == "Test AI"
    
    assert manager.get_ai_player("nonexistent") is None


def test_ai_player_manager_get_all():
    """Test getting all AI players."""
    manager = AIPlayerManager()
    
    ai1 = manager.add_ai_player(name="AI 1")
    ai2 = manager.add_ai_player(name="AI 2")
    ai3 = manager.add_ai_player(name="AI 3")
    
    all_ais = manager.get_all_ai_players()
    assert len(all_ais) == 3
    assert ai1 in all_ais
    assert ai2 in all_ais
    assert ai3 in all_ais


def test_ai_player_manager_update_all():
    """Test updating all AI players."""
    manager = AIPlayerManager()
    
    ai1 = manager.add_ai_player(decision_interval=1.0)
    ai2 = manager.add_ai_player(decision_interval=1.0)
    
    # Update with enough time for decisions
    decisions = manager.update_all(1.0)
    
    assert len(decisions) == 2
    for player_id, decision in decisions:
        assert isinstance(decision, AIDecision)


def test_ai_player_manager_update_partial():
    """Test updating when only some AIs make decisions."""
    manager = AIPlayerManager()
    
    ai1 = manager.add_ai_player(decision_interval=0.5)
    ai2 = manager.add_ai_player(decision_interval=2.0)
    
    # Only ai1 should make a decision
    decisions = manager.update_all(0.5)
    
    assert len(decisions) == 1
    assert decisions[0][0] == ai1.player_id


def test_ai_player_manager_clear():
    """Test clearing all AI players."""
    manager = AIPlayerManager()
    
    manager.add_ai_player()
    manager.add_ai_player()
    manager.add_ai_player()
    
    assert len(manager.ai_players) == 3
    
    manager.clear()
    assert len(manager.ai_players) == 0


def test_ai_player_manager_generate_id():
    """Test ID generation."""
    manager = AIPlayerManager()
    
    id1 = manager.generate_id()
    id2 = manager.generate_id()
    
    assert id1 != id2
    assert id1.startswith("ai_")
    assert id2.startswith("ai_")


def test_ai_player_manager_serialization():
    """Test AI player manager serialization."""
    manager = AIPlayerManager(max_ai_players=5)
    
    ai1 = manager.add_ai_player(name="AI 1", difficulty="easy")
    ai2 = manager.add_ai_player(name="AI 2", difficulty="hard")
    
    # Serialize
    data = manager.to_dict()
    assert data['max_ai_players'] == 5
    assert len(data['ai_players']) == 2
    
    # Deserialize
    manager2 = AIPlayerManager.from_dict(data)
    assert manager2.max_ai_players == 5
    assert len(manager2.ai_players) == 2
    
    all_ais = manager2.get_all_ai_players()
    names = [ai.name for ai in all_ais]
    assert "AI 1" in names
    assert "AI 2" in names


def test_ai_decision_enum():
    """Test AI decision type enum."""
    assert AIDecisionType.IDLE.value == "idle"
    assert AIDecisionType.BUILD.value == "build"
    assert AIDecisionType.UPGRADE.value == "upgrade"
    assert AIDecisionType.SELL.value == "sell"
    assert AIDecisionType.TRADE.value == "trade"
    assert AIDecisionType.CUSTOM.value == "custom"
