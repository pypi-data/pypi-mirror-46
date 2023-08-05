import functools
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def check_path(p):
    """
    Verifies path.

    Args:
        p (str, pathlib.Path): Path object.

    Raises:
        ValueError: If path cannot be verified.

    """

    if not Path(p).exists():
        msg = f'The path does not exist: {str(p)}'
        logger.error(msg)
        raise ValueError(msg)


class cd:
    """Context manager for temporary cd."""

    def __init__(self, destination):
        self.original_dir = os.getcwd()
        self.new_dir = destination
        logger.debug('Recording origin directory: %s', self.original_dir)

    def __enter__(self):
        logger.debug('Changing to directory: %s', self.new_dir)
        os.chdir(self.new_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug('Returning to origin: %s', self.original_dir)
        os.chdir(self.original_dir)


def log_entrance_exit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('Entering %s.', func.__name__)
        results = func(*args, **kwargs)
        logger.info('Exiting %s.', func.__name__)
        return results

    return wrapper
