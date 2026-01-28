"""
Multiplayer screen implementation.

Provides interface for hosting or joining multiplayer games.
"""

import pygame
from typing import Callable, Optional
from tycoon_engine.core.state_manager import GameState
from tycoon_engine.ui.ui_manager import UIManager
from tycoon_engine.ui.components import Button, Label, Panel, TextInput


class MultiplayerScreen(GameState):
    """
    Multiplayer lobby screen state.
    
    Provides two sub-screens:
    - Host Game: Start server and display connection info
    - Connect to Game: Input field for IP/port and connect button
    """
    
    def __init__(
        self,
        state_manager,
        on_host: Optional[Callable] = None,
        on_connect: Optional[Callable[[str, int], None]] = None,
        on_back: Optional[Callable] = None,
        background_color: tuple = (20, 30, 50)
    ):
        """
        Initialize multiplayer screen.
        
        Args:
            state_manager: State manager instance
            on_host: Callback when hosting a game
            on_connect: Callback when connecting to a game (receives host, port)
            on_back: Callback for Back button (defaults to "main_menu" state)
            background_color: RGB background color
        """
        super().__init__(state_manager)
        self.ui_manager = UIManager()
        self.background_color = background_color
        
        # Store callbacks
        self.on_host = on_host
        self.on_connect = on_connect
        self.on_back = on_back
        
        # Current sub-screen: "menu", "host", or "join"
        self.current_screen = "menu"
        
        # Connection info
        self.hosting = False
        self.connected = False
        self.status_message = ""
        
        # Input fields (will be created in enter())
        self.host_input: Optional[TextInput] = None
        self.port_input: Optional[TextInput] = None
    
    def enter(self, **kwargs) -> None:
        """Initialize the multiplayer screen."""
        self.current_screen = "menu"
        self._build_menu_screen()
    
    def exit(self) -> None:
        """Clean up multiplayer screen resources."""
        self.ui_manager.clear_all()
        self.hosting = False
        self.connected = False
    
    def update(self, dt: float) -> None:
        """Update multiplayer screen."""
        self.ui_manager.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render multiplayer screen."""
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
            if self.current_screen == "menu":
                self._handle_back()
            else:
                # Go back to menu
                self.current_screen = "menu"
                self._build_menu_screen()
    
    def _build_menu_screen(self) -> None:
        """Build the main multiplayer menu."""
        self.ui_manager.clear_all()
        
        screen_width = self.config.screen_width
        screen_height = self.config.screen_height
        
        # Title
        title = Label(
            text="Multiplayer",
            x=screen_width // 2,
            y=80,
            font_size=64,
            color=(255, 255, 255)
        )
        title.rect.centerx = screen_width // 2
        self.ui_manager.add_component(title)
        
        # Button dimensions
        button_width = 300
        button_height = 70
        button_x = (screen_width - button_width) // 2
        button_spacing = 100
        start_y = 250
        
        # Host Game button
        host_button = Button(
            text="Host Game",
            x=button_x,
            y=start_y,
            width=button_width,
            height=button_height,
            callback=self._show_host_screen,
            bg_color=(50, 150, 50),
            hover_color=(70, 200, 70),
            font_size=32
        )
        self.ui_manager.add_component(host_button)
        
        # Join Game button
        join_button = Button(
            text="Join Game",
            x=button_x,
            y=start_y + button_spacing,
            width=button_width,
            height=button_height,
            callback=self._show_join_screen,
            bg_color=(50, 50, 150),
            hover_color=(70, 70, 200),
            font_size=32
        )
        self.ui_manager.add_component(join_button)
        
        # Back button
        back_button = Button(
            text="Back",
            x=button_x,
            y=start_y + button_spacing * 2,
            width=button_width,
            height=button_height,
            callback=self._handle_back,
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            font_size=32
        )
        self.ui_manager.add_component(back_button)
    
    def _show_host_screen(self) -> None:
        """Show the host game screen."""
        self.current_screen = "host"
        self.ui_manager.clear_all()
        
        screen_width = self.config.screen_width
        screen_height = self.config.screen_height
        
        # Title
        title = Label(
            text="Host Game",
            x=screen_width // 2,
            y=80,
            font_size=56,
            color=(255, 255, 255)
        )
        title.rect.centerx = screen_width // 2
        self.ui_manager.add_component(title)
        
        # Info panel
        panel_width = 500
        panel_height = 300
        panel = Panel(
            x=(screen_width - panel_width) // 2,
            y=200,
            width=panel_width,
            height=panel_height,
            bg_color=(40, 40, 60),
            border_color=(100, 100, 150),
            alpha=230
        )
        self.ui_manager.add_component(panel)
        
        # Server info labels
        y_pos = 230
        info_x = (screen_width - panel_width) // 2 + 50
        
        server_label = Label(
            text="Server Information:",
            x=info_x,
            y=y_pos,
            font_size=28,
            color=(200, 200, 200)
        )
        self.ui_manager.add_component(server_label)
        
        y_pos += 50
        host_label = Label(
            text=f"Host: {self.config.server_host}",
            x=info_x,
            y=y_pos,
            font_size=24,
            color=(255, 255, 255)
        )
        self.ui_manager.add_component(host_label)
        
        y_pos += 40
        port_label = Label(
            text=f"Port: {self.config.server_port}",
            x=info_x,
            y=y_pos,
            font_size=24,
            color=(255, 255, 255)
        )
        self.ui_manager.add_component(port_label)
        
        y_pos += 50
        status_label = Label(
            text="Status: Ready to host" if not self.hosting else "Status: Hosting...",
            x=info_x,
            y=y_pos,
            font_size=24,
            color=(100, 255, 100) if self.hosting else (255, 255, 100)
        )
        self.ui_manager.add_component(status_label)
        
        # Buttons
        button_width = 200
        button_height = 50
        button_y = screen_height - 150
        
        # Start Server button
        start_button = Button(
            text="Start Server" if not self.hosting else "Server Running",
            x=(screen_width // 2) - button_width - 20,
            y=button_y,
            width=button_width,
            height=button_height,
            callback=self._handle_host if not self.hosting else None,
            bg_color=(50, 150, 50) if not self.hosting else (100, 100, 100),
            hover_color=(70, 200, 70) if not self.hosting else (100, 100, 100),
            font_size=24
        )
        start_button.enabled = not self.hosting
        self.ui_manager.add_component(start_button)
        
        # Back button
        back_button = Button(
            text="Back",
            x=(screen_width // 2) + 20,
            y=button_y,
            width=button_width,
            height=button_height,
            callback=lambda: (self._build_menu_screen(), setattr(self, 'current_screen', 'menu')),
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            font_size=24
        )
        self.ui_manager.add_component(back_button)
    
    def _show_join_screen(self) -> None:
        """Show the join game screen."""
        self.current_screen = "join"
        self.ui_manager.clear_all()
        
        screen_width = self.config.screen_width
        screen_height = self.config.screen_height
        
        # Title
        title = Label(
            text="Join Game",
            x=screen_width // 2,
            y=80,
            font_size=56,
            color=(255, 255, 255)
        )
        title.rect.centerx = screen_width // 2
        self.ui_manager.add_component(title)
        
        # Info panel
        panel_width = 500
        panel_height = 300
        panel = Panel(
            x=(screen_width - panel_width) // 2,
            y=200,
            width=panel_width,
            height=panel_height,
            bg_color=(40, 40, 60),
            border_color=(100, 100, 150),
            alpha=230
        )
        self.ui_manager.add_component(panel)
        
        # Input fields
        y_pos = 230
        label_x = (screen_width - panel_width) // 2 + 50
        input_x = label_x
        input_width = 400
        
        # Host input
        host_label = Label(
            text="Server Host:",
            x=label_x,
            y=y_pos,
            font_size=24,
            color=(200, 200, 200)
        )
        self.ui_manager.add_component(host_label)
        
        y_pos += 35
        self.host_input = TextInput(
            x=input_x,
            y=y_pos,
            width=input_width,
            height=40,
            initial_text=self.config.server_host,
            placeholder="localhost",
            font_size=20
        )
        self.ui_manager.add_component(self.host_input)
        
        # Port input
        y_pos += 60
        port_label = Label(
            text="Server Port:",
            x=label_x,
            y=y_pos,
            font_size=24,
            color=(200, 200, 200)
        )
        self.ui_manager.add_component(port_label)
        
        y_pos += 35
        self.port_input = TextInput(
            x=input_x,
            y=y_pos,
            width=input_width,
            height=40,
            initial_text=str(self.config.server_port),
            placeholder="5000",
            max_length=10,
            font_size=20
        )
        self.ui_manager.add_component(self.port_input)
        
        # Status message
        y_pos += 60
        self.status_label = Label(
            text=self.status_message,
            x=label_x,
            y=y_pos,
            font_size=20,
            color=(255, 100, 100)
        )
        self.ui_manager.add_component(self.status_label)
        
        # Buttons
        button_width = 200
        button_height = 50
        button_y = screen_height - 150
        
        # Connect button
        connect_button = Button(
            text="Connect",
            x=(screen_width // 2) - button_width - 20,
            y=button_y,
            width=button_width,
            height=button_height,
            callback=self._handle_connect,
            bg_color=(50, 150, 50),
            hover_color=(70, 200, 70),
            font_size=24
        )
        self.ui_manager.add_component(connect_button)
        
        # Back button
        back_button = Button(
            text="Back",
            x=(screen_width // 2) + 20,
            y=button_y,
            width=button_width,
            height=button_height,
            callback=lambda: (self._build_menu_screen(), setattr(self, 'current_screen', 'menu')),
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            font_size=24
        )
        self.ui_manager.add_component(back_button)
    
    def _handle_host(self) -> None:
        """Handle hosting a game."""
        self.hosting = True
        if self.on_host:
            self.on_host()
        else:
            print(f"Hosting game on {self.config.server_host}:{self.config.server_port}")
            print("Note: Server implementation needed")
        
        # Refresh the host screen to show updated status
        self._show_host_screen()
    
    def _handle_connect(self) -> None:
        """Handle connecting to a game."""
        if not self.host_input or not self.port_input:
            return
        
        host = self.host_input.get_text()
        port_str = self.port_input.get_text()
        
        # Validate inputs
        if not host:
            self.status_message = "Please enter a host"
            self.status_label.set_text(self.status_message)
            return
        
        try:
            port = int(port_str)
        except ValueError:
            self.status_message = "Invalid port number"
            self.status_label.set_text(self.status_message)
            return
        
        # Attempt connection
        if self.on_connect:
            self.on_connect(host, port)
        else:
            print(f"Connecting to {host}:{port}")
            print("Note: Client implementation needed")
            self.status_message = "Connected!"
            self.status_label.set_text(self.status_message)
            self.status_label.set_color((100, 255, 100))
    
    def _handle_back(self) -> None:
        """Handle Back button click."""
        if self.on_back:
            self.on_back()
        else:
            # Default: go back to main menu
            if "main_menu" in self.state_manager.states:
                self.state_manager.change_state("main_menu")
