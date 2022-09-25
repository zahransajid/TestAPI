import multiprocessing
from queue import Queue
from API import route, testing
import tkinter as tk
from gui import GUI
from multiprocessing import Process
from tkinter import ttk
import os
from events import Events as events 


def execute_request(data: dict):
    path = data["Path"]
    api_route = route.APIRoute(path)
    result = api_route.execute()
    headers = { k : v[0:15] for k,v in result.headers.items()}
    return {
                "Headers" : headers,
                "Content": str(result.content)
            }


def make_new_route(data: dict):
    path = data["Path"]
    api_route = route.APIRoute(
        url=data["Url"],
        readfrom=None,
        req_type=data["ReqType"],
        headers=data["Headers"],
        data={},
        isBatch=False,
        handler_name="index.py",
    )
    api_route.save(path)
    return None


def delete_route(data: dict):
    path = data["Path"]
    os.rmdir(path)
    return None


def run_batch_test(data: dict):
    testing.stress_expn(data["MaxN"])
    return None

handlers = {
    events.execute_request: execute_request,
    events.delete_route: delete_route,
    events.make_new_or_update_route: make_new_route,
    events.run_batch_test: run_batch_test,
}
def run_gui (rcx: multiprocessing.Queue, trx: multiprocessing.Queue) : 
    g = GUI(rcx, trx)
    g.run()

def main():
    rcx = multiprocessing.Queue()
    trx = multiprocessing.Queue()
    p = Process(target=run_gui, args=(rcx, trx))
    p.start()
    # The main loop
    while True : 
        print("waiting")
        msg = rcx.get()
        resp = handlers[msg['Event']](msg['Data'])
        response = {
            "Event": msg['Event'],
            "Data": resp
        }
        print(response)
        trx.put(response)
                

if __name__  == "__main__" :
    main()


