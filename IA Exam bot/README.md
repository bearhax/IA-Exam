# DHS Application Bot for IA Exam

A comprehensive bot application for managing DHS applications and conducting IA (Information Assurance) examinations.

## Features

- User application management
- IA exam testing and scoring
- Application status tracking
- Test result analysis
- Data validation and processing

## Project Structure

```
├── src/
│   ├── main.py              # Main application entry point
│   ├── bot.py               # Core bot logic
│   ├── exam.py              # IA exam management
│   ├── application.py       # Application management
│   ├── database.py          # Database operations
│   └── utils.py             # Utility functions
├── config/
│   └── settings.py          # Configuration settings
├── tests/
│   ├── test_bot.py          # Bot tests
│   ├── test_exam.py         # Exam tests
│   └── test_application.py  # Application tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure settings in `config/settings.py`

## Usage

Run the bot:
```bash
python src/main.py
```

## Testing

Run tests:
```bash
python -m pytest tests/
```

## License

© DHS 2025
