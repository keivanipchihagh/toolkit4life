# Standard imports
from threading import Thread as T


class Thread(T):
    """ Modified thread object that can return a value once its execution is complete """

    def __init__(self, group = None, target = None, name: str = None, args: tuple = (), kwargs: dict = {}) -> None:
        """
            Constructor

            Parameters:
                group: Thread group
                target: The function/callable to be ran in the thread
                name (str): The name of the thread
                args (tuple): A tuple of arguments to be passed to the function
                kwargs (dict): A dictionary of keyword arguments to be passed to the function
        """
        T.__init__(self, group, target, name, args, kwargs)
        self._return = None


    def run(self) -> None:
        """ Run the thread (non-blocking) """
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)    # Run the target function and store the return value


    def join(self, *args):
        """ Wait for the thread to finish and return the return value """
        T.join(self, *args)     # Block until the thread is done
        return self._return     # Return the return value


class ThreadPool():
    """ Modified thread pool object that can return a dictionary of name:<return value> once all threads have finished execution """

    def __init__(self, configs: dict) -> None:
        """
        Constructor

        Parameters:
            configs (dict): A dict of tuples containing the following keys:
                - key: The name of the thread
                - value: A tuple containing the following:
                    - target: The function/callable to be ran in the thread
                    - args: A tuple of arguments to be passed to the function
        """
        self.threads = []

        # Initialize threads
        for name, (target, args) in configs.items():
            if args is None: args = ()
            self.threads.append(Thread(target = target, args = args, name = name))


    def start(self) -> None:
        """ Execute threads in parallel """
        for thread in self.threads:
            thread.start()


    def join(self) -> dict:
        """ Wait for all threads to finish and return a dictionary of name:<return value> """
        return {thread.name: thread.join() for thread in self.threads}


    def start_and_join(self) -> dict:
        """ Execute threads in parallel and return a dictionary of name:<return value> when all threads have finished execution """
        self.start()
        return self.join()