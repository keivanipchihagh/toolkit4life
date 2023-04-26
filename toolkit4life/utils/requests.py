# Standard imports
from typing import List
from requests import Response, Session
from requests.adapters import HTTPAdapter, Retry

# Third-party imports
from .threads import Thread


class Requests():

    def __init__(self, timeout: int = None, retries: int = 3, backoff_factor: float = 0.1, status_forcelist: List[int] = [500, 502, 503, 504]) -> None:
        """
            Initialize and mount session

            Parameters:
                timeout (int): The number of seconds to wait before throwing a TimeOutExceotion (default is None, which means it'll wait until the connection is closed).
                retries (int): The number of retries to attempt if a request fails
                backoff_factor (float): The amount of time to wait between retries
                status_forcelist (list): A set of integer HTTP status codes that we should force a retry on
        """
        self.timeout = timeout
        self.session = Session()
        retries = Retry(
            total = retries,
            backoff_factor = backoff_factor,
            status_forcelist = status_forcelist
        )

        # Mount HTTP and HTTPS onto session
        self.session.mount('http://', HTTPAdapter(max_retries = retries))
        self.session.mount('https://', HTTPAdapter(max_retries = retries))


    def get(self, url: str, params: dict = {}, headers: dict = None, verify: bool = True, auth = None, threaded: bool = False) -> Response:
        """
            GET request

            Parameters:
                url (str): The URL to send the request to
                params (dict): The parameters to send with the request
                headers (dict): The headers to send with the request
                verify (bool): Whether or not to verify the SSL certificate
                auth: The authentication to send with the request
                threaded (bool): Whether or not to run the request in a thread
            Returns:
                (Response) The response from the request
        """
        thread = Thread(target = self.session.get, kwargs = {"url": url, "params": params, "headers": headers, "verify": verify, "auth": auth, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()


    def post(self, url: str, json: dict = {}, params: dict = {}, headers: dict = None, verify: bool = True, auth = None, threaded: bool = False) -> Response:
        """
            POST request

            Parameters:
                url (str): The URL to send the request to
                json (dict): The JSON to send with the request
                params (dict): The parameters to send with the request
                headers (dict): The headers to send with the request
                verify (bool): Whether or not to verify the SSL certificate
                auth: The authentication to send with the request
                threaded (bool): Whether or not to run the request in a thread
            Returns:
                (Response) The response from the request
        """
        thread = Thread(target = self.session.post, kwargs = {"url": url, "json": json, "params": params, "headers": headers, "verify": verify, "auth": auth, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()


    def delete(self, url: str, json: dict = {}, params: dict = {}, headers: dict = None, verify: bool = True, auth = None, threaded: bool = False) -> Response:
        """
            DELETE request

            Parameters:
                url (str): The URL to send the request to
                json (dict): The JSON to send with the request
                params (dict): The parameters to send with the request
                headers (dict): The headers to send with the request
                verify (bool): Whether or not to verify the SSL certificate
                auth: The authentication to send with the request
                threaded (bool): Whether or not to run the request in a thread
            Returns:
                (Response) The response from the request
        """
        thread = Thread(target = self.session.delete, kwargs = {"url": url, "json": json, "params": params, "headers": headers, "verify": verify, "auth": auth, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()


    def put(self, url: str, json: dict = {}, params: dict = {}, headers: dict = None, verify: bool = True, auth = None, threaded: bool = False) -> Response:
        """
            PUT request

            Parameters:
                url (str): The URL to send the request to
                json (dict): The JSON to send with the request
                params (dict): The parameters to send with the request
                headers (dict): The headers to send with the request
                verify (bool): Whether or not to verify the SSL certificate
                auth: The authentication to send with the request
                threaded (bool): Whether or not to run the request in a thread
            Returns:
                (Response) The response from the request
        """
        thread = Thread(target = self.session.put, kwargs = {"url": url, "json": json, "params": params, "headers": headers, "verify": verify, "auth": auth, "timeout": self.timeout})
        thread.start()
        if not threaded: return thread.join()