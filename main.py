from API import route, testing
import tkinter as tk
from tkinter import ttk
import os


def execute_request(data: dict):
    path = data["Path"]
    api_route = route.APIRoute(path)
    result = api_route.execute()
    return result.as_json()


def make_new_route(data: dict):
    path = data["Path"]
    api_route = route.APIRoute(
        readfrom=None,
        req_type=data["ReqType"],
        headers=data["Headers"],
        data={},
        isBatch=False,
        handler_name="index.py",
    )
    return None


def delete_route(data: dict):
    path = data["Path"]
    os.rmdir(path)
    return None


def run_batch_test(data: dict):
    testing.stress_expn(data["MaxN"])
    return None
