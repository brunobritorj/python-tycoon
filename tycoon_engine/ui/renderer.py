"""
UI rendering utilities.

Provides helper functions for rendering UI elements with pygame.
"""

import pygame
from typing import Tuple, Optional


class UIRenderer:
    """Helper class for rendering common UI elements."""
    
    @staticmethod
    def draw_text(
        screen: pygame.Surface,
        text: str,
        position: Tuple[int, int],
        font_size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        font_name: Optional[str] = None
    ) -> pygame.Rect:
        """
        Draw text on screen.
        
        Args:
            screen: Surface to draw on
            text: Text to display
            position: (x, y) position
            font_size: Font size
            color: RGB color tuple
            font_name: Font name (None for default)
            
        Returns:
            Rectangle of rendered text
        """
        font = pygame.font.Font(font_name, font_size)
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(topleft=position)
        screen.blit(text_surface, rect)
        return rect
    
    @staticmethod
    def draw_button(
        screen: pygame.Surface,
        text: str,
        rect: pygame.Rect,
        bg_color: Tuple[int, int, int] = (100, 100, 100),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 2
    ) -> None:
        """
        Draw a button.
        
        Args:
            screen: Surface to draw on
            text: Button text
            rect: Button rectangle
            bg_color: Background color
            text_color: Text color
            border_color: Border color (None for no border)
            border_width: Border width in pixels
        """
        # Draw background
        pygame.draw.rect(screen, bg_color, rect)
        
        # Draw border
        if border_color:
            pygame.draw.rect(screen, border_color, rect, border_width)
        
        # Draw text centered
        font = pygame.font.Font(None, 32)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    @staticmethod
    def draw_panel(
        screen: pygame.Surface,
        rect: pygame.Rect,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Tuple[int, int, int] = (100, 100, 100),
        border_width: int = 2,
        alpha: int = 255
    ) -> pygame.Surface:
        """
        Draw a UI panel.
        
        Args:
            screen: Surface to draw on
            rect: Panel rectangle
            bg_color: Background color
            border_color: Border color
            border_width: Border width
            alpha: Alpha transparency (0-255)
            
        Returns:
            Panel surface
        """
        panel = pygame.Surface((rect.width, rect.height))
        panel.set_alpha(alpha)
        panel.fill(bg_color)
        pygame.draw.rect(panel, border_color, panel.get_rect(), border_width)
        screen.blit(panel, rect.topleft)
        return panel
    
    @staticmethod
    def draw_progress_bar(
        screen: pygame.Surface,
        rect: pygame.Rect,
        progress: float,
        bg_color: Tuple[int, int, int] = (50, 50, 50),
        fill_color: Tuple[int, int, int] = (0, 200, 0),
        border_color: Tuple[int, int, int] = (100, 100, 100)
    ) -> None:
        """
        Draw a progress bar.
        
        Args:
            screen: Surface to draw on
            rect: Bar rectangle
            progress: Progress value (0.0 to 1.0)
            bg_color: Background color
            fill_color: Fill color
            border_color: Border color
        """
        # Clamp progress
        progress = max(0.0, min(1.0, progress))
        
        # Draw background
        pygame.draw.rect(screen, bg_color, rect)
        
        # Draw fill
        fill_width = int(rect.width * progress)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(screen, fill_color, fill_rect)
        
        # Draw border
        pygame.draw.rect(screen, border_color, rect, 2)
