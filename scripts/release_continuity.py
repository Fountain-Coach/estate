#!/usr/bin/env python3
"""Version-pinned, source-preserving, browser-state-aware local estate releases.

Build and serve are distinct. Serving is read-only except for the independently
maintained atomic 'current' symlink. No DNS, production route, Store, credentials,
user session or private archive media can be mutated here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html import escape

SCHEMA = "fountain.estate.release-continuity.v1"
IDENTITIES = ("estate/index.html", "teatro/index.html",
              "solstice/editions/first-reading/index.html")
ASSETS = ("estate-shell.css", "estate-shell-state.js",
          "estate-shell-stage-nav.js", "estate-shell-logo.png",
          "estate-release-continuity.js")
ID = re.compile(r"^[a-f0-9]{64}$")

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def tree_digest(root: Path) -> str:
    items = []
    for file in sorted(root.rglob("*")):
        if file.is_file():
            items.append([file.relative_to(root).as_posix(), sha(file.read_bytes())])
    return sha(json.dumps(items, separators=(",", ":"), ensure_ascii=True).encode())

def verify_original_stage(original: Path):
    data = json.loads((original/"source-lock.json").read_text())
    if (data.get("status") != "WLAN-PREVIEW-NOT-PUBLIC" or
        data.get("authorPublished") is not False or
        data.get("archiveMediaCopied") is not False or
        data.get("releaseReceipt") is not None or
        set(data.get("sites", {})) != {"estate", "solstice", "teatro"}):
        raise ValueError("not an admitted private shell stage")
    for path in IDENTITIES:
        if not (original/path).is_file(): raise ValueError("missing source page: " + path)
    if any(original.rglob("*.mp4")) or any(original.rglob("*.wav")):
        raise ValueError("private audio/video must not enter estate stage")
    return data

def make_release(source: Path, store: Path, continuity_js: Path, purpose: str):
    source = source.resolve(strict=True)
    verify_original_stage(source)
    if not re.fullmatch(r"[a-z0-9-]{3,50}", purpose):
        raise ValueError("release purpose invalid")
    origin_digest = tree_digest(source)
    javascript = continuity_js.read_bytes()
    bundle = {
        key: (javascript if key == "estate-release-continuity.js"
              else (source/"assets"/key).read_bytes())
        for key in ASSETS
    }
    release_id = sha(json.dumps({"sourceTree":origin_digest,"purpose":purpose,
                                "assets":{k:sha(v) for k,v in bundle.items()}},
                               sort_keys=True, separators=(",",":")).encode())
    releases = store/"releases"
    target = releases/release_id
    if target.exists(): raise ValueError("immutable release already exists")
    releases.mkdir(parents=True,exist_ok=True)
    shutil.copytree(source, target, symlinks=False)
    for key,data in bundle.items():
        folder = target/"__estate_assets"
        folder.mkdir(exist_ok=True)
        (folder/key).write_bytes(data)
    page_proofs = {}
    stage_ip = "http://192.168.8.50:8200/"
    for rel in IDENTITIES:
        page = target/rel
        content = page.read_text()
        if 'data-estate-release=' in content: raise ValueError("already versioned")
        if "<html" not in content or "</head>" not in content:
            raise ValueError("invalid owner document")
        content = content.replace("<html", '<html data-estate-release="'+release_id+'"', 1)
        for asset in ASSETS[:-1]:
            content = content.replace('/assets/'+asset,
                '/__estate/'+release_id+'/'+asset)
        # Explicitly reroute only pre-admitted local links; never mutate canonical
        # HTTPS identity metadata and never route public domains to private IPs.
        content = content.replace(stage_ip, "http://192.168.8.50:8201/")
        content = content.replace("</head>", '<script defer src="/__estate/'+release_id+
            '/estate-release-continuity.js"></script></head>', 1)
        page.write_text(content)
        page_proofs[rel] = sha(content.encode())
    manifest = {
        "schema": SCHEMA, "releaseId": release_id,
        "purpose": purpose, "originTreeSHA256":origin_digest,
        "publicPublished": False, "archiveMediaCopied": False,
        "templateVersion": "fountain.estate.shell.v1-candidate-20261022",
        "assetsSHA256":{k:sha(v) for k,v in bundle.items()},
        "pagesSHA256":page_proofs
    }
    (target/"release-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    verify_release(store, release_id)
    return manifest

def verify_release(store: Path, release_id: str):
    if not ID.fullmatch(release_id): raise ValueError("invalid immutable release id")
    root = store/"releases"/release_id
    if not root.is_dir() or root.is_symlink(): raise ValueError("missing release")
    m = json.loads((root/"release-manifest.json").read_text())
    if (m.get("schema")!=SCHEMA or m.get("releaseId")!=release_id or
        m.get("publicPublished") is not False or m.get("archiveMediaCopied") is not False):
        raise ValueError("release manifest incompatible")
    verify_original_stage(root)
    for asset,digest in m["assetsSHA256"].items():
        if asset not in ASSETS or sha((root/"__estate_assets"/asset).read_bytes())!=digest:
            raise ValueError("asset digest mismatch: "+asset)
    if set(m["pagesSHA256"])!=set(IDENTITIES):
        raise ValueError("release page inventory drift")
    for page,digest in m["pagesSHA256"].items():
        if sha((root/page).read_bytes())!=digest:
            raise ValueError("HTML digest mismatch: "+page)
    return m

def current_release(store: Path):
    pointer = store/"current"
    if not pointer.is_symlink(): raise ValueError("no atomic release pointer")
    target = pointer.readlink()
    if target.parts != ("releases", target.name) or not ID.fullmatch(target.name):
        raise ValueError("unexpected release pointer")
    return verify_release(store,target.name)

class Handler(SimpleHTTPRequestHandler):
    server_version="FountainEstateReleaseContinuity/1"
    def __init__(self,*args,store:Path,**kwargs):
        self.store=store
        self._immutable=False
        self._release=None
        super().__init__(*args,directory=str(store),**kwargs)
    def list_directory(self,path):
        self.send_error(404,"Directory listings disabled");return None
    def translate_path(self,path):
        p=unquote(urlsplit(path).path)
        if p.startswith("/__estate/"):
            sections=p.strip("/").split("/")
            if len(sections)!=3 or sections[0]!="__estate" or not ID.fullmatch(sections[1]) or sections[2] not in ASSETS:
                return str(self.store/"__denied")
            self._immutable=True
            self._release=sections[1]
            return str(self.store/"releases"/sections[1]/"__estate_assets"/sections[2])
        # No release/manifests or internal browser evidence on the public preview.
        segments=Path(p).parts
        if any(x in ("release-manifest.json","source-lock.json","contract.json",
                     "__estate_assets","releases",".git","current") for x in segments):
            return str(self.store/"__denied")
        m=current_release(self.store)
        self._release=m["releaseId"]
        rel=p.lstrip("/")
        if not rel: rel="estate/index.html"
        elif p.endswith("/"):rel+="index.html"
        resolved=(self.store/"releases"/self._release/rel).resolve()
        parent=(self.store/"releases"/self._release).resolve()
        if not resolved.is_relative_to(parent):return str(self.store/"__denied")
        return str(resolved)
    def end_headers(self):
        if self._release: self.send_header("X-Estate-Release",self._release)
        if self._immutable:
            self.send_header("Cache-Control","public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control","no-store, max-age=0")
        self.send_header("X-Robots-Tag","noindex, nofollow")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Referrer-Policy","no-referrer")
        super().end_headers()
    def _handle(self,head=False):
        if urlsplit(self.path).path=="/__estate/current.json":
            try:
                m=current_release(self.store)
                data=json.dumps({"schema":SCHEMA,"releaseId":m["releaseId"],
                                "templateVersion":m["templateVersion"],
                                "publicPublished":False}).encode()
            except (OSError,ValueError,KeyError) as exc:
                self.send_error(503,"Unverified release authority");return
            self.send_response(200);self.send_header("Content-Type","application/json")
            self.send_header("X-Estate-Authority","source-locked")
            self.send_header("X-Estate-Release",m["releaseId"])
            self.send_header("Content-Length",str(len(data)))
            self.send_header("Cache-Control","no-store, max-age=0")
            self.send_header("X-Robots-Tag","noindex,nofollow")
            self.end_headers()
            if not head:self.wfile.write(data)
            return
        try:
            super().do_HEAD() if head else super().do_GET()
        except (OSError,ValueError,KeyError):
            self.send_error(503,"Unverified release authority")
    def do_GET(self):self._handle()
    def do_HEAD(self):self._handle(head=True)

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd",required=True)
    build=sub.add_parser("build")
    build.add_argument("--source",required=True,type=Path)
    build.add_argument("--store",required=True,type=Path)
    build.add_argument("--javascript",required=True,type=Path)
    build.add_argument("--purpose",required=True)
    serve=sub.add_parser("serve")
    serve.add_argument("--store",required=True,type=Path)
    serve.add_argument("--host",default="192.168.8.50")
    serve.add_argument("--port",type=int,default=8201)
    verify=sub.add_parser("verify")
    verify.add_argument("--store",required=True,type=Path)
    args=p.parse_args()
    if args.cmd=="build":
        print(json.dumps(make_release(args.source,args.store,args.javascript,args.purpose),indent=2))
    elif args.cmd=="verify":
        print(json.dumps(current_release(args.store),indent=2))
    else:
        current_release(args.store)
        server=ThreadingHTTPServer((args.host,args.port),partial(Handler,store=args.store.resolve()))
        server.daemon_threads=True
        print("READY version-locked estate staging",args.host,args.port,flush=True)
        server.serve_forever()
if __name__=="__main__":main()
