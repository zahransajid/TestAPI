from asyncore import read
import json
import tkinter as tk
from tkinter import DISABLED, INSERT, NSEW, Label, ttk
from tkinter import font

class GUI () :
    def __init__(s) -> None:
        s.root = tk.Tk()
        s.root.title("Forest")
        s.root.option_add("*tearOff", False) # This is always a good idea

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
        
        s.routes_directory_list =[ key + "\n" + item['url'] for key, item in json.loads(open("./routes.json").read()).items()]
        s.methods_menu_list = ["POST", "GET", ""]
        s.request ={
            "method": tk.StringVar(value=s.methods_menu_list[0]),
            "url": tk.StringVar(value="http://google.com"),
        }

        s.response = {
            "body": tk.StringVar(value="Send a Request to view the response body"),
            "headers": {},
        }

        s.logging = tk.StringVar(value="Logging Started ...")

        s.setup_directory_traversal_panel()
        s.setup_request_config_panel()
        s.setup_response_config_panel()  

    def setup_directory_traversal_panel (s) : 
        # The routes browser
        routes_directory_frame = ttk.LabelFrame(s.root, text="Saved Routes Configuration Browser", padding=(20, 20))
        routes_directory_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky=NSEW)
        routes_directory_frame.columnconfigure(index=0, weight=1)
        for directory, i in zip(s.routes_directory_list, range(len(s.routes_directory_list))): 
                button = ttk.Button(routes_directory_frame, text=directory, style="Accent.TButton")
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
        raw_response_data = '''
        <!doctype html>

        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>A Basic HTML5 Template</title>
        <meta name="description" content="A simple HTML5 Template for new projects.">
        <meta name="author" content="SitePoint">

        <meta property="og:title" content="A Basic HTML5 Template">
        <meta property="og:type" content="website">
        <meta property="og:url" content="https://www.sitepoint.com/a-basic-html5-template/">
        <meta property="og:description" content="A simple HTML5 Template for new projects.">
        <meta property="og:image" content="image.png">

        <link rel="icon" href="/favicon.ico">
        <link rel="icon" href="/favicon.svg" type="image/svg+xml">
        <link rel="apple-touch-icon" href="/apple-touch-icon.png">

        <link rel="stylesheet" href="css/styles.css?v=1.0">

        </head>

        <body>
        <!-- your content here... -->
        <script src="js/scripts.js"></script>
        </body>
        </html>'''
        response_raw_data_text = tk.Text(response_raw_data_pane )
        response_raw_data_text.grid(row=0, column=0, sticky=tk.NSEW)
        response_raw_data_text.insert(INSERT, raw_response_data)
        response_raw_data_text.config(state=DISABLED)
        notebook.add(response_raw_data_pane, text="Raw Text")

        # Tab #2 - Response Headers
        response_header_pane = ttk.Frame(notebook)
        response_header_pane.columnconfigure(index=0, weight=1)
        response_header_pane.columnconfigure(index=1, weight=1)
        response_headers = {
            "Status Code": "200",
            "Connection": "Keep Alive",
            "Content Encoding": "Keep-Alive",
            "Server": "Apache",
            "x-frame-options": "DENY"
        }

        for (header, value), i in zip(response_headers.items(), range(len(response_headers))) :
            text = Label(response_header_pane, text=header, relief=tk.GROOVE, font=('Courier', 15))
            text.grid(row=i, column=0, padx=5, pady=5, sticky=NSEW)
            value = Label(response_header_pane, text=value, relief=tk.GROOVE, font=('Courier', 15))
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
        request_method_combobox = ttk.Combobox(request_configuration_frame, state="readonly", values=s.methods_menu_list)
        request_method_combobox.set(s.methods_menu_list[0])
        request_method_combobox.grid(row=0, column=0, padx=5, pady=10,  sticky="ew")

        request_url_entry = ttk.Entry(request_configuration_frame, textvariable=s.request['url'])
        request_url_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        send_request_button = ttk.Button(request_configuration_frame, text="Send Request")
        send_request_button.grid(row=1, column=0, columnspan=2, sticky=NSEW, padx=5, pady=10)

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

    
 


if __name__ == "__main__" : 
    g = GUI()
    g.run()