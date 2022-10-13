# Standard imports
from .threads import Thread
from requests import Response, Session
from requests.adapters import HTTPAdapter, Retry


class BaseRequests():

    def __init__(self, timeout: int = None, retries: int = 3, backoff_factor: float = 0.1, status_forcelist: list = [500, 502, 503, 504]) -> None:
        """
            Initialize a Base Requests instance with a Backoff-Strategy

            Parameters:
                timeout (int): The number of seconds to wait before throwing a TimeOutExceotion (default is None, which means it'll wait until the connection is closed). Be careful with this, as it can exhaust retries.
                retries (int): The number of times a request is rest with a Backoff-Strategy before giving up and throwign an Exception
                backoff_factor (float): Increase the amout of wait time between each failed requests
                status_forcelist (list): List of error messages that are forced a retry if received
        """

        self.timeout = timeout
        self.session = Session()
        retries = Retry(
            total = retries,
            backoff_factor = backoff_factor,
            status_forcelist = status_forcelist
        )

        # Mount session
        self.session.mount('http://', HTTPAdapter(max_retries = retries))
        self.session.mount('https://', HTTPAdapter(max_retries = retries))


    def get(self, url: str, params: dict = {}, headers: dict = None, threaded: bool = False) -> Response:
        """ GET request """
        thread = Thread(target = self.session.get, kwargs = {"url": url, "params": params, "headers": headers, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()


    def post(self, url: str, json: dict = {}, params: dict = {}, headers: dict = None, threaded: bool = False) -> Response:
        """ POST request """
        thread = Thread(target = self.session.post, kwargs = {"url": url, "json": json, "params": params, "headers": headers, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()


    def delete(self, url: str, json: dict = {}, params: dict = {}, headers: dict = None, threaded: bool = False) -> Response:
        """ DELETE request """
        thread = Thread(target = self.session.delete, kwargs = {"url": url, "json": json, "params": params, "headers": headers, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()


    def put(self, url: str, json: dict = {}, params: dict = {}, headers: dict = None, threaded: bool = False) -> Response:
        """ PUT request """
        thread = Thread(target = self.session.put, kwargs = {"url": url, "json": json, "params": params, "headers": headers, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()