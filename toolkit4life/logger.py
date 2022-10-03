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


# logger
@parametrized
def status(func: Callable, name: str):
    """
        A decorator that logs the function's execution status onto a file

        parameters:
            func: The function to be logged.
    """

    def now() -> datetime: return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def run(*args, **kwargs):
        try:
            print(f"[INFO - {now()}] '{name}' started..")
            start_time = time()
            func(*args, **kwargs)
            print(f"[SUCCESS - {now()}] '{name}' executed successfully. (Took {round(time() - start_time, 2)} seconds)")
        except Exception as ex:            
            print(f"[ERROR - {now()}] '{name}' failed to execute. (details: {ex})")

    return run