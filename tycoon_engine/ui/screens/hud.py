"""
HUD (Heads-Up Display) screen implementation.

Provides an in-game overlay for displaying game stats and controls.
"""

import pygame
from typing import Callable, Optional, Dict, Any
from tycoon_engine.core.state_manager import GameState
from tycoon_engine.ui.ui_manager import UIManager
from tycoon_engine.ui.components import Button, Label, Panel, ProgressBar


class HUDScreen:
    """
    In-game HUD component (not a full state, but a reusable UI component).
    
    Provides:
    - Resource display (money, etc.)
    - Game stats
    - Menu button (pause/settings)
    - Customizable layout
    
    Note: This is not a GameState but a UI component that can be used
    within playing states.
    """
    
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        on_menu: Optional[Callable] = None,
        show_menu_button: bool = True
    ):
        """
        Initialize HUD.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
            on_menu: Callback for menu button click
            show_menu_button: Whether to show the menu button
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.on_menu = on_menu
        self.show_menu_button = show_menu_button
        
        self.ui_manager = UIManager()
        
        # Data to display
        self.resources: Dict[str, Any] = {}
        self.stats: Dict[str, Any] = {}
        
        # UI components (will be created in build())
        self.resource_labels: Dict[str, Label] = {}
        self.stat_labels: Dict[str, Label] = {}
        self.progress_bars: Dict[str, ProgressBar] = {}
        
        self._build_hud()
    
    def _build_hud(self) -> None:
        """Build the HUD UI components."""
        self.ui_manager.clear_all()
        
        # Top panel for resources
        panel_height = 60
        self.top_panel = Panel(
            x=0,
            y=0,
            width=self.screen_width,
            height=panel_height,
            bg_color=(40, 40, 40),
            border_color=(80, 80, 80),
            alpha=200
        )
        self.ui_manager.add_component(self.top_panel)
        
        # Money label (default resource)
        self.money_label = Label(
            text="Money: $0.00",
            x=20,
            y=18,
            font_size=28,
            color=(255, 215, 0)  # Gold color
        )
        self.ui_manager.add_component(self.money_label)
        self.resource_labels['money'] = self.money_label
        
        # Menu button (top right)
        if self.show_menu_button:
            menu_button = Button(
                text="Menu",
                x=self.screen_width - 130,
                y=10,
                width=120,
                height=40,
                callback=self._handle_menu,
                bg_color=(80, 80, 80),
                hover_color=(120, 120, 120),
                font_size=24
            )
            self.ui_manager.add_component(menu_button)
    
    def update(self, dt: float) -> None:
        """
        Update HUD.
        
        Args:
            dt: Delta time in seconds
        """
        self.ui_manager.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render HUD.
        
        Args:
            screen: Surface to render on
        """
        self.ui_manager.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle events.
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        return self.ui_manager.handle_event(event)
    
    def set_money(self, amount: float) -> None:
        """
        Update money display.
        
        Args:
            amount: Current money amount
        """
        self.resources['money'] = amount
        self.money_label.set_text(f"Money: ${amount:.2f}")
    
    def set_resource(self, name: str, value: Any, format_str: str = "{}") -> None:
        """
        Set a resource value to display.
        
        Args:
            name: Resource name
            value: Resource value
            format_str: Format string for display (must contain {} for value)
        """
        self.resources[name] = value
        
        # Create label if it doesn't exist
        if name not in self.resource_labels and name != 'money':
            x_offset = 200 + len(self.resource_labels) * 150
            label = Label(
                text=format_str.format(value),
                x=x_offset,
                y=18,
                font_size=24,
                color=(200, 200, 200)
            )
            self.ui_manager.add_component(label)
            self.resource_labels[name] = label
        elif name in self.resource_labels:
            self.resource_labels[name].set_text(format_str.format(value))
    
    def set_stat(self, name: str, value: Any, x: int, y: int, 
                 format_str: str = "{}", font_size: int = 20,
                 color: tuple = (255, 255, 255)) -> None:
        """
        Set a stat value to display at a specific position.
        
        Args:
            name: Stat name
            value: Stat value
            x: X position
            y: Y position
            format_str: Format string for display
            font_size: Font size
            color: RGB color
        """
        self.stats[name] = value
        
        # Create label if it doesn't exist
        if name not in self.stat_labels:
            label = Label(
                text=format_str.format(value),
                x=x,
                y=y,
                font_size=font_size,
                color=color
            )
            self.ui_manager.add_component(label)
            self.stat_labels[name] = label
        else:
            self.stat_labels[name].set_text(format_str.format(value))
    
    def add_progress_bar(
        self,
        name: str,
        x: int,
        y: int,
        width: int,
        height: int,
        initial_progress: float = 0.0,
        **kwargs
    ) -> None:
        """
        Add a progress bar to the HUD.
        
        Args:
            name: Progress bar identifier
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
            initial_progress: Initial progress (0.0 to 1.0)
            **kwargs: Additional arguments for ProgressBar
        """
        progress_bar = ProgressBar(
            x=x,
            y=y,
            width=width,
            height=height,
            progress=initial_progress,
            **kwargs
        )
        self.ui_manager.add_component(progress_bar)
        self.progress_bars[name] = progress_bar
    
    def update_progress_bar(self, name: str, progress: float) -> None:
        """
        Update a progress bar value.
        
        Args:
            name: Progress bar identifier
            progress: New progress value (0.0 to 1.0)
        """
        if name in self.progress_bars:
            self.progress_bars[name].set_progress(progress)
    
    def add_button(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        callback: Callable,
        **kwargs
    ) -> Button:
        """
        Add a custom button to the HUD.
        
        Args:
            text: Button text
            x: X position
            y: Y position
            width: Button width
            height: Button height
            callback: Click callback
            **kwargs: Additional Button arguments
            
        Returns:
            Created Button instance
        """
        button = Button(
            text=text,
            x=x,
            y=y,
            width=width,
            height=height,
            callback=callback,
            **kwargs
        )
        self.ui_manager.add_component(button)
        return button
    
    def add_label(
        self,
        text: str,
        x: int,
        y: int,
        **kwargs
    ) -> Label:
        """
        Add a custom label to the HUD.
        
        Args:
            text: Label text
            x: X position
            y: Y position
            **kwargs: Additional Label arguments
            
        Returns:
            Created Label instance
        """
        label = Label(
            text=text,
            x=x,
            y=y,
            **kwargs
        )
        self.ui_manager.add_component(label)
        return label
    
    def clear(self) -> None:
        """Clear all HUD components."""
        self.ui_manager.clear_all()
        self.resource_labels.clear()
        self.stat_labels.clear()
        self.progress_bars.clear()
        self.resources.clear()
        self.stats.clear()
        self._build_hud()
    
    def _handle_menu(self) -> None:
        """Handle menu button click."""
        if self.on_menu:
            self.on_menu()
        else:
            # Default: Do nothing - user should provide a callback
            pass


