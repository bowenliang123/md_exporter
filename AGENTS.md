# Agent Coding Guidelines for md-exporter

This document provides essential information for agentic coding agents working in the md-exporter repository.

## 🔧 Build, Lint, and Test Commands

### Package Management
- **Primary**: `uv` package manager is used for dependency management
- **Fallback**: `pip` if `uv` is not available
- **Python Requirement**: Python 3.11 or higher required

### Code Quality and Formatting

#### Lint and Format Code
```bash
# Alternative: Run from project root using provided script
./dev.reformat.sh
```

#### Run Tests
```bash
# Run all tests
test/bin/run_all_tests.sh 

# Run specific test file
test/bin/test_md_to_docx.sh 

or

uv run pytest test/skills/test_md_to_docx.py
```

### Development Scripts
- **Main CLI**: `scripts/md-exporter` (shell script wrapper)
- **Test Scripts**: Individual test scripts in `test/bin/`

## 📝 Code Style Guidelines

### Formatting and Style
- **Line Length**: 120 characters maximum
- **Line Ending**: LF (Unix-style)
- **Indentation**: 4 spaces (not tabs)
- **Quotes**: Use double quotes for strings unless single quotes are preferred for specific cases
- **End of File**: All files must end with newline character

### Python Style Standards

#### Import Organization
```python
# Standard library imports
from pathlib import Path
from tempfile import NamedTemporaryFile

# Third-party imports
from pypandoc import convert_file

# Local imports (relative paths)
from scripts.utils.markdown_utils import get_md_text
```

#### Type Hints and Annotations
- Use Python 3.11+ union syntax: `Path | None` (not `Optional[Path]`)
- All function parameters and return values should have type hints
- Use pathlib.Path for file paths, not strings

#### Function Documentation
```python
def convert_md_to_docx(
    md_text: str, output_path: Path, template_path: Path | None = None, is_strip_wrapper: bool = False
) -> None:
    """
    Convert Markdown text to DOCX format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output DOCX file
        template_path: Optional path to DOCX template file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
```

#### Naming Conventions
- **Files**: `snake_case.py` for Python files
- **Functions**: `snake_case()` for functions and methods
- **Classes**: `PascalCase` for classes
- **Constants**: `UPPER_SNAKE_CASE` for constants
- **Private Methods**: Prefix with single underscore `_private_method()`

### Error Handling
- Always handle exceptions properly, never use empty catch blocks
- Raise specific exceptions with descriptive messages
- Use context managers (`with` statements) for resource management
- Clean up temporary files in `finally` blocks

### Ruff Linting Rules
The project uses these ruff rules:
- **UP**: pyupgrade rules for modern Python features
- **I**: isort for import organization
- **E402**: Module level import not at top of file
- **F401**: Imported but unused

Configuration is in `.ruff.toml`.

## 📁 Project Structure

### Core Directories
- **`scripts/`**: Main entry points and core logic
  - `services/`: Conversion service modules (`svc_*.py`)
  - `parser/`: CLI parsers for each tool (`cli_*.py`)
  - `utils/`: Shared utility functions
- **`test/`**: Test files organized by functionality
  - `skills/`: Tests for each conversion tool
  - `bin/`: Shell script test runners
- **`assets/`**: Template files and static resources
  - `template/`: DOCX and PPTX template files

### Key Service Patterns
Each conversion tool follows this pattern:
- **Service**: `scripts/services/svc_md_to_X.py` - Core conversion logic
- **Parser**: `scripts/parser/cli_md_to_X.py` - CLI argument parsing
- **CLI**: `scripts/md-exporter X` - Shell script entry point
- **Test**: `test/skills/test_md_to_X.py` - Unit tests

### File Processing Patterns
- Use `pathlib.Path` for all file operations
- Implement proper cleanup for temporary files
- Support custom template files when available
- Handle both relative and absolute file paths correctly

## 🧪 Testing Guidelines

### Test Structure
- Tests extend `TestBase` class
- Use `run_script()` method for CLI testing
- Verify output files exist and are not empty
- Use descriptive test method names: `test_tool_name()`

### Test Data
- Input files are in `test/resources/`
- Output files should go to `test_output/`
- Each tool has corresponding test resources

### Running Individual Tests
```bash
# Run specific tool test
cd test/bin && ./test_md_to_html.sh

# Run with pytest directly
uv run pytest test/skills/test_md_to_docx.py -v
```

## 🚫 Important Constraints

1. **Python Version**: Always use Python 3.11+ features and syntax
2. **Package Manager**: Prefer `uv` over `pip` for development
3. **Path Handling**: Use `pathlib.Path` exclusively for file paths
4. **Error Handling**: Never suppress exceptions or use empty catch blocks
5. **Code Quality**: Always run `ruff check --fix` before committing
6. **Testing**: Run tests after any changes to ensure functionality

## 🔄 Development Workflow

1. Make changes following the code style guidelines
2. Run linting: `dev/reformat.sh`
3. Run tests: `test/bin/run_all_tests.sh`
4. Verify all tools still work correctly
5. Test individual tools via CLI scripts
