import http.server
import socketserver
import requests
import json
import os
from argparse import ArgumentParser
from cachetools import LRUCache
from urllib.parse import urlparse

CACHE_FILE = 'cache.json'

cache = LRUCache(maxsize=10)

def load_cache():
    """Loads cache"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as file:
                cache.update(json.load(file))
        except Exception as e:
            print('Error loading cache: ' + e)


def save_cache():
    """Saves cache"""
    with open(CACHE_FILE, 'w') as file:
        json.dump(dict(cache), file)


def clear_cache():
    """Clears cache"""
    cache.clear()
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


class CachingProxyHandler(http.server.BaseHTTPRequestHandler):
    """Proxy Request Handler with Caching"""
    
    def do_GET(self):
        global cache
        parsed_url = urlparse(self.path)
        cache_key = parsed_url.path

        if cache_key in cache:
            print(f"Cache hit: {cache_key}")
            cached_content, content_type = cache[cache_key]
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('X-Cache', 'HIT')
            self.end_headers()
            self.wfile.write(cached_content.encode("utf-8"))
            return

        print(f"Cache miss: {cache_key}")

        # Forward request to origin
        origin_url = f"{self.server.origin}{self.path}"
        try:
            headers = {'Accept-Encoding': 'identity'}
            response = requests.get(origin_url, headers=headers, stream=True)

            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                cache[cache_key] = (response.text, content_type)
                save_cache()
            
            self.send_response(response.status_code)

            for key, value in response.headers.items():
                if key.lower() != 'transfer-encoding':
                    self.send_header(key, value)

            self.send_header('X-Cache', 'MISS')
            self.send_header('Content-type', content_type)
            self.end_headers()

            for chunk in response.iter_content(chunk_size=4096):
                self.wfile.write(chunk)
        
        except requests.RequestException as e:
            self.send_error(500, f"Error fetching data: {e}")


def main():

    parser = ArgumentParser(description="Proxy Caching")

    parser.add_argument('--port', type=int, help='Port where the caching proxy server will run')
    parser.add_argument('--origin', type=str, help='URL of the origin server to forward request')
    parser.add_argument('--clear-cache', action='store_true', help='Clears the cache')

    args = parser.parse_args()

    if args.clear_cache:
        print('Cache cleared')
        clear_cache()
        return

    load_cache()
    
    class ProxyServer(socketserver.TCPServer):
        """Custom TCP Server to store origin"""
        def __init__(self, server_address, handler, origin):
            super().__init__(server_address, handler)
            self.origin = origin

    with ProxyServer(("", args.port), CachingProxyHandler, args.origin) as httpd:
        print(f"Serving at port {args.port}, forwarding to {args.origin}")
        httpd.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        save_cache()
