"""
Configuration settings for the DHS IA Exam Bot
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Database configuration
DATABASE_PATH = PROJECT_ROOT / "data" / "dhs_bot.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Application settings
APP_NAME = "DHS IA Exam Bot"
APP_VERSION = "1.0.0"
DEBUG_MODE = True

# Exam configuration
IA_EXAM_CONFIG = {
    "min_passing_score": 70,
    "max_attempts": 3,
    "time_limit_minutes": 120,
    "total_questions": 50
}

# Application states
APPLICATION_STATES = [
    "DRAFT",
    "SUBMITTED",
    "UNDER_REVIEW",
    "APPROVED",
    "REJECTED",
    "PENDING_EXAM"
]

# Exam categories
EXAM_CATEGORIES = [
    "Security Fundamentals",
    "Network Security",
    "Cryptography",
    "Access Control",
    "Incident Response"
]

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "logs" / "dhs_bot.log"

# Create necessary directories
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
