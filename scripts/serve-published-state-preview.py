#!/usr/bin/env python3
"""Read-only WLAN-only visual proof of the existing public estate plus Satzfunk.

Never proxy or serve the private Satzfunk player. No media, authentication or
production estate publisher is involved.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, root, **kwargs):
        super().__init__(*args, directory=str(root), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404)
        return None

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--bind",default="192.168.8.50")
    parser.add_argument("--port",type=int,default=8197)
    args=parser.parse_args()
    root=args.root.resolve(strict=True)
    if not (root/"capture-lock.json").is_file():
        raise SystemExit("Not a captured and pinned published-state preview")
    from functools import partial
    server=ThreadingHTTPServer((args.bind,args.port),partial(Handler,root=root))
    server.daemon_threads=True
    print("READY local published-state preview",args.bind,args.port,root,flush=True)
    server.serve_forever()
