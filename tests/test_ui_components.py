"""
Tests for UI components module.
"""

import pytest
import pygame
from tycoon_engine.ui.components import (
    UIComponent,
    Label,
    Button,
    Panel,
    ProgressBar,
    TextInput,
    Alignment
)


@pytest.fixture(autouse=True)
def init_pygame():
    """Initialize pygame for all tests."""
    pygame.init()
    yield
    # No explicit cleanup needed


@pytest.fixture
def screen():
    """Create a test screen surface."""
    return pygame.display.set_mode((800, 600))


def test_ui_component_creation():
    """Test base UI component creation."""
    component = UIComponent(10, 20, 100, 50)
    
    assert component.rect.x == 10
    assert component.rect.y == 20
    assert component.rect.width == 100
    assert component.rect.height == 50
    assert component.visible is True
    assert component.enabled is True


def test_label_creation():
    """Test label creation."""
    label = Label("Test", 10, 20, font_size=24)
    
    assert label.text == "Test"
    assert label.rect.x == 10
    assert label.rect.y == 20
    assert label.font_size == 24
    assert label.visible is True


def test_label_set_text():
    """Test updating label text."""
    label = Label("Initial", 0, 0)
    label.set_text("Updated")
    
    assert label.text == "Updated"


def test_label_set_color():
    """Test updating label color."""
    label = Label("Test", 0, 0, color=(255, 255, 255))
    label.set_color((255, 0, 0))
    
    assert label.color == (255, 0, 0)


def test_label_alignment():
    """Test label alignment."""
    label_left = Label("Test", 100, 0, alignment=Alignment.LEFT)
    label_center = Label("Test", 100, 0, alignment=Alignment.CENTER)
    label_right = Label("Test", 100, 0, alignment=Alignment.RIGHT)
    
    assert label_left.alignment == Alignment.LEFT
    assert label_center.alignment == Alignment.CENTER
    assert label_right.alignment == Alignment.RIGHT


def test_button_creation():
    """Test button creation."""
    called = {'value': False}
    
    def callback():
        called['value'] = True
    
    button = Button("Click", 10, 20, 100, 50, callback=callback)
    
    assert button.text == "Click"
    assert button.callback is callback
    assert button.rect.width == 100
    assert button.rect.height == 50


def test_button_click(screen):
    """Test button click detection."""
    called = {'value': False}
    
    def callback():
        called['value'] = True
    
    button = Button("Click", 100, 100, 100, 50, callback=callback)
    
    # Simulate click event at button position
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(150, 125)  # Inside button
    )
    
    # Mock mouse position
    pygame.mouse.get_pos = lambda: (150, 125)
    
    handled = button.handle_event(event)
    assert handled is True
    assert called['value'] is True


def test_button_set_text():
    """Test updating button text."""
    button = Button("Initial", 0, 0, 100, 50)
    button.set_text("Updated")
    
    assert button.text == "Updated"


def test_panel_creation():
    """Test panel creation."""
    panel = Panel(10, 20, 200, 150)
    
    assert panel.rect.x == 10
    assert panel.rect.y == 20
    assert panel.rect.width == 200
    assert panel.rect.height == 150
    assert len(panel.children) == 0


def test_panel_children():
    """Test panel child management."""
    panel = Panel(0, 0, 200, 200)
    child = Label("Child", 10, 10)
    
    panel.add_child(child)
    assert len(panel.children) == 1
    assert child in panel.children
    
    panel.remove_child(child)
    assert len(panel.children) == 0
    assert child not in panel.children


def test_progress_bar_creation():
    """Test progress bar creation."""
    bar = ProgressBar(10, 20, 200, 30, progress=0.5)
    
    assert bar.rect.x == 10
    assert bar.rect.y == 20
    assert bar.rect.width == 200
    assert bar.rect.height == 30
    assert bar.progress == 0.5


def test_progress_bar_set_progress():
    """Test setting progress bar value."""
    bar = ProgressBar(0, 0, 100, 20)
    
    bar.set_progress(0.75)
    assert bar.progress == 0.75
    
    # Test clamping
    bar.set_progress(1.5)
    assert bar.progress == 1.0
    
    bar.set_progress(-0.5)
    assert bar.progress == 0.0


def test_text_input_creation():
    """Test text input creation."""
    text_input = TextInput(10, 20, 200, 40, initial_text="test")
    
    assert text_input.text == "test"
    assert text_input.rect.width == 200
    assert text_input.rect.height == 40
    assert text_input.active is False


def test_text_input_get_set_text():
    """Test text input get/set."""
    text_input = TextInput(0, 0, 100, 30)
    
    text_input.set_text("Hello")
    assert text_input.get_text() == "Hello"


def test_text_input_max_length():
    """Test text input max length."""
    text_input = TextInput(0, 0, 100, 30, max_length=5)
    
    text_input.set_text("Hello World")
    assert len(text_input.get_text()) == 5
    assert text_input.get_text() == "Hello"


def test_text_input_backspace():
    """Test text input backspace handling."""
    text_input = TextInput(0, 0, 100, 30, initial_text="Hello")
    text_input.active = True
    
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode='')
    text_input.handle_event(event)
    
    assert text_input.get_text() == "Hell"


def test_text_input_activation(screen):
    """Test text input activation on click."""
    text_input = TextInput(100, 100, 200, 40)
    
    # Mock mouse position inside input
    pygame.mouse.get_pos = lambda: (150, 120)
    
    # Click event
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(150, 120))
    handled = text_input.handle_event(event)
    
    assert handled is True
    assert text_input.active is True


def test_component_visibility():
    """Test component visibility."""
    component = UIComponent(0, 0, 100, 100)
    
    assert component.visible is True
    component.visible = False
    assert component.visible is False


def test_component_enabled():
    """Test component enabled state."""
    component = UIComponent(0, 0, 100, 100)
    
    assert component.enabled is True
    component.enabled = False
    assert component.enabled is False


def test_component_is_hovered():
    """Test component hover detection."""
    component = UIComponent(100, 100, 100, 100)
    
    # Mock mouse inside component
    pygame.mouse.get_pos = lambda: (150, 150)
    assert component.is_hovered() is True
    
    # Mock mouse outside component
    pygame.mouse.get_pos = lambda: (10, 10)
    assert component.is_hovered() is False
    
    # Disabled component should not be hovered
    pygame.mouse.get_pos = lambda: (150, 150)
    component.enabled = False
    assert component.is_hovered() is False
