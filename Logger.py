import logging
import sys

logger = None
def get_logger():
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')

        console_output = logging.StreamHandler(
            stream = sys.stdout)

        console_output.setLevel(logging.DEBUG)
        console_output.setFormatter(formatter)
        logger.addHandler(console_output)

    return logger
