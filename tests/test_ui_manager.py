"""
Tests for UI manager module.
"""

import pytest
import pygame
from tycoon_engine.ui.ui_manager import UIManager
from tycoon_engine.ui.components import UIComponent, Button, Label


@pytest.fixture(autouse=True)
def init_pygame():
    """Initialize pygame for all tests."""
    pygame.init()
    yield


@pytest.fixture
def ui_manager():
    """Create a UI manager for testing."""
    return UIManager()


@pytest.fixture
def screen():
    """Create a test screen surface."""
    return pygame.display.set_mode((800, 600))


def test_ui_manager_creation(ui_manager):
    """Test UI manager creation."""
    assert ui_manager is not None
    assert len(ui_manager.components) == 0
    assert ui_manager.focused_component is None


def test_add_component(ui_manager):
    """Test adding components."""
    component = Label("Test", 0, 0)
    ui_manager.add_component(component)
    
    assert len(ui_manager.components) == 1
    assert component in ui_manager.components


def test_remove_component(ui_manager):
    """Test removing components."""
    component = Label("Test", 0, 0)
    ui_manager.add_component(component)
    ui_manager.remove_component(component)
    
    assert len(ui_manager.components) == 0
    assert component not in ui_manager.components


def test_clear_all(ui_manager):
    """Test clearing all components."""
    ui_manager.add_component(Label("Test1", 0, 0))
    ui_manager.add_component(Label("Test2", 0, 10))
    
    ui_manager.clear_all()
    
    assert len(ui_manager.components) == 0
    assert ui_manager.focused_component is None


def test_update(ui_manager):
    """Test updating components."""
    component = UIComponent(0, 0, 100, 100)
    update_called = {'value': False}
    
    original_update = component.update
    def mock_update(dt):
        update_called['value'] = True
        original_update(dt)
    
    component.update = mock_update
    ui_manager.add_component(component)
    
    ui_manager.update(0.016)
    assert update_called['value'] is True


def test_render(ui_manager, screen):
    """Test rendering components."""
    component = UIComponent(0, 0, 100, 100)
    render_called = {'value': False}
    
    original_render = component.render
    def mock_render(surface):
        render_called['value'] = True
        original_render(surface)
    
    component.render = mock_render
    ui_manager.add_component(component)
    
    ui_manager.render(screen)
    assert render_called['value'] is True


def test_handle_event(ui_manager):
    """Test event handling."""
    called = {'value': False}
    
    def callback():
        called['value'] = True
    
    button = Button("Click", 100, 100, 100, 50, callback=callback)
    ui_manager.add_component(button)
    
    # Mock mouse position
    pygame.mouse.get_pos = lambda: (150, 125)
    
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(150, 125))
    handled = ui_manager.handle_event(event)
    
    assert handled is True
    assert called['value'] is True


def test_event_order_top_to_bottom(ui_manager):
    """Test that events are handled from top to bottom."""
    call_order = []
    
    def callback1():
        call_order.append(1)
    
    def callback2():
        call_order.append(2)
    
    # Add two overlapping buttons
    button1 = Button("First", 100, 100, 100, 50, callback=callback1)
    button2 = Button("Second", 100, 100, 100, 50, callback=callback2)
    
    ui_manager.add_component(button1)
    ui_manager.add_component(button2)  # Added last, should be on top
    
    # Mock mouse position
    pygame.mouse.get_pos = lambda: (150, 125)
    
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(150, 125))
    ui_manager.handle_event(event)
    
    # Only the top button should handle the event
    assert call_order == [2]


def test_focus_management(ui_manager):
    """Test focus management."""
    component1 = Label("Test1", 0, 0)
    component2 = Label("Test2", 0, 10)
    
    ui_manager.add_component(component1)
    ui_manager.add_component(component2)
    
    # Set focus
    ui_manager.set_focus(component1)
    assert ui_manager.get_focused_component() == component1
    
    # Change focus
    ui_manager.set_focus(component2)
    assert ui_manager.get_focused_component() == component2
    
    # Clear focus
    ui_manager.clear_focus()
    assert ui_manager.get_focused_component() is None


def test_get_component_at(ui_manager):
    """Test getting component at position."""
    component = Label("Test", 100, 100)
    component.rect = pygame.Rect(100, 100, 100, 50)
    ui_manager.add_component(component)
    
    # Inside component
    found = ui_manager.get_component_at(150, 125)
    assert found == component
    
    # Outside component
    found = ui_manager.get_component_at(10, 10)
    assert found is None


def test_bring_to_front(ui_manager):
    """Test bringing component to front."""
    component1 = Label("First", 0, 0)
    component2 = Label("Second", 0, 10)
    
    ui_manager.add_component(component1)
    ui_manager.add_component(component2)
    
    # Bring first to front
    ui_manager.bring_to_front(component1)
    
    # component1 should now be last in list (on top)
    assert ui_manager.components[-1] == component1


def test_send_to_back(ui_manager):
    """Test sending component to back."""
    component1 = Label("First", 0, 0)
    component2 = Label("Second", 0, 10)
    
    ui_manager.add_component(component1)
    ui_manager.add_component(component2)
    
    # Send second to back
    ui_manager.send_to_back(component2)
    
    # component2 should now be first in list (at back)
    assert ui_manager.components[0] == component2


def test_show_hide_all(ui_manager):
    """Test showing and hiding all components."""
    component1 = Label("Test1", 0, 0)
    component2 = Label("Test2", 0, 10)
    
    ui_manager.add_component(component1)
    ui_manager.add_component(component2)
    
    # Hide all
    ui_manager.hide_all()
    assert not component1.visible
    assert not component2.visible
    
    # Show all
    ui_manager.show_all()
    assert component1.visible
    assert component2.visible


def test_enable_disable_all(ui_manager):
    """Test enabling and disabling all components."""
    component1 = Label("Test1", 0, 0)
    component2 = Label("Test2", 0, 10)
    
    ui_manager.add_component(component1)
    ui_manager.add_component(component2)
    
    # Disable all
    ui_manager.disable_all()
    assert not component1.enabled
    assert not component2.enabled
    
    # Enable all
    ui_manager.enable_all()
    assert component1.enabled
    assert component2.enabled


def test_count(ui_manager):
    """Test component count."""
    assert ui_manager.count() == 0
    
    ui_manager.add_component(Label("Test1", 0, 0))
    assert ui_manager.count() == 1
    
    ui_manager.add_component(Label("Test2", 0, 10))
    assert ui_manager.count() == 2


def test_get_components(ui_manager):
    """Test getting components list."""
    component1 = Label("Test1", 0, 0)
    component2 = Label("Test2", 0, 10)
    
    ui_manager.add_component(component1)
    ui_manager.add_component(component2)
    
    components = ui_manager.get_components()
    assert len(components) == 2
    assert component1 in components
    assert component2 in components
    
    # Should return a copy
    components.clear()
    assert ui_manager.count() == 2
