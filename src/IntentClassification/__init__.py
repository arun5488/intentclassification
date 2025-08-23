import logging
import os
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOGS_DIR = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOGS_DIR, exist_ok = True)

log_file_path = os.path.join(LOGS_DIR, LOG_FILE)

#creating custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#file handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(logging.Formatter("[ %(asctime)s ] [ %(levelname)s ][ %(lineno)d ] [ %(name)s ] - %(message)s"))

# console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[ %(asctime)s ] [ %(levelname)s ][ %(lineno)d ] [ %(name)s ] - %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)