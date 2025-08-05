from datetime import datetime
from .config import LOG_FILE

def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f'[{timestamp}] {message}\n')
