"""
Decorators for Python-based keywords.
"""
import functools
import sys

import robot
from robot.api import logger
from robot.libraries.Screenshot import Screenshot

from tos.settings import PLATFORM
from tos.utils import get_stacktrace_string


def log_number_of_task_objects(func):
    """
    Decorator for logging the number of processed task objects.

    Note that the function to decorate should return the
    number of processed objects.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        counter = func(*args, **kwargs)
        if counter == 0:
            logger.warn("No task objects processed")
        else:
            logger.info(f"{counter} task object(s) processed")
        return counter
    return wrapper


def handle_errors(error_msg=""):
    """
    Decorator for handling all general exceptions.

    Function to decorate ``func`` is the set of actions we are trying to do
    (e.g., ``main_action`` method). That function can take arbitrary arguments.
    All exceptions are caught when this function is called. When exception
    occurs, full stacktrace is logged with Robot Framework logger and the status
    of task object is set to 'fail'.

    The task object must be passed as a keyword argument so it can
    be accessed here inside the decorator.

    :returns: value, status, where value is either the return value of the
     decorated function or the exception message from the exception encountered
     in this function call. Status is always either "pass" or "fail".
    :rtype: tuple

    Usage example:

    .. code-block:: python

        class RobotLibrary:

            def __init__(self):
                self.error_msg = "Alternative error message"

            @handle_errors("One is not one anymore")
            def function_which_might_fail(self, to=None):
                if to["one"] != 1:
                    raise ValueError


    >>> RobotLibrary().function_which_might_fail(to={"one": 2})
        """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lib_instance = args[0]
            _error_msg = error_msg
            if not error_msg:
                _error_msg = getattr(lib_instance, "error_msg", "")
            to = kwargs.get("to", {})

            value = None
            # TODO: consider adding BusinessException back here
            try:
                value = func(*args, **kwargs)
            except NotImplementedError:
                raise
            except Exception:
                value, _ = get_stacktrace_string(sys.exc_info())
                logger.error(
                    f"Task {to.get('_id')} failed: {_error_msg}.\n{value}"
                )
                _take_screenshot()
                status = "fail"
            else:
                status = "pass"
            return value, status
        return wrapper
    return decorator


def _take_screenshot():
    """Take screenshot of all visible screens.

    Use Robot Framework standard library with Scrot screenshotting utility.
    """
    if PLATFORM == "Linux":
        module = "Scrot"  # NOTE: needs Scrot to be installed with apt-get or similar
    elif PLATFORM == "Windows":  # pragma: no cover
        module = "Pil"
    else:  # pragma: no cover
        logger.warn("Screenshotting is supported only on Windows and Linux")
        return
    try:
        Screenshot(screenshot_module=module).take_screenshot()
    except robot.libraries.BuiltIn.RobotNotRunningError as err:
        logger.warn(
            f"Robot needs to be running for screenshotting to work: {str(err)}")


# Is this ever needed?
# def abort_on_failure(error_msg):
#     """
#     Decorator for stopping execution of the robot if
#     the decorated function fails.
#     """
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 value = func(*args, **kwargs)
#             except Exception as err:
#                 exc_type, exc_value, exc_traceback = sys.exc_info()
#                 exc_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
#                 exc_text = " ".join(exc_lines)
#                 logger.fatal(f"{error_msg}:\n{exc_text}")
#                 BuiltIn().run_keyword("Fatal Error")
#             else:
#                 return value
#         return wrapper
#     return decorator
