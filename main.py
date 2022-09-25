from audioop import mul
from queue import Queue
from API import route, testing
import tkinter as tk
from gui import GUI
from multiprocessing import Process
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

class EventManager():
    def __init__(self) -> None:
       
    def loop(self) -> None:
            self.res = self.thread_queue.get()
            self._print(self.res)
            self.root.after(100, self.listen_for_result)

def main():
    p = Process(lambda : GUI())