# Contributing to MIDI Pushover Notifier

First off, thank you for considering contributing to MIDI Pushover Notifier! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your system information:**
  - macOS version
  - Python version
  - MIDI controller model
  - Any error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure your code follows the existing style
4. Make sure your code lints
5. Write a clear commit message

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/midi-pushover-notifier.git
   cd midi-pushover-notifier
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app in development mode:
   ```bash
   python3 src/midi_pushover_notifier.py
   ```

## Code Style

- Follow PEP 8
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused
- Document all functions with docstrings

## Testing

Before submitting a pull request:

1. Test with different MIDI controllers if possible
2. Verify all menu items work correctly
3. Test MIDI mapping functionality
4. Ensure notifications are sent properly
5. Test on different macOS versions if possible

## Project Structure

```
src/
├── midi_pushover_notifier.py   # Main application
assets/
├── logo.icns                   # Application icon
build/
├── setup.py                    # Build configuration
├── build_app.sh               # Build script
```

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎹
