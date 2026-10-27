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
    def __init__(self, *args, root:Path, **kwargs):
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
    teatro=meta.get("teatroSatzfunkPlayerScenarioStage",{})
    released=teatro.get("releasedMediaFiles",[]) if isinstance(teatro,dict) else []
    if released:
        if (teatro.get("scenarioID")!="teatro.satzfunk-player-ear-wind.01"
            or teatro.get("status")!="WLAN-CANDIDATE-PLAYER-ROUTE-AND-BOOK-STAGED-LIVE-ACCEPTANCE-PENDING"
            or teatro.get("publicProductionAffected") is not False
            or not teatro.get("scenarioRoute","/teatro/scenarios/").startswith("/teatro/scenarios/")):
            raise RuntimeError("Released Teatro media requires the source-locked Player Scenario candidate")
        if not isinstance(released,list) or len(released)>4:
            raise RuntimeError("Invalid source-locked Teatro released-media inventory")
        for item in released:
            rel=item.get("path","")
            digest=item.get("sha256","")
            size=item.get("bytes")
            if (not isinstance(rel,str) or not rel.startswith("teatro/media/")
                or ".." in Path(rel).parts or Path(rel).is_absolute()
                or Path(rel).suffix.lower()!=".mp4"
                or not isinstance(digest,str) or not re.fullmatch(r"[a-f0-9]{64}",digest)
                or not isinstance(size,int) or size<=0
                or item.get("publicReleaseAuthorized") is not True
                or not isinstance(item.get("publicSource"),str)
                or not item["publicSource"].startswith("https://")
                or not isinstance(item.get("sourceRepository"),str)
                or not item["sourceRepository"].startswith("Fountain-Coach/")
                or rel in media):
                raise RuntimeError("Invalid source-locked Teatro released-media entry")
            f=(root/rel).resolve()
            if not f.is_relative_to(root) or not f.is_file():
                raise RuntimeError("Source-locked Teatro media missing")
            data=f.read_bytes()
            if len(data)!=size or hashlib.sha256(data).hexdigest()!=digest:
                raise RuntimeError("Source-locked Teatro media bytes mismatch")
            media[rel]=digest
    for scope in ("pointer/assets/historical-cache/boom-bangs",
                  "pointer/assets/historical-media"):
        for asset in (root/scope).rglob("*"):
            if asset.is_file() and asset.suffix.lower() in (".jpg",".jpeg",".png",".mp4"):
                if asset.relative_to(root).as_posix() not in media:
                    raise RuntimeError("Unlisted historical media")
    study = meta.get("doorScoreEssayStage", {})
    wavs = study.get("permittedWAVFiles", []) if isinstance(study, dict) else []
    admitted_wavs = set()
    if wavs:
        if (study.get("sourceOwner") != "Fountain-Coach/fountain.coach"
            or not re.fullmatch(r"[a-f0-9]{40}", study.get("sourceCommit", ""))
            or study.get("scope") != "owner-WLAN-only"
            or study.get("publicProductionAffected") is not False
            or study.get("sourceLicense") != "CC0-1.0"
            or study.get("sourceURL") != "https://opengameart.org/content/100-cc0-metal-and-wood-sfx"
            or not isinstance(wavs, list) or len(wavs) > 8):
            raise RuntimeError("Invalid authored sound-study admission")
        for item in wavs:
            rel, digest, size = item.get("path", ""), item.get("sha256", ""), item.get("bytes")
            if (not isinstance(rel, str)
                or not rel.startswith("estate/essays/the-door-is-a-score/assets/")
                or Path(rel).suffix.lower() != ".wav" or ".." in Path(rel).parts
                or not re.fullmatch(r"[a-f0-9]{64}", digest)
                or not isinstance(size, int) or not 0 < size <= 10000000
                or item.get("sourceKind") not in {"CC0-source-conversion", "authored-sound-study"}
                or rel in admitted_wavs):
                raise RuntimeError("Invalid source-locked study WAV entry")
            asset = (root / rel).resolve()
            if (not asset.is_relative_to(root) or not asset.is_file()
                or asset.stat().st_size != size
                or hashlib.sha256(asset.read_bytes()).hexdigest() != digest):
                raise RuntimeError("Source-locked study WAV bytes mismatch")
            admitted_wavs.add(rel)
    for wav in root.rglob("*.wav"):
        if wav.relative_to(root).as_posix() not in admitted_wavs:
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
    server=ThreadingHTTPServer((a.bind,a.port),partial(Handler,root=a.root.resolve()))
    server.daemon_threads=True
    print("READY EstateShell SOURCE-LOCKED WLAN ONLY",meta["templateVersion"],flush=True)
    server.serve_forever()
if __name__=="__main__":
    main()
