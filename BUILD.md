# Build & Distribution Guide

This guide covers building, packaging, and distributing the Tycoon Engine.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Building Executables](#building-executables)
- [Version Management](#version-management)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Creating Releases](#creating-releases)
- [Asset Management](#asset-management)

## Prerequisites

### Python Environment

- Python 3.8 or higher
- pip package manager

### Install Build Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-build.txt

# Or install the package with build extras
pip install -e ".[build]"
```

## Building Executables

### Windows Executable

To build a standalone Windows executable using PyInstaller:

```bash
python build_tools/build_exe.py
```

The executable will be created in the `dist/` directory with the naming format:
```
LemonadeStandTycoon-v{VERSION}.exe
```

### Build Options

The build script automatically:
- Packages all Python dependencies
- Includes the tycoon_engine module
- Bundles any assets found in `assets/` or `examples/demo_tycoon/assets/`
- Creates a single-file executable with no console window
- Names the executable with the current version

### Cleaning Build Artifacts

To remove build artifacts and start fresh:

```bash
python build_tools/build_exe.py --clean
```

This removes:
- `build/` directory
- `dist/` directory
- `*.spec` files
- `__pycache__/` directories

## Version Management

The project uses **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

### Current Version

The version is centralized in `tycoon_engine/version.py`:

```python
__version__ = "0.1.0"
```

### Bumping the Version

Use the version bump script to update versions across all files:

```bash
# Bump patch version (0.1.0 -> 0.1.1)
python build_tools/bump_version.py patch

# Bump minor version (0.1.0 -> 0.2.0)
python build_tools/bump_version.py minor

# Bump major version (0.1.0 -> 1.0.0)
python build_tools/bump_version.py major
```

The script automatically updates:
- `tycoon_engine/version.py`
- `pyproject.toml`

After bumping, commit the changes and create a git tag:

```bash
# Review changes
git diff

# Commit version bump
git add .
git commit -m "Bump version to 0.2.0"

# Create and push tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin main
git push origin v0.2.0
```

## GitHub Actions Workflow

The project includes a GitHub Actions workflow (`.github/workflows/build.yml`) that automates building and releasing.

### Workflow Triggers

The workflow runs on:

1. **Push to main branch**: Builds and uploads artifacts (no release)
2. **Pull requests**: Validates that the build succeeds
3. **Version tags** (v*.*.*): Builds and creates a GitHub Release
4. **Manual trigger**: Can be run via GitHub Actions UI

### Workflow Jobs

#### Build Job

- Runs on Windows
- Installs Python dependencies
- Builds Windows executable
- Uploads artifact to GitHub (30-day retention)

#### Release Job

- Runs only for version tags (e.g., `v0.1.0`)
- Downloads build artifacts
- Creates a GitHub Release
- Attaches executable files
- Marks alpha/beta/rc versions as pre-releases

### Viewing Build Artifacts

For non-release builds, artifacts are available in the GitHub Actions run:

1. Go to the repository's **Actions** tab
2. Click on the workflow run
3. Scroll to **Artifacts** section
4. Download the artifact

## Creating Releases

### Automatic Releases (Recommended)

1. Bump the version:
   ```bash
   python build_tools/bump_version.py minor
   ```

2. Commit and create tag:
   ```bash
   git add .
   git commit -m "Bump version to 0.2.0"
   git tag -a v0.2.0 -m "Release v0.2.0"
   ```

3. Push to GitHub:
   ```bash
   git push origin main
   git push origin v0.2.0
   ```

4. GitHub Actions will automatically:
   - Build the executable
   - Create a GitHub Release
   - Attach the executable to the release

### Manual Releases

If you need to create a release manually:

1. Build the executable:
   ```bash
   python build_tools/build_exe.py
   ```

2. Go to your GitHub repository
3. Click **Releases** → **Create a new release**
4. Choose or create a tag (e.g., `v0.2.0`)
5. Fill in release title and description
6. Upload the executable from `dist/`
7. Publish the release

## Asset Management

### Including Assets in Builds

The build script automatically includes assets from:

- `assets/` (root directory)
- `examples/demo_tycoon/assets/` (demo-specific)

Assets are bundled into the executable and accessible at runtime.

### Adding New Assets

1. Place assets in one of the asset directories
2. Access them in code using relative paths
3. The build script will automatically include them

### Asset Types Supported

- Images: `.png`, `.jpg`, `.bmp`
- Fonts: `.ttf`, `.otf`
- Audio: `.wav`, `.mp3`, `.ogg`
- Data: `.json`, `.yaml`, `.txt`

## Troubleshooting

### Build Fails with "PyInstaller not found"

Install build dependencies:
```bash
pip install -r requirements-build.txt
```

### Executable Won't Run

Try building with console window for debugging:
1. Edit `build_tools/build_exe.py`
2. Change `--windowed` to `--console`
3. Rebuild and check console output

### Missing Assets in Built Executable

1. Verify assets exist in `assets/` directories
2. Check console output during build
3. Ensure paths are correct in your code

### Version Mismatch

After bumping version, ensure:
1. `tycoon_engine/version.py` is updated
2. `pyproject.toml` is updated
3. Changes are committed before tagging

## Best Practices

1. **Always test builds locally** before pushing tags
2. **Update CHANGELOG.md** before creating releases
3. **Use semantic versioning** consistently
4. **Test executables** on clean Windows machines
5. **Keep dependencies updated** but test thoroughly
6. **Document breaking changes** in release notes

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Releases Guide](https://docs.github.com/en/repositories/releasing-projects-on-github)
