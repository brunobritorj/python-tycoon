"""
Tests for utility functions.
"""

import pytest
from tycoon_engine.utils.helpers import Timer, clamp, lerp, distance


def test_timer_creation():
    """Test timer creation."""
    callback_called = []
    
    def callback():
        callback_called.append(True)
    
    timer = Timer(1.0, callback, repeat=False)
    assert timer.interval == 1.0
    assert timer.repeat is False
    assert timer.active is True


def test_timer_validation():
    """Test timer interval validation."""
    def callback():
        pass
    
    # Should raise ValueError for non-positive intervals
    with pytest.raises(ValueError):
        Timer(0.0, callback)
    
    with pytest.raises(ValueError):
        Timer(-1.0, callback)


def test_timer_callback():
    """Test timer callback execution."""
    callback_called = []
    
    def callback():
        callback_called.append(True)
    
    timer = Timer(0.5, callback, repeat=False)
    
    # Update but don't reach interval
    timer.update(0.3)
    assert len(callback_called) == 0
    
    # Reach interval
    timer.update(0.2)
    assert len(callback_called) == 1
    assert timer.active is False  # Non-repeating timer should stop


def test_timer_repeat():
    """Test repeating timer."""
    callback_count = []
    
    def callback():
        callback_count.append(True)
    
    timer = Timer(0.5, callback, repeat=True)
    
    # First trigger
    timer.update(0.5)
    assert len(callback_count) == 1
    assert timer.active is True
    
    # Second trigger (should preserve timing accuracy)
    timer.update(0.5)
    assert len(callback_count) == 2
    assert timer.active is True


def test_timer_timing_accuracy():
    """Test timer timing accuracy with lag."""
    callback_count = []
    
    def callback():
        callback_count.append(True)
    
    timer = Timer(0.5, callback, repeat=True)
    
    # Large update that exceeds interval
    timer.update(1.2)
    assert len(callback_count) == 1
    # Elapsed should be 0.7 (1.2 - 0.5), preserving excess time
    assert abs(timer.elapsed - 0.7) < 0.01


def test_timer_reset():
    """Test timer reset."""
    callback_called = []
    
    def callback():
        callback_called.append(True)
    
    timer = Timer(1.0, callback)
    timer.update(0.5)
    timer.reset()
    
    assert timer.elapsed == 0.0
    assert timer.active is True


def test_timer_stop():
    """Test timer stop."""
    callback_called = []
    
    def callback():
        callback_called.append(True)
    
    timer = Timer(1.0, callback)
    timer.stop()
    
    # Update shouldn't trigger callback
    timer.update(2.0)
    assert len(callback_called) == 0


def test_clamp():
    """Test clamp function."""
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10


def test_lerp():
    """Test linear interpolation."""
    assert lerp(0, 10, 0.0) == 0
    assert lerp(0, 10, 1.0) == 10
    assert lerp(0, 10, 0.5) == 5
    assert lerp(10, 20, 0.5) == 15


def test_distance():
    """Test distance calculation."""
    assert distance(0, 0, 3, 4) == 5.0
    assert distance(0, 0, 0, 0) == 0.0
    assert abs(distance(1, 1, 2, 2) - 1.414213) < 0.001