class PauseMenuState(GameState):
    """
    Pause menu state that can be used with the HUD.
    
    A simple pause menu that can be shown when the menu button is clicked.
    """
    
    def __init__(
        self,
        state_manager,
        on_resume: Optional[Callable] = None,
        on_settings: Optional[Callable] = None,
        on_quit: Optional[Callable] = None,
        background_alpha: int = 180
    ):
        """
        Initialize pause menu.
        
        Args:
            state_manager: State manager instance
            on_resume: Callback for Resume button
            on_settings: Callback for Settings button
            on_quit: Callback for Quit button
            background_alpha: Background overlay alpha (0-255)
        """
        super().__init__(state_manager)
        self.ui_manager = UIManager()
        self.background_alpha = background_alpha
        
        # Store callbacks
        self.on_resume = on_resume
        self.on_settings = on_settings
        self.on_quit = on_quit
        
        # Previous state to return to
        self.previous_state = None
    
    def enter(self, **kwargs) -> None:
        """Initialize pause menu."""
        # Store previous state
        self.previous_state = kwargs.get('previous_state')
        
        self.ui_manager.clear_all()
        
        screen_width = self.config.screen_width
        screen_height = self.config.screen_height
        
        # Semi-transparent overlay
        overlay = Panel(
            x=0,
            y=0,
            width=screen_width,
            height=screen_height,
            bg_color=(0, 0, 0),
            border_color=None,
            alpha=self.background_alpha
        )
        self.ui_manager.add_component(overlay)
        
        # Pause menu panel
        panel_width = 400
        panel_height = 400
        panel = Panel(
            x=(screen_width - panel_width) // 2,
            y=(screen_height - panel_height) // 2,
            width=panel_width,
            height=panel_height,
            bg_color=(50, 50, 50),
            border_color=(150, 150, 150)
        )
        self.ui_manager.add_component(panel)
        
        # Title
        title = Label(
            text="Paused",
            x=screen_width // 2,
            y=(screen_height - panel_height) // 2 + 50,
            font_size=48,
            color=(255, 255, 255)
        )
        title.rect.centerx = screen_width // 2
        self.ui_manager.add_component(title)
        
        # Buttons
        button_width = 250
        button_height = 50
        button_x = (screen_width - button_width) // 2
        start_y = screen_height // 2 - 50
        spacing = 70
        
        # Resume button
        resume_button = Button(
            text="Resume",
            x=button_x,
            y=start_y,
            width=button_width,
            height=button_height,
            callback=self._handle_resume,
            bg_color=(50, 150, 50),
            hover_color=(70, 200, 70),
            font_size=28
        )
        self.ui_manager.add_component(resume_button)
        
        # Settings button
        settings_button = Button(
            text="Settings",
            x=button_x,
            y=start_y + spacing,
            width=button_width,
            height=button_height,
            callback=self._handle_settings,
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            font_size=28
        )
        self.ui_manager.add_component(settings_button)
        
        # Quit button
        quit_button = Button(
            text="Quit to Menu",
            x=button_x,
            y=start_y + spacing * 2,
            width=button_width,
            height=button_height,
            callback=self._handle_quit,
            bg_color=(150, 50, 50),
            hover_color=(200, 70, 70),
            font_size=28
        )
        self.ui_manager.add_component(quit_button)
    
    def exit(self) -> None:
        """Clean up pause menu."""
        self.ui_manager.clear_all()
    
    def update(self, dt: float) -> None:
        """Update pause menu."""
        self.ui_manager.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render pause menu."""
        # Note: The previous state's render is not called,
        # so we show a static paused screen
        self.ui_manager.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events."""
        # Let UI manager handle events first
        if self.ui_manager.handle_event(event):
            return
        
        # ESC to resume
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._handle_resume()
    
    def _handle_resume(self) -> None:
        """Handle Resume button."""
        if self.on_resume:
            self.on_resume()
        elif self.previous_state:
            self.state_manager.change_state(self.previous_state)
    
    def _handle_settings(self) -> None:
        """Handle Settings button."""
        if self.on_settings:
            self.on_settings()
        elif "settings" in self.state_manager.states:
            self.state_manager.change_state("settings")
    
    def _handle_quit(self) -> None:
        """Handle Quit button."""
        if self.on_quit:
            self.on_quit()
        elif "main_menu" in self.state_manager.states:
            self.state_manager.change_state("main_menu")
