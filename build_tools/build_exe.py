"""
Build script for creating Windows EXE using PyInstaller.

This script packages the Tycoon Engine demo game as a standalone Windows executable
with all necessary dependencies and assets included.

Usage:
    python build_tools/build_exe.py
    python build_tools/build_exe.py --clean  # Clean build artifacts
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Add parent directory to path to import version
sys.path.insert(0, str(Path(__file__).parent.parent))
from tycoon_engine.version import __version__


def build_exe():
    """Build the game as a Windows executable."""
    
    # Get project root
    project_root = Path(__file__).parent.parent
    
    # Paths
    main_script = project_root / "examples" / "demo_tycoon" / "main.py"
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    if not main_script.exists():
        print(f"Error: Main script not found at {main_script}")
        return False
    
    print(f"Building Windows EXE with PyInstaller (v{__version__})...")
    print(f"Main script: {main_script}")
    
    # Build PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (use --console for debugging)
        "--name", f"LemonadeStandTycoon-v{__version__}",
        "--add-data", f"{project_root / 'tycoon_engine'}{os.pathsep}tycoon_engine",
    ]
    
    # Check for assets directories and include them
    assets_dirs = [
        project_root / "assets",
        project_root / "examples" / "demo_tycoon" / "assets",
    ]
    
    for assets_dir in assets_dirs:
        if assets_dir.exists():
            print(f"Including assets from: {assets_dir}")
            cmd.extend(["--add-data", f"{assets_dir}{os.pathsep}assets"])
    
    # Add the main script as the last argument
    cmd.append(str(main_script))
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, cwd=project_root, check=True)
        
        print("\n" + "="*60)
        print("Build completed successfully!")
        print(f"Version: {__version__}")
        print(f"Executable location: {dist_dir / f'LemonadeStandTycoon-v{__version__}.exe'}")
        print("="*60)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False
    except FileNotFoundError:
        print("Error: PyInstaller not found. Install it with:")
        print("  pip install pyinstaller")
        print("Or:")
        print("  pip install -r requirements-build.txt")
        return False


def clean_build():
    """Clean build artifacts."""
    project_root = Path(__file__).parent.parent
    
    dirs_to_clean = [
        project_root / "build",
        project_root / "dist",
        project_root / "__pycache__"
    ]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            print(f"Removing {dir_path}")
            shutil.rmtree(dir_path)
    
    # Remove spec files
    for spec_file in project_root.glob("*.spec"):
        print(f"Removing {spec_file}")
        spec_file.unlink()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build game executable")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    
    args = parser.parse_args()
    
    if args.clean:
        clean_build()
    else:
        build_exe()
