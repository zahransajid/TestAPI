from API import *


def make(req: Request):
    return req


def receive(rec: Response):
    rec.content = str(rec.content).split("\\")
    return rec
