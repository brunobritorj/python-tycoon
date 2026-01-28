"""
Build script for creating Windows EXE using PyInstaller.

Usage:
    python build_tools/build_exe.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


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
    
    print("Building Windows EXE with PyInstaller...")
    print(f"Main script: {main_script}")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (use --console for debugging)
        "--name", "LemonadeStandTycoon",
        "--add-data", f"{project_root / 'tycoon_engine'}{os.pathsep}tycoon_engine",
        str(main_script)
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, cwd=project_root, check=True)
        
        print("\n" + "="*50)
        print("Build completed successfully!")
        print(f"Executable location: {dist_dir / 'LemonadeStandTycoon.exe'}")
        print("="*50)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False
    except FileNotFoundError:
        print("Error: PyInstaller not found. Install it with:")
        print("  pip install pyinstaller")
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
