# TestAPI

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A lightweight, modern, highly extensible API testing toolkit built on python, tkinter and requests.

The program is highly modular and affords the user both high and low level access to the request and response data.

The modular nature allows the user to write their own tests and show statistics as needed.

### Structure

Each API route is assigned its own folder containing a `definition.json` file and a `index.py` file.

The `definition.json` file contains default values for important parameters. However these can be overriden by the `index.py` file.

The `index.py` file has two functions `make` and `receive` which are called on the request and response objects respectively.

### Extensibility

Due to the modular nature of each API route and the usage of python scripting, the sky is literally the limit when it comes to filtering and manipulating API requests and responses.

In addition, the prebuilt data and utility classes help provide a simplified interface.

### Ease of use

The program offers all major functionality through GUI and allows quick and easy prototyping and templating.

This, combined with the extemely powerful scripting extensibility makes it a force to be reckoned with.

![GUI](https://github.com/zahransajid/TestAPI/blob/master/screenshots/screenshot2.jpeg?raw=true)
