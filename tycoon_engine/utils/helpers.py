"""
Utility functions for the game engine.
"""

import time
from typing import Callable


class Timer:
    """Simple timer for tracking time intervals."""
    
    def __init__(self, interval: float, callback: Callable[[], None], repeat: bool = True):
        """
        Initialize a timer.
        
        Args:
            interval: Time interval in seconds (must be positive)
            callback: Function to call when timer expires
            repeat: Whether to repeat the timer
        
        Raises:
            ValueError: If interval is not positive
        """
        if interval <= 0:
            raise ValueError("Timer interval must be positive")
        self.interval = interval
        self.callback = callback
        self.repeat = repeat
        self.elapsed = 0.0
        self.active = True
    
    def update(self, dt: float) -> None:
        """Update the timer."""
        if not self.active:
            return
        
        self.elapsed += dt
        if self.elapsed >= self.interval:
            self.callback()
            if self.repeat:
                # Subtract interval to preserve timing accuracy
                self.elapsed -= self.interval
            else:
                self.active = False
    
    def reset(self) -> None:
        """Reset the timer."""
        self.elapsed = 0.0
        self.active = True
    
    def stop(self) -> None:
        """Stop the timer."""
        self.active = False


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between min and max."""
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between start and end."""
    return start + (end - start) * t


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate distance between two points."""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
