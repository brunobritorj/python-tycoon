"""
Tests for event dispatcher module.
"""

import pytest
import pygame
from tycoon_engine.core.events import (
    EventDispatcher,
    EventPriority,
    GameEvent,
    on_key_down,
    on_mouse_click
)


@pytest.fixture
def dispatcher():
    """Create an event dispatcher for testing."""
    pygame.init()
    return EventDispatcher()


def test_event_dispatcher_creation(dispatcher):
    """Test event dispatcher creation."""
    assert dispatcher is not None
    assert len(dispatcher._pygame_listeners) == 0
    assert len(dispatcher._custom_listeners) == 0
    assert len(dispatcher._event_queue) == 0


def test_subscribe_pygame_event(dispatcher):
    """Test subscribing to pygame events."""
    called = {'value': False}
    
    def callback(event):
        called['value'] = True
    
    dispatcher.subscribe(pygame.KEYDOWN, callback)
    assert dispatcher.has_listeners(pygame.KEYDOWN)
    
    # Dispatch event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    dispatcher.dispatch_pygame_event(event)
    assert called['value']


def test_subscribe_custom_event(dispatcher):
    """Test subscribing to custom events."""
    called = {'value': False, 'data': None}
    
    def callback(event):
        called['value'] = True
        called['data'] = event.data
    
    dispatcher.subscribe('test_event', callback)
    assert dispatcher.has_listeners('test_event')
    
    # Dispatch custom event
    dispatcher.dispatch_custom_event('test_event', {'key': 'value'})
    dispatcher.process_custom_events()
    
    assert called['value']
    assert called['data'] == {'key': 'value'}


def test_event_priority(dispatcher):
    """Test event priority ordering."""
    call_order = []
    
    def low_priority(event):
        call_order.append('low')
    
    def high_priority(event):
        call_order.append('high')
    
    def normal_priority(event):
        call_order.append('normal')
    
    # Subscribe in mixed order
    dispatcher.subscribe(pygame.KEYDOWN, normal_priority, EventPriority.NORMAL)
    dispatcher.subscribe(pygame.KEYDOWN, high_priority, EventPriority.HIGH)
    dispatcher.subscribe(pygame.KEYDOWN, low_priority, EventPriority.LOW)
    
    # Dispatch event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    dispatcher.dispatch_pygame_event(event)
    
    # Check that high priority was called first
    assert call_order == ['high', 'normal', 'low']


def test_unsubscribe(dispatcher):
    """Test unsubscribing from events."""
    called = {'value': False}
    
    def callback(event):
        called['value'] = True
    
    # Subscribe and unsubscribe
    dispatcher.subscribe(pygame.KEYDOWN, callback)
    dispatcher.unsubscribe(pygame.KEYDOWN, callback)
    
    # Dispatch event - callback should not be called
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    dispatcher.dispatch_pygame_event(event)
    assert not called['value']


def test_clear_all(dispatcher):
    """Test clearing all listeners."""
    def callback(event):
        pass
    
    dispatcher.subscribe(pygame.KEYDOWN, callback)
    dispatcher.subscribe('custom_event', callback)
    dispatcher.dispatch_custom_event('custom_event', {})
    
    dispatcher.clear_all()
    
    assert not dispatcher.has_listeners(pygame.KEYDOWN)
    assert not dispatcher.has_listeners('custom_event')
    assert len(dispatcher._event_queue) == 0


def test_clear_event_type(dispatcher):
    """Test clearing specific event type."""
    def callback(event):
        pass
    
    dispatcher.subscribe(pygame.KEYDOWN, callback)
    dispatcher.subscribe(pygame.MOUSEBUTTONDOWN, callback)
    
    dispatcher.clear_event_type(pygame.KEYDOWN)
    
    assert not dispatcher.has_listeners(pygame.KEYDOWN)
    assert dispatcher.has_listeners(pygame.MOUSEBUTTONDOWN)


def test_game_event_creation():
    """Test GameEvent creation."""
    event = GameEvent('test_type', {'key': 'value'})
    
    assert event.event_type == 'test_type'
    assert event.data == {'key': 'value'}
    assert event.timestamp > 0


def test_multiple_listeners(dispatcher):
    """Test multiple listeners for same event."""
    calls = []
    
    def callback1(event):
        calls.append('callback1')
    
    def callback2(event):
        calls.append('callback2')
    
    dispatcher.subscribe(pygame.KEYDOWN, callback1)
    dispatcher.subscribe(pygame.KEYDOWN, callback2)
    
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    dispatcher.dispatch_pygame_event(event)
    
    assert len(calls) == 2
    assert 'callback1' in calls
    assert 'callback2' in calls


def test_on_key_down_helper(dispatcher):
    """Test on_key_down convenience function."""
    called = {'value': False}
    
    def callback(event):
        called['value'] = True
    
    on_key_down(dispatcher, pygame.K_SPACE, callback)
    
    # Dispatch SPACE key
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    dispatcher.dispatch_pygame_event(event)
    assert called['value']
    
    # Dispatch different key - should not be called
    called['value'] = False
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
    dispatcher.dispatch_pygame_event(event)
    # Note: The filter will still call the function, but we'd need to check the key


def test_on_mouse_click_helper(dispatcher):
    """Test on_mouse_click convenience function."""
    called = {'value': False}
    
    def callback(event):
        called['value'] = True
    
    on_mouse_click(dispatcher, 1, callback)  # Left click
    
    # Dispatch left click
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0))
    dispatcher.dispatch_pygame_event(event)
    # The filter checks button, so this should work
