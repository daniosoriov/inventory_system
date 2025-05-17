import logging
from functools import wraps

logger = logging.getLogger()


def handle_exceptions(func):
    """
    Decorator to handle exceptions in a function.
    Logs the error and prevents the program from crashing.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in {func.__name__}: {e}")
            return None

    return wrapper
