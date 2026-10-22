#!/usr/bin/env python3
"""Serve a version-pinned, immutable and media-free EstateShell WLAN acceptance preview.

This endpoint is deliberately not an EstatePublisher public host. The input
must be the non-publishing source-locked 3-site staged artifact and remains
read-only with no directory indexing or release mutation.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

EXPECTED = {"fountain.estate.shell.v1-candidate-20261022", "fountain.estate.shell.v2-editorial-20261022"}
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, root:Path, **kwargs):
        super().__init__(*args, directory=str(root), **kwargs)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()
    def list_directory(self, path):
        self.send_error(404, "Directory listing disabled")
        return None
    def _private_path(self):
        return self.path.split('?',1)[0].strip('/') in ("source-lock.json","contract.json")
    def do_GET(self):
        if self._private_path():
            self.send_error(404)
            return
        return super().do_GET()
    def do_HEAD(self):
        if self._private_path():
            self.send_error(404)
            return
        return super().do_HEAD()

def inspect(root:Path) ->dict:
    root=root.resolve(strict=True)
    lockpath=root/"source-lock.json"
    if not lockpath.is_file():
        raise RuntimeError("Refuse non-source-locked shell preview")
    meta=json.loads(lockpath.read_text())
    if (meta.get("status")!="WLAN-PREVIEW-NOT-PUBLIC"
        or meta.get("templateVersion") not in EXPECTED
        or meta.get("archiveMediaCopied") is not False
        or meta.get("authorPublished") is not False
        or meta.get("releaseReceipt") is not None
        or set(meta.get("sites",{}))!={"estate","teatro","solstice"}):
        raise RuntimeError("Refuse release lacking immutable private preview predicates")
    for rel in ("estate/index.html","teatro/index.html",
        "solstice/editions/first-reading/index.html",
        "assets/estate-shell.css","assets/estate-shell-logo.png",
        "assets/estate-shell-state.js"):
        if not (root/rel).is_file():raise RuntimeError("Missing required route/asset: "+rel)
    if list(root.rglob("*.mp4")) or list(root.rglob("*.wav")):
        raise RuntimeError("Audio/video media forbidden in shell acceptance stage")
    return meta

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--bind",default="192.168.8.50")
    p.add_argument("--port",type=int,default=8200)
    a=p.parse_args()
    meta=inspect(a.root)
    server=ThreadingHTTPServer((a.bind,a.port),partial(Handler,root=a.root.resolve()))
    server.daemon_threads=True
    print("READY EstateShell SOURCE-LOCKED WLAN ONLY",meta["templateVersion"],flush=True)
    server.serve_forever()
if __name__=="__main__":
    main()
