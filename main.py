from API import route
import tkinter as tk
from tkinter import ttk

def main():
    r1 = route.APIRoute("route1")
    print(r1.execute().content)





if __name__ == '__main__':
    root = tk.Tk()
    root.option_add("*tearOff", False)
    root.tk.call("source", "forest-dark.tcl")
    style = ttk.Style(root)
    style.theme_use("forest-dark")
    root.mainloop()
    # main()