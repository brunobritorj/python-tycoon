"""
UI components module.

Provides reusable UI components for building game interfaces.
"""

import pygame
from typing import Optional, Tuple, Callable, List
from enum import Enum


class Alignment(Enum):
    """Text alignment options."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class UIComponent:
    """
    Base class for all UI components.
    
    Provides common functionality for positioning, visibility, and event handling.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize UI component.
        
        Args:
            x: X position
            y: Y position
            width: Component width
            height: Component height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
    
    def update(self, dt: float) -> None:
        """
        Update component logic.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the component.
        
        Args:
            screen: Surface to render on
        """
        pass
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event.
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled, False otherwise
        """
        return False
    
    def is_hovered(self) -> bool:
        """Check if mouse is hovering over component."""
        if not self.visible or not self.enabled:
            return False
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)


class Label(UIComponent):
    """
    Text label component.
    
    Displays static or dynamic text with customizable appearance.
    """
    
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        font_size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        font_path: Optional[str] = None,
        alignment: Alignment = Alignment.LEFT
    ):
        """
        Initialize label.
        
        Args:
            text: Text to display
            x: X position
            y: Y position
            font_size: Font size in points
            color: RGB color tuple
            font_path: Path to custom font (None for default)
            alignment: Text alignment
        """
        # Initialize with temporary size (will be updated when text is rendered)
        super().__init__(x, y, 0, 0)
        
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font_path = font_path
        self.alignment = alignment
        
        # Load font
        self.font = pygame.font.Font(font_path, font_size)
        
        # Render initial text
        self._update_surface()
    
    def _update_surface(self) -> None:
        """Update the rendered text surface."""
        self.surface = self.font.render(self.text, True, self.color)
        
        # Update rect size
        self.rect.width = self.surface.get_width()
        self.rect.height = self.surface.get_height()
        
        # Adjust position based on alignment
        if self.alignment == Alignment.CENTER:
            self.text_rect = self.surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        elif self.alignment == Alignment.RIGHT:
            self.text_rect = self.surface.get_rect(topright=(self.rect.right, self.rect.top))
        else:  # LEFT
            self.text_rect = self.surface.get_rect(topleft=(self.rect.left, self.rect.top))
    
    def set_text(self, text: str) -> None:
        """Update label text."""
        if self.text != text:
            self.text = text
            self._update_surface()
    
    def set_color(self, color: Tuple[int, int, int]) -> None:
        """Update label color."""
        if self.color != color:
            self.color = color
            self._update_surface()
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the label."""
        if self.visible:
            screen.blit(self.surface, self.text_rect)


class Button(UIComponent):
    """
    Clickable button component.
    
    Supports hover states, click callbacks, and customizable appearance.
    """
    
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        callback: Optional[Callable] = None,
        bg_color: Tuple[int, int, int] = (100, 100, 100),
        hover_color: Tuple[int, int, int] = (150, 150, 150),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 2,
        font_size: int = 24,
        font_path: Optional[str] = None
    ):
        """
        Initialize button.
        
        Args:
            text: Button text
            x: X position
            y: Y position
            width: Button width
            height: Button height
            callback: Function to call when button is clicked
            bg_color: Background color
            hover_color: Color when hovered
            text_color: Text color
            border_color: Border color (None for no border)
            border_width: Border width in pixels
            font_size: Font size
            font_path: Path to custom font
        """
        super().__init__(x, y, width, height)
        
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        
        # Load font and render text
        self.font = pygame.font.Font(font_path, font_size)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def set_text(self, text: str) -> None:
        """Update button text."""
        if self.text != text:
            self.text = text
            self.text_surface = self.font.render(text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the button."""
        if not self.visible:
            return
        
        # Choose color based on hover state
        color = self.hover_color if self.is_hovered() and self.enabled else self.bg_color
        
        # Draw button background
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw border if specified
        if self.border_color:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        
        # Draw text
        screen.blit(self.text_surface, self.text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.is_hovered():
                if self.callback:
                    self.callback()
                return True
        
        return False


class Panel(UIComponent):
    """
    Container panel component.
    
    Can hold multiple child components and provides a background.
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Optional[Tuple[int, int, int]] = (100, 100, 100),
        border_width: int = 2,
        alpha: int = 255
    ):
        """
        Initialize panel.
        
        Args:
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
            bg_color: Background color
            border_color: Border color (None for no border)
            border_width: Border width in pixels
            alpha: Alpha transparency (0-255)
        """
        super().__init__(x, y, width, height)
        
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.alpha = alpha
        
        # Child components
        self.children: List[UIComponent] = []
        
        # Create panel surface
        self._create_surface()
    
    def _create_surface(self) -> None:
        """Create the panel surface with background and border."""
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.surface.set_alpha(self.alpha)
        self.surface.fill(self.bg_color)
        
        if self.border_color:
            pygame.draw.rect(
                self.surface,
                self.border_color,
                self.surface.get_rect(),
                self.border_width
            )
    
    def add_child(self, child: UIComponent) -> None:
        """
        Add a child component to the panel.
        
        Args:
            child: Component to add
        """
        self.children.append(child)
    
    def remove_child(self, child: UIComponent) -> None:
        """
        Remove a child component from the panel.
        
        Args:
            child: Component to remove
        """
        if child in self.children:
            self.children.remove(child)
    
    def update(self, dt: float) -> None:
        """Update panel and all children."""
        if self.visible:
            for child in self.children:
                child.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render panel and all children."""
        if not self.visible:
            return
        
        # Draw panel background
        screen.blit(self.surface, self.rect.topleft)
        
        # Draw children
        for child in self.children:
            child.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for panel and children."""
        if not self.visible or not self.enabled:
            return False
        
        # Let children handle events first (reverse order for proper z-ordering)
        for child in reversed(self.children):
            if child.handle_event(event):
                return True
        
        return False


