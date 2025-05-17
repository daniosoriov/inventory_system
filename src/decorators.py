import logging
from functools import wraps

logger = logging.getLogger()


def handle_exceptions(suppress: bool = False):
    """
    Decorator to handle exceptions in a function.
    Logs the error and prevents the program from crashing.

    :param suppress: If True, suppresses the exception and returns None.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"An error occurred in {func.__name__}: {e}", exc_info=True)
                if not suppress:
                    raise
                return None

        return wrapper

    return decorator
