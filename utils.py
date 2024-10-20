# utils.py
import logging

def setup_logging(name):
    """
    Set up logging with the given logger name.
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)