"""
Main menu screen implementation.

Provides a standard main menu with navigation to other game screens.
"""

import pygame
from typing import Callable, Optional
from tycoon_engine.core.state_manager import GameState
from tycoon_engine.ui.ui_manager import UIManager
from tycoon_engine.ui.components import Button, Label, Panel


class MainMenuScreen(GameState):
    """
    Main menu screen state.
    
    Provides buttons for:
    - Play (start game)
    - Multiplayer
    - Settings
    - Quit
    """
    
    def __init__(
        self,
        state_manager,
        on_play: Optional[Callable] = None,
        on_multiplayer: Optional[Callable] = None,
        on_settings: Optional[Callable] = None,
        on_quit: Optional[Callable] = None,
        background_color: tuple = (20, 20, 50)
    ):
        """
        Initialize main menu screen.
        
        Args:
            state_manager: State manager instance
            on_play: Callback for Play button (defaults to changing to "playing" state)
            on_multiplayer: Callback for Multiplayer button (defaults to "multiplayer" state)
            on_settings: Callback for Settings button (defaults to "settings" state)
            on_quit: Callback for Quit button (defaults to pygame.QUIT event)
            background_color: RGB background color
        """
        super().__init__(state_manager)
        self.ui_manager = UIManager()
        self.background_color = background_color
        
        # Store callbacks
        self.on_play = on_play
        self.on_multiplayer = on_multiplayer
        self.on_settings = on_settings
        self.on_quit = on_quit
    
    def enter(self, **kwargs) -> None:
        """Initialize the main menu."""
        # Clear any existing UI
        self.ui_manager.clear_all()
        
        # Get screen dimensions
        screen_width = self.config.screen_width
        screen_height = self.config.screen_height
        
        # Create title label
        title = Label(
            text=self.config.game_title,
            x=screen_width // 2,
            y=100,
            font_size=72,
            color=(255, 215, 0)  # Gold color
        )
        # Center the title
        title.rect.centerx = screen_width // 2
        self.ui_manager.add_component(title)
        
        # Button dimensions
        button_width = 300
        button_height = 60
        button_x = (screen_width - button_width) // 2
        button_spacing = 80
        start_y = 250
        
        # Create Play button
        play_button = Button(
            text="Play",
            x=button_x,
            y=start_y,
            width=button_width,
            height=button_height,
            callback=self._handle_play,
            bg_color=(50, 150, 50),
            hover_color=(70, 200, 70),
            font_size=32
        )
        self.ui_manager.add_component(play_button)
        
        # Create Multiplayer button (if enabled in config)
        if self.config.enable_multiplayer:
            multiplayer_button = Button(
                text="Multiplayer",
                x=button_x,
                y=start_y + button_spacing,
                width=button_width,
                height=button_height,
                callback=self._handle_multiplayer,
                bg_color=(50, 50, 150),
                hover_color=(70, 70, 200),
                font_size=32
            )
            self.ui_manager.add_component(multiplayer_button)
            next_y = start_y + button_spacing * 2
        else:
            next_y = start_y + button_spacing
        
        # Create Settings button
        settings_button = Button(
            text="Settings",
            x=button_x,
            y=next_y,
            width=button_width,
            height=button_height,
            callback=self._handle_settings,
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            font_size=32
        )
        self.ui_manager.add_component(settings_button)
        
        # Create Quit button
        quit_button = Button(
            text="Quit",
            x=button_x,
            y=next_y + button_spacing,
            width=button_width,
            height=button_height,
            callback=self._handle_quit,
            bg_color=(150, 50, 50),
            hover_color=(200, 70, 70),
            font_size=32
        )
        self.ui_manager.add_component(quit_button)
        
        # Version label
        version_label = Label(
            text=f"v{self.config.game_version}",
            x=screen_width - 100,
            y=screen_height - 30,
            font_size=20,
            color=(150, 150, 150)
        )
        self.ui_manager.add_component(version_label)
    
    def exit(self) -> None:
        """Clean up main menu resources."""
        self.ui_manager.clear_all()
    
    def update(self, dt: float) -> None:
        """Update main menu."""
        self.ui_manager.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render main menu."""
        # Draw background
        screen.fill(self.background_color)
        
        # Render UI
        self.ui_manager.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events."""
        # Let UI manager handle events first
        if self.ui_manager.handle_event(event):
            return
        
        # Handle ESC key to quit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._handle_quit()
    
    def _handle_play(self) -> None:
        """Handle Play button click."""
        if self.on_play:
            self.on_play()
        else:
            # Default: change to "playing" state
            if "playing" in self.state_manager.states:
                self.state_manager.change_state("playing")
    
    def _handle_multiplayer(self) -> None:
        """Handle Multiplayer button click."""
        if self.on_multiplayer:
            self.on_multiplayer()
        else:
            # Default: change to "multiplayer" state
            if "multiplayer" in self.state_manager.states:
                self.state_manager.change_state("multiplayer")
    
    def _handle_settings(self) -> None:
        """Handle Settings button click."""
        if self.on_settings:
            self.on_settings()
        else:
            # Default: change to "settings" state
            if "settings" in self.state_manager.states:
                self.state_manager.change_state("settings")
    
    def _handle_quit(self) -> None:
        """Handle Quit button click."""
        if self.on_quit:
            self.on_quit()
        else:
            # Default: post QUIT event
            pygame.event.post(pygame.event.Event(pygame.QUIT))
