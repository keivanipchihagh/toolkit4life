from requests import Response, Session
from requests.adapters import HTTPAdapter, Retry


class BaseRequests():

    def __init__(self, retries: int = 3, backoff_factor: float = 0.1, status_forcelist: list = [500, 502, 503, 504]) -> None:
        """ Initialize and mount session """
        self.session = Session()
        retries = Retry(
            total = retries,
            backoff_factor = backoff_factor,
            status_forcelist = status_forcelist
        )

        # Mount session
        self.session.mount('http://', HTTPAdapter(max_retries = retries))
        self.session.mount('https://', HTTPAdapter(max_retries = retries))


    def get(self, url: str, params: dict = {}, headers: dict = None) -> Response:
        """ GET request """ 
        return self.session.get(url = url, params = params, headers = headers)


    def post(self, url: str, data: dict = {}, params: dict = {}, headers: dict = None) -> Response:
        """ POST request """
        return self.session.post(url = url, data = data, params = params, headers = headers)


    def delete(self, url: str, data: dict = {}, params: dict = {}, headers: dict = None) -> Response:
        """ DELETE request """
        return self.session.delete(url = url, data = data, params = params, headers = headers)


    def put(self, url: str, data: dict = {}, params: dict = {}, headers: dict = None) -> Response:
        """ PUT request """
        return self.session.delete(url = url, data = data, params = params, headers = headers)