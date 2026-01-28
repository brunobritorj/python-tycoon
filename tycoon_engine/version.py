"""Version information for Tycoon Engine."""

__version__ = "0.1.0"

# Parse version safely
try:
    # Only support plain semantic versions (no pre-release or build metadata)
    _parts = __version__.split(".")
    if len(_parts) != 3 or not all(p.isdigit() for p in _parts):
        raise ValueError("Version must be in format MAJOR.MINOR.PATCH with numeric values")
    __version_info__ = tuple(int(x) for x in _parts)
except (ValueError, AttributeError) as e:
    raise ValueError(f"Invalid version format '{__version__}': {e}")

# Semantic Versioning (SemVer) components
MAJOR = __version_info__[0]
MINOR = __version_info__[1]
PATCH = __version_info__[2]
