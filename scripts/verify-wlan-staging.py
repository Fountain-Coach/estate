#!/usr/bin/env python3
"""Read-only admission proof for Ubuntu WLAN three-front staging.

Tests user-facing URLs, static assets, local navigation, source provenance,
noindex/no-cache and the separation from production publication.
"""
from __future__ import annotations

import json
import re
from urllib.request import Request, urlopen

IP = "192.168.8.249"
ROOTS = {
    "fountain": f"http://{IP}:8180/",
    "solstice": f"http://{IP}:8181/",
    "teatro": f"http://{IP}:8182/",
}
NAV = re.compile(r'<nav\b[^>]*class="[^"]*\bestate-nav\b[^"]*"[^>]*>.*?</nav>', re.S)
IDS = ["estate", "first-reading", "teatro"]
HREFS = [
    ROOTS["fountain"],
    ROOTS["solstice"] + "editions/first-reading/",
    ROOTS["teatro"],
]

def fetch(url):
    with urlopen(Request(url, headers={"Cache-Control": "no-cache"}), timeout=18) as response:
        body = response.read()
        assert response.status == 200, (url, response.status)
        assert response.headers.get("X-Robots-Tag", "").startswith("noindex"), url
        return body, response.headers

def test():
    for host, root in ROOTS.items():
        raw, _ = fetch(root + "__stage/health")
        state = json.loads(raw)
        assert state["status"] == "ready"
        assert state["productionPublished"] is False
        assert set(state["sites"]) == set(ROOTS)
        assert state["sites"][host]["repository"] == {
            "fountain":"Fountain-Coach/fountain.coach",
            "solstice":"Fountain-Coach/solstice.fountain.coach",
            "teatro":"Fountain-Coach/teatro.fountain.coach",
        }[host]
        assert re.fullmatch(r"[a-f0-9]{40}",state["sites"][host]["commit"])
        html, _ = fetch(root)
        document = html.decode("utf-8")
        if host == "fountain":
            assert document.count('data-book-chapter=')==3, "Fountain must open the complete essays Linotype reader"
            assert 'id="book-viewport"' in document and 'id="book-contents"' in document
            cover=re.search(r'<section\b[^>]*class="[^"]*book-cover[^"]*"[^>]*>.*?</section>',document,re.S)
            assert cover is not None, "Missing reader cover"
            for ident,target in (("first-reading",HREFS[1]),("teatro",HREFS[2])):
                anchor=re.search(r'<a\b[^>]*data-estate-id="'+ident+r'"[^>]*>',cover.group())
                assert anchor is not None and 'href="'+target+'"' in anchor.group(),ident
            essays,_=fetch(root+"essays/")
            nav=NAV.search(essays.decode()).group()
        else:
            nav=NAV.search(document).group()
        assert re.findall(r'data-estate-id="([^"]+)"', nav) == IDS, host
        for ident,target in zip(IDS,HREFS):
            anchor=re.search(r'<a\b[^>]*data-estate-id="'+ident+r'"[^>]*>',nav)
            assert anchor is not None and 'href="'+target+'"' in anchor.group(),(host,ident)
        assert 'data-estate-id="status"' not in nav
        assert 'data-legal-role="company-status"' in document,host
        print("PASS",host,"three-front-links","company-status-footer")
    book, _ = fetch(ROOTS["solstice"]+"editions/first-reading/")
    for token in (b'id="book-viewport"',b'id="book-next"',b'id="book-page-count"',
                  b'mobile-page-navigation.js',b'linotype-engine.js',b'assets/book.js'):
        assert token in book, token
    assets = {
        "fountain": ["assets/linotype/book.css","assets/linotype/book.js",
                     "assets/linotype/linotype-engine.js","assets/linotype/mobile-page-navigation.js",
                     "assets/linotype/essays.css"],
        "solstice": ["assets/book.css","assets/book.js","assets/linotype-engine.js",
                     "assets/mobile-page-navigation.js","assets/mobile-page-navigation.css"],
        "teatro": ["assets/estate-core.css","assets/estate-core.js","assets/index-CY5_5ULO.js"],
    }
    for host, files in assets.items():
        for path in files:
            contents, _ = fetch(ROOTS[host]+path)
            assert len(contents)>0, (host,path)
        print("PASS",host,len(files),"real source assets")
    print("THREE_FRONT_WLAN_STAGE_PASS",HREFS)

if __name__=="__main__":
    test()
