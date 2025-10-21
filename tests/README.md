# Testing Documentation

This directory contains the test suite for the gev-ai project.

## Running Tests

To run all tests:
```bash
poetry run pytest
```

To run tests with verbose output:
```bash
poetry run pytest -v
```

To run specific test files:
```bash
poetry run pytest tests/test_interfaces.py
poetry run pytest tests/test_settings.py
```

To run tests with coverage:
```bash
poetry run pytest --cov=gev_ai --cov-report=html
```

## Test Structure

- `conftest.py` - Shared pytest configuration and fixtures
- `test_interfaces.py` - Tests for the Tool interface and abstract base classes
- `test_settings.py` - Tests for the Settings configuration
- `test_todo.py.disabled` - Original todo tests (disabled due to import issues to be fixed later)

## Test Organization

Tests are organized by module and follow these conventions:
- Test files are named `test_*.py`
- Test classes are named `Test*`
- Test functions are named `test_*`

## Test Markers

The following test markers are available:
- `@pytest.mark.unit` - Unit tests that test individual components
- `@pytest.mark.integration` - Integration tests that test multiple components together

Use markers like this:
```python
@pytest.mark.unit
def test_something():
    pass
```

Run only unit tests:
```bash
poetry run pytest -m unit
```

## Writing Tests

When writing new tests:
1. Follow the existing naming conventions
2. Use descriptive test names that explain what is being tested
3. Keep tests focused on a single behavior
4. Use appropriate markers to categorize tests
5. Add docstrings to test classes and functions

## Future Improvements

- Add integration tests for database operations once import issues are resolved
- Add tests for the orchestrator and agent functionality
- Add coverage reporting to CI/CD pipeline
- Add performance/load tests for critical paths
