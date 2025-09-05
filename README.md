# Hangman Game - TDD Implementation

A Python implementation of the classic Hangman word guessing game, developed using Test-Driven Development (TDD) methodology with comprehensive unit testing.

## Features

- **Two Difficulty Levels**:
  - Basic: Single word guessing
  - Intermediate: Phrase guessing with spaces
- **Timer Functionality**: 15-second countdown per guess
- **Life System**: 6 lives with visual hangman drawing
- **Input Validation**: Comprehensive error handling
- **Dictionary Support**: Customizable word/phrase lists

## Requirements

- Python 3.8+
- pytest 7.4.3
- pytest-cov 4.1.0
- flake8 6.1.0

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/EchoKe26/hangman-tdd-assignment.git
   cd hangman-tdd-assignment
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the game:
```bash
python src/hangman.py
```

Run tests:
```bash
python -m pytest tests/ -v
```

Run tests with coverage:
```bash
python -m pytest tests/ -v --cov=src --cov-report=html
```

Check code quality:
```bash
flake8 src/ tests/ --max-line-length=100
```

## Project Structure

```
├── src/
│   ├── __init__.py
│   └── hangman.py          # Main game implementation
├── tests/
│   ├── __init__.py
│   └── test_hangman.py     # Comprehensive test suite
├── data/
│   ├── words.txt           # Word dictionary for basic level
│   └── phrases.txt         # Phrase dictionary for intermediate level
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── Software_Unit_Testing_Report.md  # Detailed technical report
```

## Game Rules

1. Choose difficulty level (Basic or Intermediate)
2. Guess letters to reveal the hidden word/phrase
3. You have 15 seconds per guess
4. You have 6 lives total
5. Wrong guesses cost one life
6. Win by guessing all letters before running out of lives or time
7. Spaces and punctuation are revealed automatically in intermediate mode

## Development

This project was developed using Test-Driven Development (TDD):

1. **Red Phase**: Write failing tests first
2. **Green Phase**: Write minimal code to pass tests
3. **Refactor Phase**: Improve code while maintaining test coverage

### Test Coverage

Current test coverage: 71% (25 test cases)

Key test categories:
- Game initialization and configuration
- Dictionary loading and word/phrase selection
- Guess validation and processing
- Game state management (win/loss/timeout)
- Timer functionality
- Display formatting
- Error handling

## Contributing

1. Follow TDD principles
2. Maintain code quality (flake8 compliance)
3. Ensure test coverage for new features
4. Update documentation as needed

## License

Educational project for PRT582 Software Unit Testing course.