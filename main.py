import http.server
import socketserver
from argparse import ArgumentParser
from cachetools import cached, LRUCache, TTLCache

def main():

    parser = ArgumentParser(description="Proxy Caching")

    parser.add_argument('--port', type=int, help='Port Number', required=True)
    parser.add_argument('--origin', type=str, help='URL', required=True)

    args = parser.parse_args()

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        print(f"Serving at port {args.port}")
        httpd.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated")