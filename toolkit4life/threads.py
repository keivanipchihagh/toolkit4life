# Standard imports
from threading import Thread as T


class Thread(T):
    """ A thread that can return a value once it's done. """

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = {}, Verbose = None):
        T.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        T.join(self, *args)
        return self._return


class ThreadPool():
    """ A pool of threads that can return a list of return values from threads once it's done """

    def __init__(self, confs: dict) -> None:
        """
        Constructor

        Parameters:
            confs: A dict of tuples containing the following keys:
                - key: The name of the thread
                - value: A tuple containing the following:
                    - target: The function/callable to be ran in the thread
                    - args: A tuple of arguments to be passed to the function
        """
        self.threads = []

        # Create threads
        for name, (target, args) in confs.items():
            if args is None: args = ()
            self.threads.append(Thread(target = target, args = args, name = name))


    def start(self) -> None:
        """ Start all threads in parallel """
        for thread in self.threads:
            thread.start()


    def join(self) -> dict:
        """ Wait for all threads to finish and return a dictionary of name:<return value> """
        return {thread.name: thread.join() for thread in self.threads}