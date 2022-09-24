from API import route,testing
import tkinter as tk
from tkinter import ttk

def main():
    r1 = route.APIRoute("route1")
    r1.isBatch = True
    r1.iterator = range(100)
    print([r.response_time() for r in r1.execute()])





if __name__ == '__main__':
    # root = tk.Tk()
    # root.option_add("*tearOff", False)
    # root.tk.call("source", "forest-dark.tcl")
    # style = ttk.Style(root)
    # style.theme_use("forest-dark")
    # root.mainloop()
    r1 = route.APIRoute("route1")
    testing.stress_expn(r1,100)
    