# Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/brunobritorj/python-tycoon.git
cd python-tycoon
```

### 2. Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

**For Users (Run Games):**
```bash
pip install -r requirements.txt
```

**For Developers (Development & Testing):**
```bash
pip install -r requirements-dev.txt
```

**For Building Executables:**
```bash
pip install -r requirements-build.txt
```

### 4. Install the Package

**As Editable Package (for development):**
```bash
pip install -e .
```

**As Regular Package:**
```bash
pip install .
```

## Running the Demo Game

### Method 1: Using the Installed Command
```bash
tycoon-demo
```

### Method 2: Using Python Module
```bash
python -m examples.demo_tycoon.main
```

### Method 3: Direct Execution
```bash
python examples/demo_tycoon/main.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=tycoon_engine

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v
```

## Building an Executable

### Build Windows EXE

1. Install build dependencies:
```bash
pip install -r requirements-build.txt
```

2. Run the build script:
```bash
python build_tools/build_exe.py
```

3. Find the executable in the `dist/` directory

### Clean Build Artifacts

```bash
python build_tools/build_exe.py --clean
```

## Running the Multiplayer Server

### Method 1: Using the Installed Command
```bash
# Default (localhost:5000)
tycoon-server

# Custom host and port
tycoon-server --host 0.0.0.0 --port 8080
```

### Method 2: Using Python Module
```bash
python -m tycoon_engine.networking.server --host localhost --port 5000
```

## Project Structure Overview

```
python-tycoon/
├── tycoon_engine/              # Core game engine
│   ├── core/                   # Game loop, states, config
│   ├── networking/             # Multiplayer (server/client)
│   ├── entities/               # Entity & resource management
│   ├── ui/                     # UI rendering utilities
│   └── utils/                  # Helper functions
├── examples/
│   └── demo_tycoon/            # Demo lemonade stand game
├── build_tools/                # Build scripts
├── tests/                      # Unit tests
├── docs/                       # Documentation
│   ├── API.md                  # API reference
│   └── TUTORIAL.md             # Tutorial
├── pyproject.toml              # Package configuration
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Development dependencies
├── requirements-build.txt      # Build dependencies
└── README.md                   # Main documentation
```

## Troubleshooting

### pygame Issues

**Linux:**
If you get display errors, make sure you have the required system libraries:
```bash
sudo apt-get install python3-pygame
```

**macOS:**
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

### Import Errors

If you get import errors, make sure the package is installed:
```bash
pip install -e .
```

### Build Issues

If PyInstaller fails, try:
1. Update PyInstaller: `pip install --upgrade pyinstaller`
2. Clear cache: `python build_tools/build_exe.py --clean`
3. Check for conflicting dependencies

## Development Workflow

### 1. Set Up Development Environment
```bash
git clone https://github.com/brunobritorj/python-tycoon.git
cd python-tycoon
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
pip install -e .
```

### 2. Make Changes
Edit the code in `tycoon_engine/` or `examples/`

### 3. Run Tests
```bash
pytest
```

### 4. Format Code
```bash
black .
```

### 5. Lint Code
```bash
flake8 tycoon_engine/
```

### 6. Test Your Changes
```bash
python -m examples.demo_tycoon.main
```

## Getting Help

- Check the [API Documentation](docs/API.md)
- Read the [Tutorial](docs/TUTORIAL.md)
- Review the demo game in `examples/demo_tycoon/`
- Open an issue on GitHub for bugs or questions

## Next Steps

1. **Learn the basics**: Read the [Tutorial](docs/TUTORIAL.md)
2. **Explore the API**: Check [API Documentation](docs/API.md)
3. **Build your game**: Start with the demo and customize it
4. **Add multiplayer**: Enable networking and run the server
5. **Package your game**: Build an executable with PyInstaller
