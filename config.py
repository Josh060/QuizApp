# config.py
import json
import logging
from typing import Dict, List

class Config:
    # Application constants
    APP_TITLE = "Quiz App"
    USERNAME_LABEL_TEXT = "Username:"
    START_BUTTON_TEXT = "Start Quiz"
    RESTART_BUTTON_TEXT = "Restart App"
    ADMIN_BUTTON_TEXT = "Admin Mode"
    LANGUAGE_SELECTION_TITLE = "Select Language"
    CHOOSE_LANGUAGE_TEXT = "Choose a Language:"

    # Error messages
    USERNAME_ERROR_EMPTY = "Please enter a valid username."
    USERNAME_ERROR_LENGTH = "Username must be 1-20 characters long"
    USERNAME_ERROR_CHARS = "Only alphanumeric characters and _- are allowed"
    NO_QUESTIONS_ERROR = "No questions found for '{language}'."
    DATABASE_ERROR = "Database connection failed after {attempts} attempts"

    # Default configuration
    DEFAULT_CONFIG = {
        "languages": ["Python", "Java", "Cpp", "JavaScript"],
        "max_username_length": 20,
        "fullscreen": True,
        "enable_logging": True,
        "log_file": "quiz_app.log"
    }

    # UI Strings for easy localization or changes
    # In config.py
    UI_STRINGS = {
        "previous_button": "Previous",
        "next_button": "Next",
        "question_label": "Question {current}/{total}",
        "time_left": "⏱ Time left: {time}s",  # Correct placeholder
        "timeout_message": "Time's up!",
        "end_quiz_message": "Quiz Completed!",
        "play_again_message": "Do you want to play again?",
        "quit_message": "Are you sure you want to quit the quiz?"
    }

    @classmethod
    def load_config(cls) -> Dict:
        try:
            with open("config.json", "r") as f:
                user_config = json.load(f)
                return {**cls.DEFAULT_CONFIG, **user_config}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Using default config: {e}")
            return cls.DEFAULT_CONFIG

    @classmethod
    def get_languages(cls) -> List[str]:
        config = cls.load_config()
        return config.get("languages", cls.DEFAULT_CONFIG["languages"])
