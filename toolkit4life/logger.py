# https://stackoverflow.com/questions/1288498/using-the-same-decorator-with-arguments-with-functions-and-methods/1288936#1288936

# Standard imports
from time import time
from typing import Callable
from datetime import datetime


def __now() -> str:
    """ Returns the current datetime as string """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def __run(func: Callable, *args, **kwargs) -> tuple:
    """ Runs the given function with args and kwargs and returns the result and execution time """
    start_time = time()
    result = func(*args, **kwargs)
    return result, round(time() - start_time, 2)



class _MethodDecoratorAdaptor(object):

    def __init__(self, decorator, func):
        self.decorator = decorator
        self.func = func


    def __call__(self, *args, **kwargs):
        return self.decorator(self.func)(*args, **kwargs)


    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))



def auto_adapt_to_methods(decorator):
    """ Allows you to use the same decorator on methods and functions, hiding the self argument from the decorator """
    def adapt(func):
        return _MethodDecoratorAdaptor(decorator, func)
    return adapt



def status():
    """ A decorator that notifies state of the function execution and its duration """
    @auto_adapt_to_methods
    def wrapper(func: Callable):
        def wrapped(*args, **kwargs):
            try:
                print(f"[INFO - {__now()}] '{func.__name__}' started..")
                result, duration = __run(func, *args, **kwargs)
                print(f"[SUCCESS - {__now()}] '{func.__name__}' executed successfully. (Took {duration} seconds)")
                return result
            except Exception as ex:            
                print(f"[ERROR - {__now()}] '{func.__name__}' failed to execute. (details: {ex})")
        return wrapped
    return wrapper



def text(on_success: str, on_failure: str):
    """
        A decorator that shows custom text for function's execution states

        Parameters:
            on_success: Message to be shown when the function runs successfully
            on_failure: Message to be shown when the function throws and exception
    """
    @auto_adapt_to_methods
    def wrapper(func: Callable):
        def wrapped(*args, **kwargs):
            try:
                result, duration = __run(func, *args, **kwargs)
                print(f"SUCCESS - [{__now()}] {on_success}. (Took {duration} seconds)")
                return result
            except Exception as ex:            
                print(f"[ERROR - {__now()}] {on_failure}. (details: {ex})")
        return wrapped
    return wrapper



def restart_on_crash(warn_on_exception: bool = True, retries: int = None):
    """
        A decorator that restarts a function forever if it throws an exception

        Parameters:
            warn_on_exception: A boolean that indicates whether to warn the user when the function throws an exception.
            retries: The number of times to retry the function before giving up. If None, it will throw exception as normal
    """
    @auto_adapt_to_methods
    def wrapper(func: Callable):
        def wrapped(*args, **kwargs):
            _retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    if retries is None: raise Exception(ex)

                    if warn_on_exception:
                        print(f"[WARNING - {__now()}] '{func.__name__}' threw an exception! restarting {_retries + 1 }/{retries} ... (details: {ex})")
                    _retries += 1   # Increment the number of retries

                # Abort the function if the number of retries is greater than the maximum number of retries
                if _retries >= retries:
                    print(f"[ERROR - {__now()}] '{func.__name__}' was retried {retries} with no lucks! aborting... (max tries: {retries})")
                    break
        return wrapped
    return wrapper



def info(message: str) -> None:
    """ Prints a message as Info """
    print(f"[INFO - {__now()}] {message}")


def success(message: str) -> None:
    """ Prints a message as Success """
    print(f"[SUCCESS - {__now()}] {message}")


def error(message: str) -> None:
    """ Prints a message as error """
    print(f"[ERROR - {__now()}] {message}")


def warning(message: str) -> None:
    """ Prints a message as warning """
    print(f"[WARNING - {__now()}] {message}")