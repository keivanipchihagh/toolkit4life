# Standard imports
from typing import Callable
from datetime import datetime


def __now() -> str:
    """ Returns the current datetime as string """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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



def restrict_by_username(whitelist: list = [], unauthorized_reply_msg: str = None):
    """
        A decorator that restricts access to a function based on the username of the user who called it.

        Parameters:
            whitelist (list): A list of usernames that are allowed to access the function.
            unauthorized_reply_msg (str): If not spesified, the default message is replied
    """
    @auto_adapt_to_methods
    def wrapper(func: Callable):
        def wrapped(*args, **kwargs):
            update = args[0]
            username = update.effective_user.username

            if username not in whitelist:
                print(f"[ACCESS DENIED - {__now()}] Unauthorized access denied for '{username}'.")
                update.message.reply_text(unauthorized_reply_msg if unauthorized_reply_msg is not None else f" Sorry, you are not permitted to use this bot.")
                return
            return func(*args, **kwargs)
        return wrapped
    return wrapper



def restrict_by_id(whitelist: list = [], unauthorized_reply_msg: str = None):
    """
        A decorator that restricts access to a function based on the ID of the user who called it.

        Parameters:
            whitelist (list): A list of IDs that are allowed to access the function.
            unauthorized_reply_msg (str): If not spesified, the default message is replied
    """
    @auto_adapt_to_methods
    def wrapper(func: Callable):
        def wrapped(*args, **kwargs):
            update = args[0]
            id = update.effective_user.id

            if id not in whitelist:
                print(f"[ACCESS DENIED - {__now()}] Unauthorized access denied for '{id}'.")
                update.message.reply_text(unauthorized_reply_msg if unauthorized_reply_msg is not None else f" Sorry, you are not permitted to use this bot.")
                return
            return func(*args, **kwargs)
        return wrapped
    return wrapper
