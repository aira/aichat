"""Constants like BOT_NAME, BASE_DIR, DATA_DIR, PACKAGE_DIR"""
import os


BOT_NAME = os.getenv('BOT_NAME', 'Bot')

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.dirname(PACKAGE_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.abspath(os.path.join(PACKAGE_DIR, 'data'))

DEFAULT_CONTEXT_PATH = os.path.join(DATA_DIR, BOT_NAME.lower().strip().replace(' ', '-') + '.json')
DEFAULT_RESPONSE_MAPPING_PATH = os.path.join(DATA_DIR, BOT_NAME.lower().strip().replace(' ', '-') + '.csv')
DEFAULT_ERROR_MESSAGES_PATH = os.path.join(DATA_DIR, BOT_NAME.lower().strip().replace(' ', '-') + 'errors.csv')

DEFAULT_CONTEXT = {
    "user": {
        "name": {
            "last": "Explorer",
            "preferred": "Explorer",
            "nickname": "Explorer",
            "full": "Aira Explorer",
            "first": "Aira"
            }
        }
    }
DEFAULT_RESPONSE_MAPPING = [
    ('Hi', 'Hi!'),
    ('Hey', 'Hi!')
    ]
DEFAULT_ERROR_MESSAGES = [
    ('unknown_command',
        "I heard you, but I don't understand what you would like. Can you say that in a different way?"),
    ]
