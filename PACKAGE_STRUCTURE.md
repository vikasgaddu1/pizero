# Package Structure

This project has been refactored into a proper Python package for better maintainability and modularity.

## Directory Structure

```
pizero/
├── pizero/                    # Main package
│   ├── __init__.py           # Package exports
│   ├── config.py             # Configuration class
│   ├── image.py              # Image optimization utilities
│   ├── assistant.py          # VisionAssistant class
│   └── cli.py                # CLI entry point
├── tests/
│   ├── __init__.py
│   └── test_simulation.py    # Simulation tests
├── scripts/
│   ├── check_environment.py  # Environment validation
│   └── validate_code.py      # Code validation
├── main.py                    # Backward compatibility wrapper
├── setup.py                   # Package installation (legacy)
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Dependencies
├── MANIFEST.in               # Package distribution files
└── README.md                 # Project documentation
```

## Module Overview

### pizero/config.py
Contains the `Config` class with all application settings:
- API settings (Gemini API key, model)
- Image settings (size, quality)
- Camera settings (resolution, warmup time)
- Voice recognition settings (keyword, exit keywords)
- Text-to-speech settings (rate, volume)

### pizero/image.py
Contains the `ImageOptimizer` class for efficient image processing:
- Resize images while maintaining aspect ratio
- Convert to JPEG with optimized compression
- Handle different image formats (RGBA, LA, P)

### pizero/assistant.py
Contains the `VisionAssistant` class - the main application logic:
- Camera initialization and capture
- Text-to-speech integration
- Gemini API integration
- Voice recognition
- Command processing
- Dynamic prompt building based on user requests

### pizero/cli.py
Command-line interface entry point:
- Main function to start the application
- Error handling and user guidance

## Usage

### As a Package

After installation with `pip install -e .`, you can:

```python
from pizero import Config, VisionAssistant, ImageOptimizer

# Create configuration
config = Config()

# Create and run assistant
assistant = VisionAssistant(config)
assistant.run()
```

### Using the CLI

After installation, run from anywhere:

```bash
pizero-vision
```

### Backward Compatibility

The original `main.py` still works for existing deployments:

```bash
python3 main.py
```

## Installation

### Development Installation

Install in editable mode with all dependencies:

```bash
pip3 install -e .
```

### With Raspberry Pi Hardware Support

```bash
pip3 install -e ".[pi]"
```

### For Development

```bash
pip3 install -e ".[dev]"
```

## Testing

### Validate Code

```bash
python3 scripts/validate_code.py
```

### Run Simulation Test

```bash
python3 tests/test_simulation.py
```

## Benefits of the Package Structure

1. **Separation of Concerns**: Each module has a single responsibility
2. **Easier Testing**: Import and test individual components
3. **Better Maintainability**: Smaller, focused files are easier to understand
4. **Installable**: Can be installed with pip and used anywhere
5. **Backward Compatible**: Existing deployments continue to work
6. **Modern Standards**: Uses pyproject.toml for packaging
7. **Clear Organization**: Tests and scripts are in separate directories

## Migration Guide

If you have existing code that imports from `main.py`:

### Before
```python
from main import Config, VisionAssistant, ImageOptimizer
```

### After
```python
from pizero import Config, VisionAssistant, ImageOptimizer
```

The old import style still works due to the backward compatibility wrapper in `main.py`.
