#!/usr/bin/env python3
"""Independent Mac/WLAN readback for the four-part local Fountain Coach estate."""
import hashlib
import json
import re
from urllib.request import urlopen
from urllib.error import HTTPError

BASE="http://192.168.8.50"
ROOTS={
    "fountain":BASE+":8180/",
    "solstice":BASE+":8181/",
    "teatro":BASE+":8182/",
    "satzfunk":BASE+":8194/",
}

def fetch(url):
    with urlopen(url,timeout=12) as r:
        assert r.status==200,(url,r.status)
        return r.read(),r.headers

def check():
    for site in ("fountain","solstice","teatro"):
        payload,head=fetch(ROOTS[site]+"__stage/health")
        j=json.loads(payload)
        assert j["status"]=="ready" and j["productionPublished"] is False
        assert "noindex" in head.get("X-Robots-Tag","")
        assert set(j["sites"])=={"fountain","solstice","teatro"}
    expected={
        "fountain":3,
        "teatro":4,
    }
    for site,count in expected.items():
        b,_=fetch(ROOTS[site])
        html=b.decode()
        assert 'data-book-count="'+str(count)+'"' in html
        assert html.count('class="shelf-item"')==count
        assert html.count('class="shelf-book"')==count
        assert html.count('data-book-id="satzfunk"')==1
        assert html.count('data-preview-host="satzfunk"')==1
        assert 'href="'+ROOTS["satzfunk"]+'"' in html
        assert "http://192.168.8.249:" not in html
    covers=[]
    for origin,asset in (("fountain","assets/estate-bookshelf/satzfunk-archive.svg"),
                         ("teatro","assets/bookshelf/satzfunk-archive.svg")):
        body,_=fetch(ROOTS[origin]+asset)
        assert b"<svg" in body and b"Satzfunk" in body
        covers.append(hashlib.sha256(body).hexdigest())
    assert covers[0]==covers[1]
    for url in (ROOTS["fountain"]+"editions/essays/",
                ROOTS["solstice"]+"editions/first-reading/",
                ROOTS["teatro"]+"editions/first-hearing/"):
        page,_=fetch(url)
        assert b'data-estate-id="satzfunk"' in page,url
        assert b"http://192.168.8.50:8194/" in page,url
        assert b"http://192.168.8.249:" not in page,url
    for path in ("","catalog.json","media/40389.mp4","7vst-originals.html",
                 "text/7vst-reverse/1.json"):
        try:
            fetch(ROOTS["satzfunk"]+path)
            raise AssertionError("Anonymous private archive route exposed: "+path)
        except HTTPError as e:
            assert e.code==403,(path,e.code)
    return {"status":"pass","hosts":ROOTS,"bookCounts":expected,
            "sourceCoverSha256":covers[0],
            "privateArchiveUnauthenticated":"403",
            "productionPublished":False,
            "localArchivePlayback":"verified separately by owning suite"}

if __name__=="__main__":
    print(json.dumps(check(),indent=2))
