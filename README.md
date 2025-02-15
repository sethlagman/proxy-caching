
# **Proxy Caching**

Simple CLI tool that serves as a caching proxy server

## Features

- Starts a proxy server on the specified port
- Forwards requests to the specified origin
- Caches responses from the origin server
- Saves the cache locally
- Cache can be cleared

## Installation

- [X]  [Download Python 3.13.0](https://www.python.org/downloads/release/python-3130/)
- [X]  Clone or download this repository
- [X]  Go to the project directory via CLI or any IDE of your choice
- [X]  Create a virtual environment
    - For Linux or macOS: `python3 -m venv venv`
    - For Windows: `python -m venv venv`
- [X]  Activate the virtual environment
    - For Linux or macOS: `source venv/bin/activate`
    - For Windows: `venv\Scripts\activate`
- [X]  Install the dependencies
    - `pip install -r requirements.txt`
- [X]  Run the app
    - `python main.py --port <port-number> --origin <origin-url>`

## Usage

- [X]  Example of running the app
    - `python main.py --port 8000 --origin http://dummyjson.com`
- [X]  Request to
    - `http://localhost:8000/products`
- [X]  Is forwarded to
    - `http://dummyjson.com/products`
- [X]  To clear cache
    - `python main.py --clear-cache`

## Creation

- Python
