"""Application configuration and path constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

APP_TITLE = "SpielWelt – ErsteKinderApp"
APP_VERSION = "1.0.0"
