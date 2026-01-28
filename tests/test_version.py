"""Tests for version module."""

import pytest
from tycoon_engine import __version__, __version_info__
from tycoon_engine.version import MAJOR, MINOR, PATCH


def test_version_exists():
    """Test that version string exists."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_version_format():
    """Test that version follows SemVer format."""
    parts = __version__.split(".")
    assert len(parts) == 3
    for part in parts:
        assert part.isdigit()


def test_version_info():
    """Test that version_info tuple is correct."""
    assert isinstance(__version_info__, tuple)
    assert len(__version_info__) == 3
    assert all(isinstance(x, int) for x in __version_info__)


def test_version_components():
    """Test that version components match version string."""
    version_str = f"{MAJOR}.{MINOR}.{PATCH}"
    assert version_str == __version__


def test_version_info_matches_components():
    """Test that version_info matches individual components."""
    assert __version_info__[0] == MAJOR
    assert __version_info__[1] == MINOR
    assert __version_info__[2] == PATCH
