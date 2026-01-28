"""
Tests for asset loader module.
"""

import pytest
import pygame
import tempfile
import os
from pathlib import Path
from tycoon_engine.utils.asset_loader import AssetLoader, get_asset_loader


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test assets."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def asset_loader(temp_dir):
    """Create an asset loader with temp directory."""
    pygame.init()
    return AssetLoader(temp_dir)


def test_asset_loader_creation(asset_loader):
    """Test asset loader creation."""
    assert asset_loader is not None
    assert asset_loader.base_path.exists()


def test_resolve_path(asset_loader, temp_dir):
    """Test path resolution."""
    # Relative path
    relative = "test.png"
    resolved = asset_loader._resolve_path(relative)
    assert resolved == Path(temp_dir) / "test.png"
    
    # Absolute path
    absolute = "/absolute/path/test.png"
    resolved = asset_loader._resolve_path(absolute)
    assert resolved == Path(absolute)


def test_load_font_default(asset_loader):
    """Test loading default font."""
    font = asset_loader.load_font(None, 24)
    assert font is not None
    assert isinstance(font, pygame.font.Font)
    
    # Should be cached
    font2 = asset_loader.load_font(None, 24)
    assert font is font2


def test_load_font_different_sizes(asset_loader):
    """Test loading fonts with different sizes."""
    font1 = asset_loader.load_font(None, 24)
    font2 = asset_loader.load_font(None, 32)
    
    assert font1 is not font2


def test_load_image_not_found(asset_loader):
    """Test loading non-existent image."""
    with pytest.raises(FileNotFoundError):
        asset_loader.load_image("nonexistent.png")


def test_load_sound_not_found(asset_loader):
    """Test loading non-existent sound."""
    with pytest.raises(FileNotFoundError):
        asset_loader.load_sound("nonexistent.wav")


def test_music_volume(asset_loader):
    """Test music volume control."""
    # Skip if mixer not initialized (headless environment)
    if not pygame.mixer.get_init():
        pytest.skip("Audio mixer not available")
    
    # Set volume
    asset_loader.set_music_volume(0.5)
    assert pygame.mixer.music.get_volume() == 0.5
    
    # Clamp to valid range
    asset_loader.set_music_volume(1.5)
    assert pygame.mixer.music.get_volume() == 1.0
    
    asset_loader.set_music_volume(-0.5)
    assert pygame.mixer.music.get_volume() == 0.0


def test_cache_info(asset_loader):
    """Test cache info."""
    info = asset_loader.get_cache_info()
    
    assert 'images' in info
    assert 'fonts' in info
    assert 'sounds' in info
    assert info['images'] == 0
    assert info['fonts'] == 0
    assert info['sounds'] == 0
    
    # Load a font
    asset_loader.load_font(None, 24)
    info = asset_loader.get_cache_info()
    assert info['fonts'] == 1


def test_clear_cache(asset_loader):
    """Test clearing cache."""
    # Load some assets
    asset_loader.load_font(None, 24)
    asset_loader.load_font(None, 32)
    
    assert asset_loader.get_cache_info()['fonts'] == 2
    
    # Clear cache
    asset_loader.clear_cache()
    assert asset_loader.get_cache_info()['fonts'] == 0


def test_clear_specific_cache(asset_loader):
    """Test clearing specific cache types."""
    # Load fonts
    asset_loader.load_font(None, 24)
    asset_loader.load_font(None, 32)
    
    # Clear only fonts
    asset_loader.clear_fonts()
    assert asset_loader.get_cache_info()['fonts'] == 0


def test_get_global_loader():
    """Test global asset loader singleton."""
    loader1 = get_asset_loader()
    loader2 = get_asset_loader()
    
    assert loader1 is loader2


def test_preload_assets(asset_loader):
    """Test preloading assets."""
    # Preload fonts (should not raise errors for default font)
    asset_loader.preload_assets(
        fonts=[(None, 24), (None, 32)]
    )
    
    assert asset_loader.get_cache_info()['fonts'] == 2


def test_music_control(asset_loader):
    """Test music control methods."""
    # Skip if mixer not initialized (headless environment)
    if not pygame.mixer.get_init():
        pytest.skip("Audio mixer not available")
    
    # These should not raise errors even without music loaded
    asset_loader.stop_music()
    asset_loader.pause_music()
    asset_loader.unpause_music()


def test_cache_key_with_scale(asset_loader, temp_dir):
    """Test that scaled images have different cache keys."""
    # Set up display for image operations
    screen = pygame.display.set_mode((100, 100))
    
    # Create a simple test image
    test_image_path = Path(temp_dir) / "test.png"
    surface = pygame.Surface((100, 100))
    pygame.image.save(surface, str(test_image_path))
    
    # Load with different scales
    img1 = asset_loader.load_image("test.png", scale=(50, 50))
    img2 = asset_loader.load_image("test.png", scale=(100, 100))
    
    # Should be different cached objects
    assert img1.get_size() == (50, 50)
    assert img2.get_size() == (100, 100)
