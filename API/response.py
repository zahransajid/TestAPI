import requests
from API.request import Request
import time


class Response:
    def __init__(self, response: requests.Response, request: Request) -> None:
        self.response = response
        self.headers = self.response.headers
        self.request = request
        self.raw = self.response.raw
        self.content = self.response.content
        self.time = time.time()

    def set_time(self):
        self.time = time.time()