class ProgressBar(UIComponent):
    """
    Progress bar component.
    
    Displays a progress value as a filled bar.
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        progress: float = 0.0,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        fill_color: Tuple[int, int, int] = (0, 200, 0),
        border_color: Tuple[int, int, int] = (100, 100, 100),
        border_width: int = 2
    ):
        """
        Initialize progress bar.
        
        Args:
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
            progress: Initial progress (0.0 to 1.0)
            bg_color: Background color
            fill_color: Fill color
            border_color: Border color
            border_width: Border width in pixels
        """
        super().__init__(x, y, width, height)
        
        self.progress = max(0.0, min(1.0, progress))
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width
    
    def set_progress(self, progress: float) -> None:
        """
        Set progress value.
        
        Args:
            progress: Progress value (0.0 to 1.0)
        """
        self.progress = max(0.0, min(1.0, progress))
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the progress bar."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Draw fill
        fill_width = int(self.rect.width * self.progress)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, self.fill_color, fill_rect)
        
        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)


class TextInput(UIComponent):
    """
    Text input field component.
    
    Allows user to type text input.
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        initial_text: str = "",
        placeholder: str = "",
        max_length: int = 50,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        placeholder_color: Tuple[int, int, int] = (150, 150, 150),
        border_color: Tuple[int, int, int] = (100, 100, 100),
        active_border_color: Tuple[int, int, int] = (200, 200, 200),
        border_width: int = 2,
        font_size: int = 24,
        font_path: Optional[str] = None
    ):
        """
        Initialize text input.
        
        Args:
            x: X position
            y: Y position
            width: Input width
            height: Input height
            initial_text: Initial text value
            placeholder: Placeholder text when empty
            max_length: Maximum text length
            bg_color: Background color
            text_color: Text color
            placeholder_color: Placeholder text color
            border_color: Border color when inactive
            active_border_color: Border color when active
            border_width: Border width in pixels
            font_size: Font size
            font_path: Path to custom font
        """
        super().__init__(x, y, width, height)
        
        self.text = initial_text
        self.placeholder = placeholder
        self.max_length = max_length
        self.bg_color = bg_color
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.border_color = border_color
        self.active_border_color = active_border_color
        self.border_width = border_width
        
        self.active = False  # Is input currently focused
        self.cursor_visible = True
        self.cursor_timer = 0.0
        
        # Load font
        self.font = pygame.font.Font(font_path, font_size)
    
    def update(self, dt: float) -> None:
        """Update cursor blink animation."""
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0.0
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the text input."""
        if not self.visible:
            return
        
        # Draw background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Draw border (different color when active)
        border_color = self.active_border_color if self.active else self.border_color
        pygame.draw.rect(screen, border_color, self.rect, self.border_width)
        
        # Draw text or placeholder
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
        elif self.placeholder and not self.active:
            text_surface = self.font.render(self.placeholder, True, self.placeholder_color)
        else:
            text_surface = self.font.render("", True, self.text_color)
        
        # Position text with padding
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
        screen.blit(text_surface, text_rect)
        
        # Draw cursor when active
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            cursor_y1 = self.rect.centery - 10
            cursor_y2 = self.rect.centery + 10
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle keyboard and mouse events."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicked on input
            self.active = self.is_hovered()
            self.cursor_visible = True
            self.cursor_timer = 0.0
            return self.active
        
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Add character if not at max length
                if len(self.text) < self.max_length and event.unicode.isprintable():
                    self.text += event.unicode
            return True
        
        return False
    
    def get_text(self) -> str:
        """Get current text value."""
        return self.text
    
    def set_text(self, text: str) -> None:
        """Set text value."""
        self.text = text[:self.max_length]
