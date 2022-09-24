import requests
import time


class Request:
    def __init__(self, method: str, url: str, headers: dict, data: dict) -> None:
        self.method = method
        self.REQ_TYPES = {"GET": requests.get, "POST": requests.post}
        self.func = self.REQ_TYPES[self.method]
        self.url = url
        self.headers = headers
        self.data = data
        self.time = time.time()

    def set_time(self):
        self.time = time.time()
