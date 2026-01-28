"""
Settings screen implementation.

Provides a settings menu for game configuration.
"""

import pygame
from typing import Callable, Optional, List, Tuple
from tycoon_engine.core.state_manager import GameState
from tycoon_engine.ui.ui_manager import UIManager
from tycoon_engine.ui.components import Button, Label, Panel


class SettingsScreen(GameState):
    """
    Settings menu screen state.
    
    Provides options for:
    - Volume controls
    - Resolution options
    - Graphics settings
    - Save/Apply settings
    - Back to main menu
    """
    
    def __init__(
        self,
        state_manager,
        on_back: Optional[Callable] = None,
        on_apply: Optional[Callable] = None,
        background_color: tuple = (30, 30, 30)
    ):
        """
        Initialize settings screen.
        
        Args:
            state_manager: State manager instance
            on_back: Callback for Back button (defaults to "main_menu" state)
            on_apply: Callback when settings are applied
            background_color: RGB background color
        """
        super().__init__(state_manager)
        self.ui_manager = UIManager()
        self.background_color = background_color
        
        # Store callbacks
        self.on_back = on_back
        self.on_apply = on_apply
        
        # Settings values
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.resolution_index = 0
        self.fullscreen = False
        
        # Available resolutions
        self.resolutions: List[Tuple[int, int]] = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1920, 1080)
        ]
    
    def enter(self, **kwargs) -> None:
        """Initialize the settings menu."""
        # Clear any existing UI
        self.ui_manager.clear_all()
        
        # Get screen dimensions
        screen_width = self.config.screen_width
        screen_height = self.config.screen_height
        
        # Load current settings
        self.fullscreen = self.config.fullscreen
        # Find current resolution index
        current_res = (self.config.screen_width, self.config.screen_height)
        if current_res in self.resolutions:
            self.resolution_index = self.resolutions.index(current_res)
        
        # Create title label
        title = Label(
            text="Settings",
            x=screen_width // 2,
            y=50,
            font_size=64,
            color=(255, 255, 255)
        )
        title.rect.centerx = screen_width // 2
        self.ui_manager.add_component(title)
        
        # Create settings panel
        panel_width = 600
        panel_height = 400
        panel = Panel(
            x=(screen_width - panel_width) // 2,
            y=150,
            width=panel_width,
            height=panel_height,
            bg_color=(50, 50, 50),
            border_color=(100, 100, 100),
            alpha=230
        )
        self.ui_manager.add_component(panel)
        
        # Settings labels and values (displayed on panel)
        y_offset = 180
        x_label = (screen_width - panel_width) // 2 + 50
        x_value = x_label + 300
        spacing = 60
        
        # Music Volume
        music_label = Label(
            text="Music Volume:",
            x=x_label,
            y=y_offset,
            font_size=28,
            color=(200, 200, 200)
        )
        self.ui_manager.add_component(music_label)
        
        self.music_value_label = Label(
            text=f"{int(self.music_volume * 100)}%",
            x=x_value,
            y=y_offset,
            font_size=28,
            color=(255, 255, 255)
        )
        self.ui_manager.add_component(self.music_value_label)
        
        # Music volume buttons
        music_minus = Button(
            text="-",
            x=x_value + 80,
            y=y_offset - 5,
            width=40,
            height=40,
            callback=lambda: self._change_music_volume(-0.1),
            font_size=24
        )
        self.ui_manager.add_component(music_minus)
        
        music_plus = Button(
            text="+",
            x=x_value + 130,
            y=y_offset - 5,
            width=40,
            height=40,
            callback=lambda: self._change_music_volume(0.1),
            font_size=24
        )
        self.ui_manager.add_component(music_plus)
        
        # SFX Volume
        y_offset += spacing
        sfx_label = Label(
            text="SFX Volume:",
            x=x_label,
            y=y_offset,
            font_size=28,
            color=(200, 200, 200)
        )
        self.ui_manager.add_component(sfx_label)
        
        self.sfx_value_label = Label(
            text=f"{int(self.sfx_volume * 100)}%",
            x=x_value,
            y=y_offset,
            font_size=28,
            color=(255, 255, 255)
        )
        self.ui_manager.add_component(self.sfx_value_label)
        
        # SFX volume buttons
        sfx_minus = Button(
            text="-",
            x=x_value + 80,
            y=y_offset - 5,
            width=40,
            height=40,
            callback=lambda: self._change_sfx_volume(-0.1),
            font_size=24
        )
        self.ui_manager.add_component(sfx_minus)
        
        sfx_plus = Button(
            text="+",
            x=x_value + 130,
            y=y_offset - 5,
            width=40,
            height=40,
            callback=lambda: self._change_sfx_volume(0.1),
            font_size=24
        )
        self.ui_manager.add_component(sfx_plus)
        
        # Resolution
        y_offset += spacing
        res_label = Label(
            text="Resolution:",
            x=x_label,
            y=y_offset,
            font_size=28,
            color=(200, 200, 200)
        )
        self.ui_manager.add_component(res_label)
        
        self.res_value_label = Label(
            text=self._get_resolution_text(),
            x=x_value,
            y=y_offset,
            font_size=28,
            color=(255, 255, 255)
        )
        self.ui_manager.add_component(self.res_value_label)
        
        # Resolution buttons
        res_prev = Button(
            text="<",
            x=x_value + 150,
            y=y_offset - 5,
            width=40,
            height=40,
            callback=self._prev_resolution,
            font_size=24
        )
        self.ui_manager.add_component(res_prev)
        
        res_next = Button(
            text=">",
            x=x_value + 200,
            y=y_offset - 5,
            width=40,
            height=40,
            callback=self._next_resolution,
            font_size=24
        )
        self.ui_manager.add_component(res_next)
        
        # Fullscreen toggle
        y_offset += spacing
        fullscreen_label = Label(
            text="Fullscreen:",
            x=x_label,
            y=y_offset,
            font_size=28,
            color=(200, 200, 200)
        )
        self.ui_manager.add_component(fullscreen_label)
        
        self.fullscreen_button = Button(
            text="On" if self.fullscreen else "Off",
            x=x_value,
            y=y_offset - 5,
            width=100,
            height=40,
            callback=self._toggle_fullscreen,
            bg_color=(50, 150, 50) if self.fullscreen else (150, 50, 50),
            hover_color=(70, 200, 70) if self.fullscreen else (200, 70, 70),
            font_size=24
        )
        self.ui_manager.add_component(self.fullscreen_button)
        
        # Bottom buttons
        button_width = 200
        button_height = 50
        button_y = screen_height - 100
        
        # Apply button
        apply_button = Button(
            text="Apply",
            x=(screen_width // 2) - button_width - 20,
            y=button_y,
            width=button_width,
            height=button_height,
            callback=self._handle_apply,
            bg_color=(50, 150, 50),
            hover_color=(70, 200, 70),
            font_size=28
        )
        self.ui_manager.add_component(apply_button)
        
        # Back button
        back_button = Button(
            text="Back",
            x=(screen_width // 2) + 20,
            y=button_y,
            width=button_width,
            height=button_height,
            callback=self._handle_back,
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            font_size=28
        )
        self.ui_manager.add_component(back_button)
    
    def exit(self) -> None:
        """Clean up settings menu resources."""
        self.ui_manager.clear_all()
    
    def update(self, dt: float) -> None:
        """Update settings menu."""
        self.ui_manager.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render settings menu."""
        # Draw background
        screen.fill(self.background_color)
        
        # Render UI
        self.ui_manager.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events."""
        # Let UI manager handle events first
        if self.ui_manager.handle_event(event):
            return
        
        # Handle ESC key to go back
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._handle_back()
    
    def _change_music_volume(self, delta: float) -> None:
        """Change music volume."""
        self.music_volume = max(0.0, min(1.0, self.music_volume + delta))
        self.music_value_label.set_text(f"{int(self.music_volume * 100)}%")
        pygame.mixer.music.set_volume(self.music_volume)
    
    def _change_sfx_volume(self, delta: float) -> None:
        """Change SFX volume."""
        self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + delta))
        self.sfx_value_label.set_text(f"{int(self.sfx_volume * 100)}%")
    
    def _prev_resolution(self) -> None:
        """Select previous resolution."""
        self.resolution_index = (self.resolution_index - 1) % len(self.resolutions)
        self.res_value_label.set_text(self._get_resolution_text())
    
    def _next_resolution(self) -> None:
        """Select next resolution."""
        self.resolution_index = (self.resolution_index + 1) % len(self.resolutions)
        self.res_value_label.set_text(self._get_resolution_text())
    
    def _get_resolution_text(self) -> str:
        """Get current resolution as text."""
        w, h = self.resolutions[self.resolution_index]
        return f"{w}x{h}"
    
    def _toggle_fullscreen(self) -> None:
        """Toggle fullscreen setting."""
        self.fullscreen = not self.fullscreen
        self.fullscreen_button.set_text("On" if self.fullscreen else "Off")
        self.fullscreen_button.bg_color = (50, 150, 50) if self.fullscreen else (150, 50, 50)
        self.fullscreen_button.hover_color = (70, 200, 70) if self.fullscreen else (200, 70, 70)
    
    def _handle_apply(self) -> None:
        """Handle Apply button click."""
        # Update config
        w, h = self.resolutions[self.resolution_index]
        self.config.screen_width = w
        self.config.screen_height = h
        self.config.fullscreen = self.fullscreen
        
        # Call custom callback if provided
        if self.on_apply:
            self.on_apply()
        
        print(f"Settings applied: {w}x{h}, Fullscreen: {self.fullscreen}")
        print("Note: Resolution changes require restart")
    
    def _handle_back(self) -> None:
        """Handle Back button click."""
        if self.on_back:
            self.on_back()
        else:
            # Default: go back to main menu
            if "main_menu" in self.state_manager.states:
                self.state_manager.change_state("main_menu")
