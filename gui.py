from asyncore import read
from copy import deepcopy
import json
from logging.handlers import QueueListener
import multiprocessing
from queue import Queue
import queue
import tkinter as tk
from tkinter import DISABLED, INSERT, NSEW, Label, ttk
from tkinter import font
from tkinter import messagebox
from API.route import APIRoute
from events import Events as events

class GUI () :
    def __init__(s, rcx:multiprocessing.Queue, trx:multiprocessing.Queue) -> None:
        s.root = tk.Tk()
        s.root.title("TestAPI")
        s.root.option_add("*tearOff", False) # This is always a good idea

        s.trx = rcx
        s.rcx = trx

        # Make the app responsive
        s.root.rowconfigure(index=0, weight=1)
        s.root.rowconfigure(index=1, weight=1)
        s.root.columnconfigure(index=1, weight=1)

        # Create a style
        style = ttk.Style(s.root)

        # Import the tcl file
        s.root.tk.call("source", "forest-dark.tcl")

        # Set the theme with the theme_use method
        style.theme_use("forest-dark")
        
        s.current_route = 0
        s.routes_directory_list = [ APIRoute(i) for i in json.loads(open("./routes.json").read())]
        s.methods_menu_list = ["POST", "GET", "PUT", "DELETE"]
        s.request ={
            "method": tk.StringVar(value=s.methods_menu_list[0]),
            "url": tk.StringVar(value="http://google.com"),
            "headers": {
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                "Keep-Alive": "300",
                "Connection": "keep-alive",
            }
        }

        s.response = {
            "body": "Send a Request to view the response body",
            "headers": {
            "Status Code": "200",
            "Connection": "Keep Alive",
            "Content Encoding": "g-zp",
            "x-frame-options": "DENY"
            }
        }

        s.logging = tk.StringVar(value="Logging Started ...")

        s.setup_directory_traversal_panel()
        s.setup_request_config_panel()
        s.setup_response_config_panel() 
        s.load_route(0)
        s.listener()

    def load_route(s, i : int) :
        routes = s.routes_directory_list[i]
        s.current_route = 0
        s.request['method'].set(routes.req_type)
        s.request['url'].set(routes.url)
        s.request['headers'] = routes.headers
        s.setup_request_config_panel()

    def setup_directory_traversal_panel (s) : 
        # The routes browser
        routes_directory_frame = ttk.LabelFrame(s.root, text="Saved Routes Configuration Browser", padding=(20, 20))
        routes_directory_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky=NSEW)
        routes_directory_frame.columnconfigure(index=0, weight=1)
        for directory, i in zip(s.routes_directory_list, range(len(s.routes_directory_list))): 
                button = ttk.Button(routes_directory_frame, text=directory.readfrom+ "\n" + directory.url, style="Accent.TButton", command= lambda j = i: s.load_route(j))
                button.grid(row=i, column=0, sticky=NSEW, padx=5, pady=5)

    def setup_response_config_panel (s) :
        # The response column configure
        # Panedwindow
        response_config_panel = ttk.LabelFrame(s.root, text="Response Details")
        response_config_panel.grid(row=1, column=1, columnspan=2, pady=(10, 5), sticky="nsew")

        # Notebook
        notebook = ttk.Notebook(response_config_panel)

        # Tab #1 Raw Body Response Pane
        response_raw_data_pane = ttk.LabelFrame(notebook)
        response_raw_data_text = tk.Text(response_raw_data_pane )
        response_raw_data_text.grid(row=0, column=0, sticky=tk.NSEW)
        response_raw_data_text.insert(INSERT, s.response['body'])
        response_raw_data_text.config(state=DISABLED)
        notebook.add(response_raw_data_pane, text="Raw Text")

        # Tab #2 - Response Headers
        response_header_pane = ttk.Frame(notebook)
        response_header_pane.columnconfigure(index=0, weight=1)
        response_header_pane.columnconfigure(index=1, weight=1)


        for (header, value), i in zip(s.response['headers'].items(), range(len(s.response['headers']))) :
            text = Label(response_header_pane, text=header, relief=tk.GROOVE, font=('Courier', 10))
            text.grid(row=i, column=0, padx=5, pady=5, sticky=NSEW)
            value = Label(response_header_pane, text=value, relief=tk.GROOVE, font=('Courier', 10))
            value.grid(row=i, column=1, padx=5, pady=5, sticky=NSEW)


        notebook.add(response_header_pane, text="Response Headers")



        # Tab #3 
        tab_3 = ttk.Frame(notebook)
        notebook.add(tab_3, text="Logging")
        notebook.pack(expand=True, fill="both", padx=5, pady=5)

    def setup_request_config_panel (s) :
        # The request column configure
        request_configuration_frame = ttk.LabelFrame(s.root, text="Request Configuration", padding=(20, 10))
        request_configuration_frame.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

        request_configuration_frame.columnconfigure(index=1, weight=1)
        request_method_combobox = ttk.Combobox(request_configuration_frame, state="readonly", values=s.methods_menu_list, textvariable=s.request['method'])
        request_method_combobox.set(s.methods_menu_list[0])
        request_method_combobox.grid(row=0, column=0, padx=5, pady=10,  sticky="ew")

        request_url_entry = ttk.Entry(request_configuration_frame, textvariable=s.request['url'])
        request_url_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        request_config_headers_frame = ttk.LabelFrame(request_configuration_frame, text="Request Headers", padding=(20, 10))
        request_config_headers_frame.grid(row=1, column=0, columnspan=2)
        
        for (header, value), i in zip(s.request['headers'].items(), range(len(s.request['headers']))) :
            text = Label(request_config_headers_frame, text=header, relief=tk.GROOVE, font=('Courier', 10))
            text.grid(row=i, column=0, padx=5, pady=5, sticky=NSEW)
            value = Label(request_config_headers_frame, text=value, relief=tk.GROOVE, font=('Courier', 10))
            value.grid(row=i, column=1, padx=5, pady=5, sticky=NSEW)

        send_request_button = ttk.Button(request_configuration_frame, text="Send Request", command=s.send_request)
        send_request_button.grid(row=2, column=1, columnspan=1, sticky=NSEW, padx=5, pady=10)
        save_request_button = ttk.Button(request_configuration_frame, text="Save Request", command=s.update_routes)
        save_request_button.grid(row=2, column=0, columnspan=1, sticky=NSEW, padx=5, pady=10)

        


    def run(s) :
        s.root.mainloop()

        # Center the window, and set minsize
        s.root.update()
        s.root.minsize(s.root.winfo_width(), s.root.winfo_height())
        x_cordinate = int((s.root.winfo_screenwidth()/2) - (s.root.winfo_width()/2))
        y_cordinate = int((s.root.winfo_screenheight()/2) - (s.root.winfo_height()/2))
        s.root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

        # Start the main loop
        s.root.mainloop()
    
    def send_request (s) :
        s.trx.put({
            "Event": "ExecuteRequest",
            "Data": {
                "Path" : s.routes_directory_list[s.current_route].readfrom
            }
        })
    
    def update_routes (s) : 
        s.trx.put({
            "Event": events.make_new_or_update_route,
            "Data": {
                "ReqType": s.request['method'].get(),
                "Path": s.routes_directory_list[s.current_route].readfrom,
                "Url": s.request['url'].get(),
                "Headers": {}
            }
        })
        
    def listener (s) :
        try:
            res = s.rcx.get(0)
            event = res['Event']
            dat = res['Data']
            if event == events.execute_request:
                print("got response")
                s.response['body'] = dat['Content']
                s.response['headers'] = dat['Headers']
                s.setup_response_config_panel()
            
            elif event == events.make_new_or_update_route : 
                messagebox.showinfo("Update Route", "Route Save Successfully")

            s.root.after(100, s.listener)
        except queue.Empty:
            s.root.after(100, s.listener)


    
 


if __name__ == "__main__" : 
    g = GUI(multiprocessing.Queue())
    g.run()