"""
Asset loader module.

Provides resource loading and management for images, fonts, and audio files.
"""

import pygame
import os
from typing import Dict, Optional, Tuple
from pathlib import Path


class AssetLoader:
    """
    Asset loader and manager for game resources.
    
    Handles loading and caching of:
    - Images (PNG, JPG, BMP, GIF)
    - Fonts (TTF, OTF)
    - Sounds (WAV, OGG, MP3)
    - Music (WAV, OGG, MP3)
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the asset loader.
        
        Args:
            base_path: Base directory for assets. If None, uses current directory.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        
        # Caches for loaded resources
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
        self._sound_cache: Dict[str, pygame.mixer.Sound] = {}
        
        # Track loaded music file
        self._current_music: Optional[str] = None
        
        # Initialize pygame modules if not already initialized
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error:
                print("Warning: Could not initialize audio mixer")
    
    def _resolve_path(self, relative_path: str) -> Path:
        """
        Resolve a relative asset path to absolute path.
        
        Args:
            relative_path: Relative path to asset
            
        Returns:
            Absolute path to asset
        """
        path = Path(relative_path)
        if path.is_absolute():
            return path
        return self.base_path / path
    
    def load_image(
        self, 
        path: str, 
        alpha: bool = True,
        scale: Optional[Tuple[int, int]] = None
    ) -> pygame.Surface:
        """
        Load an image file.
        
        Args:
            path: Path to image file (relative to base_path or absolute)
            alpha: Whether to convert image with alpha channel
            scale: Optional (width, height) tuple to scale the image
            
        Returns:
            Loaded pygame Surface
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            pygame.error: If image cannot be loaded
        """
        # Check cache first
        cache_key = f"{path}_{scale}"
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        
        # Resolve and load image
        full_path = self._resolve_path(path)
        if not full_path.exists():
            raise FileNotFoundError(f"Image not found: {full_path}")
        
        try:
            image = pygame.image.load(str(full_path))
            
            # Convert for better performance
            if alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            
            # Scale if requested
            if scale:
                image = pygame.transform.scale(image, scale)
            
            # Cache the image
            self._image_cache[cache_key] = image
            
            return image
        except pygame.error as e:
            raise pygame.error(f"Failed to load image {full_path}: {e}")
    
    def load_font(self, path: Optional[str], size: int = 24) -> pygame.font.Font:
        """
        Load a font file.
        
        Args:
            path: Path to font file (TTF, OTF). If None, uses pygame default font.
            size: Font size in points
            
        Returns:
            Loaded pygame Font
            
        Raises:
            FileNotFoundError: If font file doesn't exist
            pygame.error: If font cannot be loaded
        """
        # Check cache first
        cache_key = (path or "default", size)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        try:
            if path is None:
                # Use default pygame font
                font = pygame.font.Font(None, size)
            else:
                # Resolve and load custom font
                full_path = self._resolve_path(path)
                if not full_path.exists():
                    raise FileNotFoundError(f"Font not found: {full_path}")
                font = pygame.font.Font(str(full_path), size)
            
            # Cache the font
            self._font_cache[cache_key] = font
            
            return font
        except pygame.error as e:
            raise pygame.error(f"Failed to load font: {e}")
    
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """
        Load a sound effect file.
        
        Args:
            path: Path to sound file (WAV, OGG)
            
        Returns:
            Loaded pygame Sound
            
        Raises:
            FileNotFoundError: If sound file doesn't exist
            pygame.error: If sound cannot be loaded
        """
        # Check cache first
        if path in self._sound_cache:
            return self._sound_cache[path]
        
        # Resolve and load sound
        full_path = self._resolve_path(path)
        if not full_path.exists():
            raise FileNotFoundError(f"Sound not found: {full_path}")
        
        try:
            sound = pygame.mixer.Sound(str(full_path))
            
            # Cache the sound
            self._sound_cache[path] = sound
            
            return sound
        except pygame.error as e:
            raise pygame.error(f"Failed to load sound {full_path}: {e}")
    
    def load_music(self, path: str) -> None:
        """
        Load a music file for background music.
        
        Note: Unlike sounds, music is streamed and not loaded into memory.
        Only one music file can be loaded at a time.
        
        Args:
            path: Path to music file (MP3, OGG, WAV)
            
        Raises:
            FileNotFoundError: If music file doesn't exist
            pygame.error: If music cannot be loaded
        """
        # Resolve path
        full_path = self._resolve_path(path)
        if not full_path.exists():
            raise FileNotFoundError(f"Music not found: {full_path}")
        
        try:
            pygame.mixer.music.load(str(full_path))
            self._current_music = path
        except pygame.error as e:
            raise pygame.error(f"Failed to load music {full_path}: {e}")
    
    def play_music(self, loops: int = -1, start: float = 0.0) -> None:
        """
        Play the currently loaded music.
        
        Args:
            loops: Number of times to loop (-1 for infinite)
            start: Starting position in seconds
        """
        if self._current_music is None:
            raise RuntimeError("No music loaded. Call load_music() first.")
        pygame.mixer.music.play(loops, start)
    
    def stop_music(self) -> None:
        """Stop the currently playing music."""
        pygame.mixer.music.stop()
    
    def pause_music(self) -> None:
        """Pause the currently playing music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self) -> None:
        """Unpause the currently paused music."""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume: float) -> None:
        """
        Set music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
    
    def clear_cache(self) -> None:
        """Clear all cached assets to free memory."""
        self._image_cache.clear()
        self._font_cache.clear()
        self._sound_cache.clear()
    
    def clear_images(self) -> None:
        """Clear only the image cache."""
        self._image_cache.clear()
    
    def clear_fonts(self) -> None:
        """Clear only the font cache."""
        self._font_cache.clear()
    
    def clear_sounds(self) -> None:
        """Clear only the sound cache."""
        self._sound_cache.clear()
    
    def get_cache_info(self) -> Dict[str, int]:
        """
        Get information about cached assets.
        
        Returns:
            Dictionary with counts of cached assets
        """
        return {
            'images': len(self._image_cache),
            'fonts': len(self._font_cache),
            'sounds': len(self._sound_cache)
        }
    
    def preload_assets(
        self,
        images: Optional[list] = None,
        fonts: Optional[list] = None,
        sounds: Optional[list] = None
    ) -> None:
        """
        Preload multiple assets at once.
        
        Args:
            images: List of image paths to preload
            fonts: List of (path, size) tuples for fonts to preload
            sounds: List of sound paths to preload
        """
        if images:
            for image_path in images:
                try:
                    self.load_image(image_path)
                except (FileNotFoundError, pygame.error) as e:
                    print(f"Warning: Could not preload image {image_path}: {e}")
        
        if fonts:
            for font_path, size in fonts:
                try:
                    self.load_font(font_path, size)
                except (FileNotFoundError, pygame.error) as e:
                    print(f"Warning: Could not preload font {font_path}: {e}")
        
        if sounds:
            for sound_path in sounds:
                try:
                    self.load_sound(sound_path)
                except (FileNotFoundError, pygame.error) as e:
                    print(f"Warning: Could not preload sound {sound_path}: {e}")


# Global asset loader instance (singleton pattern)
_global_loader: Optional[AssetLoader] = None


def get_asset_loader(base_path: Optional[str] = None) -> AssetLoader:
    """
    Get the global asset loader instance.
    
    Args:
        base_path: Base path for assets (only used on first call)
        
    Returns:
        Global AssetLoader instance
    """
    global _global_loader
    if _global_loader is None:
        _global_loader = AssetLoader(base_path)
    return _global_loader
