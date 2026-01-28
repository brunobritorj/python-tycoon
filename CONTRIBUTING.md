# Contributing to Python Tycoon Engine

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/python-tycoon.git
cd python-tycoon
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements-dev.txt
pip install -e .
```

### 4. Verify Setup
```bash
# Run tests
pytest

# Run demo game
python -m examples.demo_tycoon.main
```

## Development Workflow

### Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new functionality

3. **Test Your Changes**
   ```bash
   # Run tests
   pytest
   
   # Check coverage
   pytest --cov=tycoon_engine
   
   # Format code
   black .
   
   # Lint code
   flake8 tycoon_engine/
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/my-new-feature
   ```

5. **Open Pull Request**
   - Go to GitHub and create a PR
   - Describe your changes
   - Link any related issues

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use black for formatting (line length: 100)
- Use type hints
- Write docstrings for all public APIs

### Example
```python
def calculate_profit(revenue: float, costs: float) -> float:
    """
    Calculate profit from revenue and costs.
    
    Args:
        revenue: Total revenue in dollars
        costs: Total costs in dollars
        
    Returns:
        Profit (revenue - costs)
    """
    return revenue - costs
```

### Documentation
- Use Google-style docstrings
- Document all parameters and return values
- Include usage examples for complex functions

## Testing Guidelines

### Writing Tests
- Create test files in `tests/` directory
- Name files `test_*.py`
- Use descriptive test names
- Test edge cases and error conditions

### Example Test
```python
def test_resource_manager_add_money():
    """Test adding money to resource manager."""
    rm = ResourceManager(starting_money=100)
    rm.add_money(50)
    assert rm.get_money() == 150
```

### Running Tests
```bash
# All tests
pytest

# Specific file
pytest tests/test_config.py

# With coverage
pytest --cov=tycoon_engine --cov-report=html

# Verbose
pytest -v
```

## What to Contribute

### High Priority
- Additional example games
- More UI components
- Improved test coverage
- Performance optimizations
- Documentation improvements

### Ideas
- Save/load system
- Audio integration
- Advanced entity behaviors
- Camera system with zoom/pan
- Animation system
- Particle effects
- Path finding
- Localization support

### Bug Fixes
- Always welcome!
- Include tests that reproduce the bug
- Explain the fix in PR description

## Reporting Issues

### Bug Reports
Include:
- Python version
- OS and version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

### Feature Requests
Include:
- Use case description
- Proposed API/interface
- Examples of how it would be used
- Why it's useful for tycoon games

## Code Review Process

### What We Look For
- **Functionality**: Does it work as intended?
- **Tests**: Are there tests that cover the changes?
- **Documentation**: Is it documented properly?
- **Style**: Does it follow code style guidelines?
- **Performance**: Is it reasonably efficient?
- **Security**: Are there any security concerns?

### Review Timeline
- Initial review within 1-3 days
- Follow-up reviews within 1-2 days
- Merge after approval and CI passes

## Building Documentation

### API Documentation
Update `docs/API.md` when adding/changing public APIs.

### Tutorial
Update `docs/TUTORIAL.md` if adding new concepts.

### README
Update `README.md` for major features.

## Release Process

### Version Numbering
We use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Creating a Release
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build and test
5. Create GitHub release

## Community Guidelines

### Be Respectful
- Be kind and respectful
- Welcome newcomers
- Provide constructive feedback
- Assume good intentions

### Communication
- Use GitHub Issues for bugs/features
- Use Pull Requests for code
- Be clear and concise
- Provide context and examples

## Questions?

- Check existing documentation
- Search existing issues
- Open a new issue if needed
- Tag with "question" label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!
