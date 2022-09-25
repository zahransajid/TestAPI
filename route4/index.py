from API import *
import json

def make(req: Request):
    return req


def receive(rec: Response):
    data = json.loads(rec.content)
    l = data['length']
    if(l > 40):
        print(f"Its a large cat fact!\nIts {l} chars long.")
    return rec
