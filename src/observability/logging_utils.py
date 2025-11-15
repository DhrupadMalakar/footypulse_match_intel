import logging
import os


def init_logging(log_file_path: str) -> logging.Logger:
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    logger = logging.getLogger('footypulse')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info('Logging initialized')
    return logger
