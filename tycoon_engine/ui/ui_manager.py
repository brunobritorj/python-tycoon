"""
UI manager module.

Manages UI element lifecycle, event routing, and rendering order.
"""

import pygame
from typing import List, Optional
from tycoon_engine.ui.components import UIComponent


class UIManager:
    """
    Manages UI components and their interactions.
    
    Provides:
    - Component registration and lifecycle management
    - Event routing to components
    - Z-order/layering support
    - Focus management
    """
    
    def __init__(self):
        """Initialize the UI manager."""
        self.components: List[UIComponent] = []
        self.focused_component: Optional[UIComponent] = None
    
    def add_component(self, component: UIComponent, z_order: Optional[int] = None) -> None:
        """
        Add a UI component to be managed.
        
        Args:
            component: Component to add
            z_order: Optional z-order for rendering (higher values render on top).
                    Note: This is a placeholder for future implementation.
                    Currently components render in order added.
        """
        # TODO: Implement proper z-ordering system
        # For now, just append to the list
        self.components.append(component)
    
    def remove_component(self, component: UIComponent) -> None:
        """
        Remove a UI component.
        
        Args:
            component: Component to remove
        """
        if component in self.components:
            self.components.remove(component)
            
            # Clear focus if this was the focused component
            if self.focused_component == component:
                self.focused_component = None
    
    def clear_all(self) -> None:
        """Remove all components."""
        self.components.clear()
        self.focused_component = None
    
    def update(self, dt: float) -> None:
        """
        Update all UI components.
        
        Args:
            dt: Delta time in seconds
        """
        for component in self.components:
            if component.visible:
                component.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render all UI components in order.
        
        Args:
            screen: Surface to render on
        """
        for component in self.components:
            if component.visible:
                component.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Route event to UI components.
        
        Events are sent to components in reverse order (top to bottom)
        so that components on top can handle events first.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            True if event was handled by any component, False otherwise
        """
        # Handle events in reverse order (top components first)
        for component in reversed(self.components):
            if component.visible and component.enabled:
                if component.handle_event(event):
                    # Update focus for certain event types
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.set_focus(component)
                    return True
        
        # Clear focus if clicked outside any component
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clear_focus()
        
        return False
    
    def set_focus(self, component: Optional[UIComponent]) -> None:
        """
        Set focus to a specific component.
        
        Args:
            component: Component to focus (None to clear focus)
        """
        self.focused_component = component
    
    def clear_focus(self) -> None:
        """Clear focus from all components."""
        self.focused_component = None
    
    def get_focused_component(self) -> Optional[UIComponent]:
        """
        Get the currently focused component.
        
        Returns:
            Currently focused component or None
        """
        return self.focused_component
    
    def get_component_at(self, x: int, y: int) -> Optional[UIComponent]:
        """
        Get the topmost component at given position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Component at position or None
        """
        # Check in reverse order (top components first)
        for component in reversed(self.components):
            if component.visible and component.rect.collidepoint(x, y):
                return component
        return None
    
    def get_hovered_component(self) -> Optional[UIComponent]:
        """
        Get the topmost component currently under the mouse.
        
        Returns:
            Hovered component or None
        """
        mouse_pos = pygame.mouse.get_pos()
        return self.get_component_at(mouse_pos[0], mouse_pos[1])
    
    def bring_to_front(self, component: UIComponent) -> None:
        """
        Bring a component to the front (render on top).
        
        Args:
            component: Component to bring forward
        """
        if component in self.components:
            self.components.remove(component)
            self.components.append(component)
    
    def send_to_back(self, component: UIComponent) -> None:
        """
        Send a component to the back (render behind others).
        
        Args:
            component: Component to send back
        """
        if component in self.components:
            self.components.remove(component)
            self.components.insert(0, component)
    
    def show_all(self) -> None:
        """Make all components visible."""
        for component in self.components:
            component.visible = True
    
    def hide_all(self) -> None:
        """Hide all components."""
        for component in self.components:
            component.visible = False
    
    def enable_all(self) -> None:
        """Enable all components."""
        for component in self.components:
            component.enabled = True
    
    def disable_all(self) -> None:
        """Disable all components."""
        for component in self.components:
            component.enabled = False
    
    def get_components(self) -> List[UIComponent]:
        """
        Get list of all managed components.
        
        Returns:
            List of components
        """
        return self.components.copy()
    
    def count(self) -> int:
        """
        Get the number of managed components.
        
        Returns:
            Number of components
        """
        return len(self.components)
