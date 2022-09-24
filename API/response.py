import requests
from API.request import Request
import time
import xmlformatter


class Response:
    def __init__(self, response: requests.Response, request: Request) -> None:
        self.response = response
        self.headers = self.response.headers
        self.request = request
        self.raw = self.response.raw
        self.content = self.response.content
        self.time = time.time()

    def isError(self) -> bool:
        return self.response.status_code > 400

    def set_time(self):
        self.time = time.time()

    def prettify(self):
        formatter = xmlformatter.Formatter(
            indent="1",
            indent_char="\t",
            encoding_output="ISO-8859-1",
            preserve=["literal"],
        )
        return formatter.format_string(str(self.content))
    def response_time(self):
        return self.time - self.request.time


class BatchResponse(Response):
    def __init__(self, response: requests.Response, request: Request) -> None:
        super().__init__(response, request)
        self.isBatch = True
