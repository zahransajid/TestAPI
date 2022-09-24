import os
import sys
import json
import importlib.util
from inspect import getmembers
from API.request import Request
from API.response import Response


class APIRoute:
    def __init__(self, readfrom=None,*args,**kwargs):
        # Loads in from directory if it exists
        self.readfrom = readfrom
        if readfrom != None:
            if validate(readfrom):
                self.load_from(readfrom)
        else:
            self.url = kwargs['url']
            self.req_type = kwargs['req_type']
            self.headers = kwargs['headers']
            self.data = kwargs['data']

    def save(self, path):
        # Save to a directory
        # Check if it exists and make it if it doesnt
        pass

    def load_from(self, path):
        with open(os.path.join(path, "definition.json")) as f:
            # Load in API definition
            self._route_definition = json.load(f)
            self._handler_name = self._route_definition["handler"]
            self._handler_path = os.path.join(self.readfrom, self._handler_name)
            _handler_spec = importlib.util.spec_from_file_location(
                self._handler_name, self._handler_path
            )
            _handler_module = importlib.util.module_from_spec(_handler_spec)
            sys.modules[self._handler_name] = _handler_module
            _handler_spec.loader.exec_module(_handler_module)
            self.handler = sys.modules[self._handler_name]
            self.members = getmembers(self.handler)
            for m in self.members:
                if m[0] == "make":
                    self.request_handler = m[1]
                if m[0] == "receive":
                    self.response_handler = m[1]

            self.url = self._route_definition["url"]
            self.req_type = self._route_definition["type"]
            self.headers = self._route_definition["default_headers"]
            self.data = self._route_definition["default_body"]
            f.close()

    def execute(self) -> Response:
        req = Request(self.req_type, self.url, self.headers, self.data)
        req = self.request_handler(req)
        req.set_time()
        response = Response(req.func(req.url, headers=req.headers, data=req.data),request=req)
        response.set_time()
        return self.response_handler(response)


def validate(path):
    return True