# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions workflow for automated building and packaging
- PyInstaller script for creating Windows executables
- Version management with SemVer strategy
- Build documentation (BUILD.md)
- Version bumping script
- Centralized version management in `tycoon_engine/version.py`

### Changed
- Updated build_exe.py to include assets and use version information
- Enhanced README with build instructions

## [0.1.0] - 2024-01-28

### Added
- Initial release of Tycoon Engine
- Core game engine with pygame
- State management system
- Entity and resource management
- Multiplayer support via Socket.IO
- UI components and rendering
- Demo tycoon game (Lemonade Stand)
- Basic build tools
- Comprehensive documentation

[Unreleased]: https://github.com/brunobritorj/python-tycoon/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/brunobritorj/python-tycoon/releases/tag/v0.1.0
