# Standard imports
from time import time
from typing import Callable
from datetime import datetime


# A Meta-Decorator (A decorator that can be used to decorate other decorators) is used on top of decorates to enable them to be parametrized
def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


def now() -> datetime: return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Prints status and the time taken to execute the function
@parametrized
def status(func: Callable, name: str) -> None:
    """ A decorator that logs the function's execution status onto a file """

    def run(*args, **kwargs):
        try:
            print(f"[INFO - {now()}] '{func.__name__}' started..")
            start_time = time()
            func(*args, **kwargs)
            print(f"[SUCCESS - {now()}] '{func.__name__}' executed successfully. (Took {round(time() - start_time, 2)} seconds)")
        except Exception as ex:            
            print(f"[ERROR - {now()}] '{func.__name__}' failed to execute. (details: {ex})")

    return run



@parametrized
def restart_on_crash(func: Callable, name: str, notify_crash: bool = True, retries: int = None) -> None:
    """
        A decorator that restarts a function forever if it crashes for any reason

        Parameters:
            func: The function to be restarted.
            name: The name of the function for logging purposes.
            notify_crash: A boolean that indicates whether to notify the user when the function crashes.
            retries: The number of times to retry the function before giving up. If None, the function will be retried forever.
    """

    def run(*args, **kwargs):
        _retries = 0
        while True:
            try:
                result = func(*args, **kwargs)                
                return None if result is None else result   # Return the return value of the function
            except Exception as ex:
                if notify_crash:
                    print(f"[WARNING - {now()}] '{name}' crashed! restarting... (details: {ex})")
                _retries += 1   # Increment the number of retries

            # Abort the function if the number of retries is greater than the maximum number of retries
            if retries is not None and _retries >= retries:
                print(f"[ERROR - {now()}] '{name}' crashed too many timee! aborting... (max tries: {retries})")
                break

    return run



@parametrized
def text(func: Callable, on_success: str, on_failure: str) -> None:
    """ A decorator that prints the time, given message and the execution duration """

    def run(*args, **kwargs):
        try:
            start_time = time()
            func(*args, **kwargs)
            print(f"SUCCESS - [{now()}] {on_success}. (Took {round(time() - start_time, 2)} seconds)")
        except Exception as ex:            
            print(f"[ERROR - {now()}] {on_failure}. (details: {ex})")

    return run