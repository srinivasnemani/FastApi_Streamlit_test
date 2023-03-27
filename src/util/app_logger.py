import logging
import functools

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('fastapi_streamlit_app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

file_handler.terminator = '\n'
file_handler.flushInterval = 1
file_handler.flush()

logger.addHandler(file_handler)

def logger_decorator(func):
    """
    A decorator function that logs the start and end of the execution of the wrapped function,
    as well as any errors that occur during execution.

    Args:
    - func: The function to be wrapped.

    Returns:
    - A new function that wraps the original function.

    Usage:
    @logger_decorator
    async def my_func():
        # function code goes here
    """
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            logging.debug(f" Excecution started for the function  : {func.__name__}")
            result = await func(*args, **kwargs)
            logging.debug(f"Excecution ended at for the function : {func.__name__}")
            return result
        except Exception as e:
            logging.exception(f"Error in {func.__name__}: {e}")
            raise
    return wrapper