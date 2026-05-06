# Contributing to AutoShip

Thank you for your interest in contributing to AutoShip! We appreciate your efforts to help improve this project.

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Docker and Docker Compose (optional)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/AutoShip.git
   cd AutoShip
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black pylint flake8
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Standards

We follow PEP 8 and use the following tools:

- **pylint**: Python code quality
  ```bash
  pylint app/
  ```

- **black**: Code formatting
  ```bash
  black app/
  ```

- **flake8**: Style guide enforcement
  ```bash
  flake8 app/
  ```

### Commit Messages

Write clear, descriptive commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add code analysis caching for performance improvement

- Implement Redis-based result caching
- Reduce database queries by 40%
- Add cache invalidation on updates

Fixes #123
```

### Pull Request Process

1. **Before submitting:**
   - Ensure code passes all linting checks
   - Write or update tests for new functionality
   - Update documentation as needed
   - Run the full test suite

2. **Submit your PR:**
   - Provide a clear description of changes
   - Reference related issues
   - Include screenshots for UI changes
   - Ensure CI/CD checks pass

3. **Address feedback:**
   - Respond to review comments
   - Make requested changes
   - Request re-review after updates

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in a `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test names: `test_should_calculate_average_score`
- Include docstrings explaining test purpose

Example:
```python
def test_health_check_endpoint():
    """Verify health check endpoint returns ok status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

## Documentation

### Code Comments

- Use docstrings for all functions and classes
- Follow Google-style docstring format
- Explain the "why", not just the "what"

Example:
```python
def analyze_code(code: str) -> dict:
    """
    Analyze Python code quality using pylint.
    
    Args:
        code: Python source code as string
        
    Returns:
        Dictionary containing:
        - score: Float between 0-10
        - issues: List of identified issues
        - is_pass: Boolean indicating pass/fail
        
    Raises:
        ValueError: If code cannot be parsed
    """
```

### Updating Documentation

- Keep README.md up to date
- Update CONTRIBUTING.md if contribution process changes
- Add changelog entries in CHANGELOG.md (if exists)
- Update technical documentation in report.tex

## Reporting Bugs

Before creating a bug report, check existing issues to avoid duplicates.

When creating an issue, include:

- **Clear title**: Specific and descriptive
- **Environment**: OS, Python version, relevant versions
- **Steps to reproduce**: Detailed, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: For UI-related bugs
- **Error messages**: Full error trace if applicable

Example:
```markdown
**Title**: Dashboard fails to load with 500 error

**Environment**:
- OS: Ubuntu 20.04
- Python: 3.9.2
- FastAPI: 0.115.0

**Steps to Reproduce**:
1. Start AutoShip
2. Navigate to http://localhost:8000
3. Wait 5 seconds

**Expected**: Dashboard loads successfully
**Actual**: Error 500 appears

**Error**:
```
SQLAlchemy error: connection refused
```
```

## Feature Requests

Suggest new features by opening an issue with:

- **Clear title**: Descriptive feature name
- **Motivation**: Why this feature is needed
- **Proposed solution**: How you envision it working
- **Alternatives**: Other approaches considered
- **Additional context**: Mockups, examples, etc.

## Security

### Reporting Security Issues

**Do not** report security vulnerabilities in public issues. Instead:

1. Email security details to: [maintainer-email]
2. Include proof of concept if possible
3. Allow 90 days for fix before disclosure

## Review Process

A maintainer will review your PR within a few days. The review may:

- Request changes for alignment with project goals
- Suggest improvements for code quality
- Ask for additional tests or documentation
- Require updates for consistency

Be responsive and open to feedback.

## Merge Approval

PRs are approved when they:

- ✅ Pass all automated checks
- ✅ Have at least one maintainer approval
- ✅ Have no unresolved conversations
- ✅ Are up to date with main branch
- ✅ Include appropriate documentation

## Deployment

After merge to main, deployment happens via:

1. Automated CI/CD pipeline
2. Docker image build
3. Testing in staging environment
4. Production release

Maintainers have access to deployment tools.

## Project Structure Best Practices

When adding new features:

- Keep modules focused and single-purpose
- Add new files under appropriate directories
- Update imports in `__init__.py` files
- Follow existing naming conventions
- Document module purposes in docstrings

## Performance Considerations

When contributing, consider:

- Database query efficiency
- API response times
- Frontend load times
- Memory usage for large datasets
- Caching opportunities

Profile code before and after changes:

```bash
python -m cProfile -s cumtime app/main.py
```

## Questions?

- Check existing documentation
- Search closed issues for answers
- Open a discussion issue
- Reach out to maintainers

## Recognition

Contributors are recognized in:

- README.md Contributors section
- Release notes for significant contributions
- GitHub contributor statistics

Thank you for contributing to AutoShip! 🚀
