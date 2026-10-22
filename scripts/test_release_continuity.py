#!/usr/bin/env python3
"""Deterministic positive/negative tests for release continuity, no browser matrix."""
import json
import tempfile
import threading
import unittest
from functools import partial
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_continuity import (
    make_release, verify_release, current_release, Handler, ThreadingHTTPServer, ASSETS
)
TEMPLATE = """<!doctype html><html lang="en"><head>
<link rel="stylesheet" href="/assets/estate-shell.css">
<script defer src="/assets/estate-shell-state.js"></script>
<script defer src="/assets/estate-shell-stage-nav.js"></script></head>
<body><header><img src="/assets/estate-shell-logo.png"></header>
<main>Original authorial work remains unchanged.</main>
<a href="http://192.168.8.50:8200/estate/" data-stage-binding="wlan-only">Estate</a>
</body></html>"""

class Continuity(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)
        self.source=self.path/"source";self.source.mkdir()
        (self.source/"assets").mkdir()
        for asset in ASSETS:
            if asset=="estate-release-continuity.js":continue
            (self.source/"assets"/asset).write_bytes(("ASSET-"+asset).encode())
        self.js=self.path/"continuity.js";self.js.write_text("/* integrity fixture */")
        for file in ("estate/index.html","teatro/index.html",
                     "solstice/editions/first-reading/index.html"):
            f=self.source/file;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(TEMPLATE)
        (self.source/"source-lock.json").write_text(json.dumps({
          "status":"WLAN-PREVIEW-NOT-PUBLIC","authorPublished":False,
          "archiveMediaCopied":False,"releaseReceipt":None,
          "sites":{"estate":{}, "teatro":{}, "solstice":{}}
        }))
        self.store=self.path/"store"

    def release(self,purpose):
        return make_release(self.source,self.store,self.js,purpose)["releaseId"]

    def activate(self,release):
        pointer=self.store/"current"
        if pointer.is_symlink():pointer.unlink()
        pointer.symlink_to("releases/"+release)

    def test_two_immutable_releases_and_atomic_pointer(self):
        a=self.release("initial-proof")
        b=self.release("fresh-proof")
        self.assertNotEqual(a,b)
        self.activate(a);self.assertEqual(current_release(self.store)["releaseId"],a)
        old=(self.store/"releases"/a/"estate/index.html").read_bytes()
        self.activate(b);self.assertEqual(current_release(self.store)["releaseId"],b)
        self.assertEqual((self.store/"releases"/a/"estate/index.html").read_bytes(),old)
        self.assertIn(("/__estate/"+a+"/estate-shell.css").encode(),old)

    def test_fresh_html_has_explicit_release(self):
        a=self.release("fresh-proof")
        html=(self.store/"releases"/a/"estate/index.html").read_text()
        self.assertIn('data-estate-release="'+a+'"',html)
        self.assertIn('/__estate/'+a+'/estate-release-continuity.js',html)
        self.assertIn('http://192.168.8.50:8201/estate/',html)
        self.assertNotIn('http://192.168.8.50:8200/estate/',html)

    def test_corrupted_file_fails_closed(self):
        a=self.release("fresh-proof");self.activate(a)
        (self.store/"releases"/a/"__estate_assets"/"estate-shell.css").write_text("tampered")
        with self.assertRaisesRegex(ValueError,"asset digest mismatch"):
            current_release(self.store)

    def test_unadmitted_source_refused(self):
        (self.source/"source-lock.json").write_text('{"status":"public"}')
        with self.assertRaisesRegex(ValueError,"not an admitted"):
            self.release("fresh-proof")

    def test_media_rejected(self):
        (self.source/"private.wav").write_bytes(b"danger")
        with self.assertRaisesRegex(ValueError,"private audio"):
            self.release("fresh-proof")

    def test_invalid_current_pointer_rejected(self):
        self.release("fresh-proof")
        (self.store/"current").symlink_to("/etc/passwd")
        with self.assertRaises(ValueError):
            current_release(self.store)

    def test_actual_http_cache_contract_and_stale_reply(self):
        a=self.release("one-release")
        b=self.release("two-release")
        self.activate(a)
        server=ThreadingHTTPServer(("127.0.0.1",0),partial(Handler,store=self.store))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        root=f"http://127.0.0.1:{server.server_port}"
        def get(path):
            with urlopen(Request(root+path,headers={"Cache-Control":"no-cache"}),timeout=5) as resp:
                return resp.status,dict(resp.headers.items()),resp.read()
        code,head,html=get("/estate/")
        self.assertEqual(code,200)
        self.assertEqual(head["Cache-Control"],"no-store, max-age=0")
        self.assertEqual(head["X-Estate-Release"],a)
        self.assertIn(a.encode(),html)
        code,head,payload=get("/__estate/"+a+"/estate-shell.css")
        self.assertEqual(code,200)
        self.assertIn("immutable",head["Cache-Control"])
        code,head,body=get("/__estate/current.json?probe=unpredictable")
        self.assertEqual(json.loads(body)["releaseId"],a)
        self.assertEqual(head["X-Estate-Authority"],"source-locked")
        self.assertIn("no-store",head["Cache-Control"])
        self.activate(b)
        code,head,body=get("/__estate/current.json?probe=another")
        self.assertEqual(json.loads(body)["releaseId"],b)
        self.assertEqual(head["X-Estate-Release"],b)
        code,head,html=get("/estate/")
        self.assertIn(b.encode(),html)
        code,head,asset=get("/__estate/"+a+"/estate-shell.css")
        self.assertEqual(code,200)
        self.assertIn("immutable",head["Cache-Control"])
        with self.assertRaises(HTTPError) as cm:
            get("/source-lock.json")
        self.assertEqual(cm.exception.code,404)

if __name__=="__main__":unittest.main(verbosity=2)
