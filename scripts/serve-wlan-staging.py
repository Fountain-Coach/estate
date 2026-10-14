#!/usr/bin/env python3
"""Three-front WLAN staging server: one Linux process, three local-only ports.

The input is a disposable projection from canonical GitHub owning sources.
No production DNS, Caddy, or publication authority is accessed.
"""
from __future__ import annotations

import functools
import json
import signal
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path("/home/benedikt/estate-three-front-staging")
IP = "192.168.8.249"
SITES = {"fountain": 8180, "solstice": 8181, "teatro": 8182}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(directory), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/__stage/health":
            self._health()
            return
        super().do_GET()

    def do_HEAD(self):
        if self.path.split("?", 1)[0] == "/__stage/health":
            self._health(head=True)
            return
        super().do_HEAD()

    def _health(self, head=False):
        try:
            release = (ROOT / "current").resolve()
            details = json.loads((release / "source-lock.json").read_text())
            payload = json.dumps({
                "status": "ready",
                "servedFrom": str(release),
                "source": "Fountain-Coach/estate",
                "sites": details["sites"],
                "productionPublished": False,
            }).encode()
            self.send_response(200)
        except Exception as error:
            payload = json.dumps({"status": "not-ready", "error": str(error)}).encode()
            self.send_response(503)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if not head:
            self.wfile.write(payload)

    def end_headers(self):
        # Staging should never be indexed or permanently cached by Safari.
        if not getattr(self, "_standard_headers_sent", False):
            self.send_header("Cache-Control", "no-store, max-age=0")
            self.send_header("X-Robots-Tag", "noindex, nofollow")
        super().end_headers()

    def log_message(self, format, *args):
        super().log_message(format, *args)


def main():
    services = []
    for site, port in SITES.items():
        directory = ROOT / "current" / site
        if not directory.is_dir():
            raise SystemExit("Missing site: " + str(directory))
        server = ThreadingHTTPServer(
            (IP, port),
            functools.partial(Handler, directory=directory),
        )
        server.daemon_threads = True
        services.append(server)
        print(f"STAGING_READY {site} http://{IP}:{port}/", flush=True)

    for service in services[1:]:
        threading.Thread(target=service.serve_forever, daemon=True).start()

    try:
        services[0].serve_forever()
    finally:
        for service in services:
            service.server_close()


if __name__ == "__main__":
    main()
