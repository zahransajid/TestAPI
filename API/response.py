import requests
from API.request import Request
import time


class Response:
    """Defines the class for handling responses.
    
    Parameters:
    - response : a requests.Response object returned by a requests method.
    - request : the request object responsible for the response"""
    def __init__(self, response: requests.Response, request: Request) -> None:
        self.response = response
        self.headers = self.response.headers
        self.request = request
        self.raw = self.response.raw
        self.content = self.response.content
        self.time = time.time()

    def as_json(self):
        """Returns dictionary with
        - Headers
        - Raw
        - Content
        - ResponseTime"""
        return {
            "Headers": self.headers,
            "Raw": self.raw,
            "Content": self.content,
            "ResponseTime": self.response_time(),
        }

    def isError(self) -> bool:
        return self.response.status_code > 400

    def set_time(self):
        self.time = time.time()

    def response_time(self):
        return self.time - self.request.time


class BatchResponse(Response):
    def __init__(self, response: requests.Response, request: Request) -> None:
        super().__init__(response, request)
        self.isBatch = True
