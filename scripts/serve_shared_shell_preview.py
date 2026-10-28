#!/usr/bin/env python3
"""Serve a version-pinned, immutable and media-free EstateShell WLAN acceptance preview.

This endpoint is deliberately not an EstatePublisher public host. The input
must be the non-publishing source-locked 3-site staged artifact and remains
read-only with no directory indexing or release mutation.
"""
from __future__ import annotations
import argparse
import json
import hashlib
import re
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

EXPECTED = {"fountain.estate.shell.v1-candidate-20261022", "fountain.estate.shell.v2-editorial-20261022"}
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, root:Path, personal_works_landing:bool=False, **kwargs):
        self._personal_works_landing = personal_works_landing
        super().__init__(*args, directory=str(root), **kwargs)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        if self.path.split("?",1)[0].lower().endswith((".mp4",".m4a")):
            self.send_header("Accept-Ranges","bytes")
        super().end_headers()
    def list_directory(self, path):
        self.send_error(404, "Directory listing disabled")
        return None
    def _private_path(self):
        return self.path.split('?',1)[0].strip('/') in ("source-lock.json","contract.json")
    def _redirect_personal_landing(self):
        if not self._personal_works_landing:
            return False
        if self.path.split("?",1)[0] not in ("/pointer/","/pointer/index.html"):
            return False
        self.send_response(308)
        self.send_header("Location","/works/")
        self.send_header("Content-Length","0")
        self.end_headers()
        return True
    def do_GET(self):
        if self._redirect_personal_landing():
            return
        if self._private_path():
            self.send_error(404)
            return
        return super().do_GET()
    def do_HEAD(self):
        if self._redirect_personal_landing():
            return
        if self._private_path():
            self.send_error(404)
            return
        return super().do_HEAD()

    def send_head(self):
        self._partial_bytes = None
        request_range=self.headers.get("Range")
        if not request_range or not self.path.split("?",1)[0].lower().endswith((".mp4",".m4a")):
            return super().send_head()
        movie=Path(self.translate_path(self.path))
        if not movie.is_file():
            return super().send_head()
        size=movie.stat().st_size
        m=re.fullmatch(r"bytes=(\d*)-(\d*)",request_range.strip())
        if not m or not any(m.groups()):
            self.send_error(416, "Unsupported byte range")
            return None
        first,last=m.groups()
        if first:
            start=int(first)
            end=int(last) if last else size-1
        else:
            suffix=int(last)
            start=max(0,size-suffix)
            end=size-1
        if start>=size or end<start or (not first and int(last)==0):
            self.send_error(416, "Range not satisfiable")
            return None
        end=min(end,size-1)
        source=movie.open("rb")
        source.seek(start)
        self._partial_bytes=end-start+1
        self.send_response(206)
        self.send_header("Content-Type","audio/mp4" if movie.suffix.lower()==".m4a" else "video/mp4")
        self.send_header("Content-Range",f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length",str(self._partial_bytes))
        self.end_headers()
        return source

    def copyfile(self,source,outputfile):
        remaining=getattr(self,"_partial_bytes",None)
        if remaining is None:
            return super().copyfile(source,outputfile)
        while remaining:
            data=source.read(min(1048576,remaining))
            if not data:break
            outputfile.write(data)
            remaining-=len(data)

def inspect(root:Path) ->dict:
    root=root.resolve(strict=True)
    lockpath=root/"source-lock.json"
    if not lockpath.is_file():
        raise RuntimeError("Refuse non-source-locked shell preview")
    meta=json.loads(lockpath.read_text())
    if (meta.get("status")!="WLAN-PREVIEW-NOT-PUBLIC"
        or meta.get("templateVersion") not in EXPECTED
        or not isinstance(meta.get("archiveMediaCopied"), bool)
        or meta.get("authorPublished") is not False
        or meta.get("releaseReceipt") is not None
        or set(meta.get("sites",{}))!={"estate","teatro","solstice"}):
        raise RuntimeError("Refuse release lacking immutable private preview predicates")
    for rel in ("estate/index.html","teatro/index.html",
        "solstice/editions/first-reading/index.html",
        "assets/estate-shell.css","assets/estate-shell-logo.png",
        "assets/estate-shell-state.js"):
        if not (root/rel).is_file():raise RuntimeError("Missing required route/asset: "+rel)
    media={}
    if meta["archiveMediaCopied"]:
        items=meta.get("historicalMediaFiles",[])
        if not isinstance(items,list) or not items:
            raise RuntimeError("Historical media inventory missing")
        for item in items:
            rel=item.get("path","")
            digest=item.get("sha256","")
            prefixes=("pointer/assets/historical-cache/boom-bangs/",
                      "pointer/assets/historical-media/")
            if (not isinstance(rel,str) or not rel.startswith(prefixes)
                or ".." in Path(rel).parts or Path(rel).is_absolute()
                or Path(rel).suffix.lower() not in (".jpg",".jpeg",".png",".mp4")
                or not isinstance(digest,str) or len(digest)!=64 or rel in media):
                raise RuntimeError("Invalid historical media scope")
            f=(root/rel).resolve()
            if not f.is_relative_to(root) or not f.is_file():
                raise RuntimeError("Historical media missing")
            if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:
                raise RuntimeError("Historical media digest mismatch")
            media[rel]=digest
    for scope in ("pointer/assets/historical-cache/boom-bangs",
                  "pointer/assets/historical-media"):
        for asset in (root/scope).rglob("*"):
            if asset.is_file() and asset.suffix.lower() in (".jpg",".jpeg",".png",".mp4"):
                if asset.relative_to(root).as_posix() not in media:
                    raise RuntimeError("Unlisted historical media")
    if list(root.rglob("*.wav")):
        raise RuntimeError("WAV not allowed on preview")
    for film in root.rglob("*.mp4"):
        if film.relative_to(root).as_posix() not in media:
            raise RuntimeError("Unexpected MP4 outside historical media scope")
    return meta

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--bind",default="192.168.8.50")
    p.add_argument("--port",type=int,default=8200)
    a=p.parse_args()
    meta=inspect(a.root)
    landing=meta.get("personalWorksLanding")
    if landing is not None and not (
        isinstance(landing,dict)
        and landing.get("stageFrom")=="/pointer/"
        and landing.get("stageTo")=="/works/"
        and landing.get("httpStatus")==308
        and landing.get("sourceOwner")=="Fountain-Coach/benedikt-eickhoff.de"
        and landing.get("stageOnly") is True
    ):
        raise RuntimeError("Invalid personal Works stage redirect")
    server=ThreadingHTTPServer((a.bind,a.port),
        partial(Handler,root=a.root.resolve(),personal_works_landing=landing is not None))
    server.daemon_threads=True
    print("READY EstateShell SOURCE-LOCKED WLAN ONLY",meta["templateVersion"],flush=True)
    server.serve_forever()
if __name__=="__main__":
    main()
