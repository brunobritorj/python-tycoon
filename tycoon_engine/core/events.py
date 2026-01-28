"""
Event dispatcher module.

Provides a flexible event system for handling keyboard, mouse, and custom game events.
"""

import pygame
from typing import Callable, Dict, List, Any, Optional
from collections import defaultdict
from enum import IntEnum


class EventPriority(IntEnum):
    """Priority levels for event handling."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class GameEvent:
    """
    Custom game event class.
    
    Used for game-specific events beyond standard pygame events.
    """
    
    def __init__(self, event_type: str, data: Optional[Dict[str, Any]] = None):
        """
        Initialize a game event.
        
        Args:
            event_type: String identifier for the event type
            data: Optional dictionary containing event data
        """
        self.event_type = event_type
        self.data = data or {}
        self.timestamp = pygame.time.get_ticks()
    
    def __repr__(self) -> str:
        return f"GameEvent(type={self.event_type}, data={self.data}, timestamp={self.timestamp})"


class EventListener:
    """Represents a listener for events with callback and priority."""
    
    def __init__(self, callback: Callable, priority: EventPriority = EventPriority.NORMAL):
        """
        Initialize an event listener.
        
        Args:
            callback: Function to call when event occurs
            priority: Priority level for this listener
        """
        self.callback = callback
        self.priority = priority
    
    def __call__(self, event: Any) -> None:
        """Execute the callback with the event."""
        self.callback(event)


class EventDispatcher:
    """
    Event dispatcher for handling pygame and custom game events.
    
    Provides an event system with:
    - Event listener registration/unregistration
    - Priority-based event handling
    - Support for pygame events and custom game events
    - Event queue management
    """
    
    def __init__(self):
        """Initialize the event dispatcher."""
        # Maps event type to list of listeners
        self._pygame_listeners: Dict[int, List[EventListener]] = defaultdict(list)
        self._custom_listeners: Dict[str, List[EventListener]] = defaultdict(list)
        
        # Event queue for custom events
        self._event_queue: List[GameEvent] = []
    
    def subscribe(
        self, 
        event_type: Any, 
        callback: Callable, 
        priority: EventPriority = EventPriority.NORMAL
    ) -> None:
        """
        Subscribe to an event.
        
        Args:
            event_type: pygame event type constant (e.g., pygame.KEYDOWN) or 
                       custom event type string
            callback: Function to call when event occurs. Should accept the event as argument.
            priority: Priority level for this listener
        """
        listener = EventListener(callback, priority)
        
        if isinstance(event_type, int):
            # Pygame event
            self._pygame_listeners[event_type].append(listener)
            # Sort by priority (highest first)
            self._pygame_listeners[event_type].sort(key=lambda x: x.priority, reverse=True)
        elif isinstance(event_type, str):
            # Custom event
            self._custom_listeners[event_type].append(listener)
            # Sort by priority (highest first)
            self._custom_listeners[event_type].sort(key=lambda x: x.priority, reverse=True)
        else:
            raise TypeError(f"Invalid event_type: {event_type}. Must be int or str.")
    
    def unsubscribe(self, event_type: Any, callback: Callable) -> None:
        """
        Unsubscribe from an event.
        
        Args:
            event_type: Event type to unsubscribe from
            callback: The callback function to remove
        """
        if isinstance(event_type, int):
            # Pygame event
            listeners = self._pygame_listeners[event_type]
            self._pygame_listeners[event_type] = [
                l for l in listeners if l.callback != callback
            ]
        elif isinstance(event_type, str):
            # Custom event
            listeners = self._custom_listeners[event_type]
            self._custom_listeners[event_type] = [
                l for l in listeners if l.callback != callback
            ]
    
    def dispatch_pygame_event(self, event: pygame.event.Event) -> None:
        """
        Dispatch a pygame event to all subscribed listeners.
        
        Args:
            event: Pygame event to dispatch
        """
        listeners = self._pygame_listeners.get(event.type, [])
        for listener in listeners:
            listener(event)
    
    def dispatch_custom_event(self, event_type: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Dispatch a custom game event.
        
        Args:
            event_type: String identifier for the event type
            data: Optional dictionary containing event data
        """
        event = GameEvent(event_type, data)
        self._event_queue.append(event)
    
    def process_custom_events(self) -> None:
        """Process all custom events in the queue."""
        while self._event_queue:
            event = self._event_queue.pop(0)
            listeners = self._custom_listeners.get(event.event_type, [])
            for listener in listeners:
                listener(event)
    
    def clear_all(self) -> None:
        """Clear all event listeners and queued events."""
        self._pygame_listeners.clear()
        self._custom_listeners.clear()
        self._event_queue.clear()
    
    def clear_event_type(self, event_type: Any) -> None:
        """
        Clear all listeners for a specific event type.
        
        Args:
            event_type: Event type to clear
        """
        if isinstance(event_type, int):
            self._pygame_listeners.pop(event_type, None)
        elif isinstance(event_type, str):
            self._custom_listeners.pop(event_type, None)
    
    def has_listeners(self, event_type: Any) -> bool:
        """
        Check if there are any listeners for an event type.
        
        Args:
            event_type: Event type to check
            
        Returns:
            True if there are listeners, False otherwise
        """
        if isinstance(event_type, int):
            return len(self._pygame_listeners.get(event_type, [])) > 0
        elif isinstance(event_type, str):
            return len(self._custom_listeners.get(event_type, [])) > 0
        return False


# Convenience functions for common event patterns

def on_key_down(dispatcher: EventDispatcher, key: int, callback: Callable, 
                priority: EventPriority = EventPriority.NORMAL) -> None:
    """
    Subscribe to a specific key press event.
    
    Args:
        dispatcher: Event dispatcher instance
        key: Pygame key constant (e.g., pygame.K_SPACE)
        callback: Function to call when key is pressed
        priority: Priority level
    """
    def key_filter(event: pygame.event.Event):
        if event.key == key:
            callback(event)
    
    dispatcher.subscribe(pygame.KEYDOWN, key_filter, priority)


def on_mouse_click(dispatcher: EventDispatcher, button: int, callback: Callable,
                   priority: EventPriority = EventPriority.NORMAL) -> None:
    """
    Subscribe to a specific mouse button click event.
    
    Args:
        dispatcher: Event dispatcher instance
        button: Mouse button number (1=left, 2=middle, 3=right)
        callback: Function to call when button is clicked
        priority: Priority level
    """
    def button_filter(event: pygame.event.Event):
        if event.button == button:
            callback(event)
    
    dispatcher.subscribe(pygame.MOUSEBUTTONDOWN, button_filter, priority)
