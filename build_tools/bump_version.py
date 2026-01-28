#!/usr/bin/env python3
"""
Version bumping script for Tycoon Engine.

This script helps manage semantic versioning (SemVer) for the project.
It updates version information in tycoon_engine/version.py and pyproject.toml.

Usage:
    python build_tools/bump_version.py major  # 0.1.0 -> 1.0.0
    python build_tools/bump_version.py minor  # 0.1.0 -> 0.2.0
    python build_tools/bump_version.py patch  # 0.1.0 -> 0.1.1
"""

import sys
import re
from pathlib import Path


def get_current_version(version_file):
    """Extract current version from version.py."""
    try:
        content = version_file.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Version file not found: {version_file}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading: {version_file}")
    
    match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        raise ValueError("Could not find version in version.py")
    return tuple(int(x) for x in match.groups())


def bump_version(version, bump_type):
    """Bump version based on type (major, minor, patch)."""
    major, minor, patch = version
    
    if bump_type == "major":
        return (major + 1, 0, 0)
    elif bump_type == "minor":
        return (major, minor + 1, 0)
    elif bump_type == "patch":
        return (major, minor, patch + 1)
    else:
        raise ValueError(f"Invalid bump type: {bump_type}. Use 'major', 'minor', or 'patch'")


def update_version_file(version_file, new_version):
    """Update version.py with new version."""
    version_str = ".".join(str(x) for x in new_version)
    try:
        content = version_file.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Version file not found: {version_file}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading: {version_file}")
    
    # Update __version__
    content = re.sub(
        r'__version__\s*=\s*"[^"]*"',
        f'__version__ = "{version_str}"',
        content
    )
    
    try:
        version_file.write_text(content, encoding='utf-8')
    except PermissionError:
        raise PermissionError(f"Permission denied writing: {version_file}")
    
    print(f"✓ Updated {version_file.name}")


def update_pyproject_toml(pyproject_file, new_version):
    """Update pyproject.toml with new version."""
    version_str = ".".join(str(x) for x in new_version)
    try:
        content = pyproject_file.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"pyproject.toml not found: {pyproject_file}")
    except PermissionError:
        raise PermissionError(f"Permission denied reading: {pyproject_file}")
    
    # Update version line in [project] section
    # More specific pattern to match only the project version
    content = re.sub(
        r'(\[project\].*?version\s*=\s*)"[^"]*"',
        r'\1"' + version_str + '"',
        content,
        flags=re.DOTALL
    )
    
    try:
        pyproject_file.write_text(content, encoding='utf-8')
    except PermissionError:
        raise PermissionError(f"Permission denied writing: {pyproject_file}")
    
    print(f"✓ Updated {pyproject_file.name}")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("major", "minor", "patch"):
        print(__doc__)
        sys.exit(1)
    
    bump_type = sys.argv[1]
    
    # Get project root
    project_root = Path(__file__).parent.parent
    version_file = project_root / "tycoon_engine" / "version.py"
    pyproject_file = project_root / "pyproject.toml"
    
    try:
        # Get current version
        current_version = get_current_version(version_file)
        current_str = ".".join(str(x) for x in current_version)
        
        # Bump version
        new_version = bump_version(current_version, bump_type)
        new_str = ".".join(str(x) for x in new_version)
        
        print(f"\nBumping version ({bump_type}):")
        print(f"  {current_str} -> {new_str}")
        print()
        
        # Update files
        update_version_file(version_file, new_version)
        update_pyproject_toml(pyproject_file, new_version)
        
        print(f"\n✓ Version bumped to {new_str}")
        print("\nNext steps:")
        print("  1. Review the changes: git diff")
        print("  2. Commit the changes: git add . && git commit -m 'Bump version to {}'".format(new_str))
        print("  3. Create a tag: git tag -a v{} -m 'Release v{}'".format(new_str, new_str))
        print("  4. Push changes: git push && git push --tags")
    
    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
