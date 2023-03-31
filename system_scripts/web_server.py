import sys
import argparse
from pathlib import Path
from functools import partial
from socketserver import ThreadingMixIn
from http.server import HTTPServer, SimpleHTTPRequestHandler


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    ''' Enable threading for HTTP server '''


def http_server(port: int, public_dir: str | Path):
    ''' Run HTTP server '''
    try:
        httpd = ThreadingSimpleServer(('', port), partial(
            SimpleHTTPRequestHandler, directory=public_dir))
        httpd.serve_forever()
    except ConnectionAbortedError:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=8080, type=int)
    parser.add_argument('--dir', default=Path(__file__).parent)
    args = parser.parse_args()

    if args.dir:
        if not Path(args.dir).exists() or not Path(args.dir).is_dir():
            sys.exit("Directory doesn't exist")

    http_server(args.port, args.dir)
