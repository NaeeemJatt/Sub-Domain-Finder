"""
Configuration settings for the Subdomain Finder application.
"""

# Application settings
APP_NAME = "Sub-Domain Finder"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Naeem Jatt"

# GUI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_X = 100
WINDOW_Y = 100

# Network settings
DEFAULT_TIMEOUT = 5  # seconds
MAX_RETRIES = 3

# File settings
DEFAULT_WORDLIST_FILE = "subdomains-10000.txt"

# Colors (for GUI styling)
BACKGROUND_COLOR = "#2C3E50"
INPUT_BACKGROUND_COLOR = "#34495E"
TEXT_COLOR = "white"
AUTHOR_COLOR = "#ECF0F1"

# Button gradients
START_BUTTON_GRADIENT = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3a7bd5, stop:1 #00d2ff)"
STOP_BUTTON_GRADIENT = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ff6e7f, stop:1 #bfe9ff)"

# Font settings
TITLE_FONT_FAMILY = "Georgia"
TITLE_FONT_SIZE = 30
AUTHOR_FONT_SIZE = 20
INPUT_FONT_SIZE = 18
BUTTON_FONT_SIZE = 18
RESULT_FONT_SIZE = 16 