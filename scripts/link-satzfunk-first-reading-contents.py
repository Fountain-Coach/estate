#!/usr/bin/env python3
"""Link First Reading to Satzfunk through its existing Contents dialog only.

This changes a disposable WLAN release, not the original Solstice book, its
prose, score, pagination, art, production routes or public release.
"""
import argparse
import json
from pathlib import Path

STAGING=Path("/home/benedikt/estate-three-front-staging")
LINK='''<p class="book-contents-satzfunk">Other hearings: <a data-estate-id="satzfunk" href="http://192.168.8.50:8194/" aria-label="Satzfunk, protected audiovisual radio">Satzfunk — audiovisual radio ↗</a></p>
'''

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--release",type=Path,required=True)
    a=p.parse_args()
    root=a.release.resolve()
    if root.parent != STAGING / "releases":
        raise SystemExit("Refusing non-staging path")
    path=root/"solstice/editions/first-reading/index.html"
    html=path.read_text()
    if 'data-estate-id="satzfunk"' in html:
        print("Already linked")
        return
    marker='<dialog id="book-contents"'
    start=html.find(marker)
    if start<0:
        raise SystemExit("Missing real First Reading Contents dialog")
    stop=html.find("</dialog>",start)
    if stop<0 or '<nav aria-label="Chapters">' not in html[start:stop]:
        raise SystemExit("Contents structure mismatch")
    proposed=html[:stop]+LINK+html[stop:]
    assert proposed.count('data-book-chapter=')==html.count('data-book-chapter=')
    assert proposed.count('class="book-toc-list"')==html.count('class="book-toc-list"')
    assert proposed.count('src="../../assets/')==html.count('src="../../assets/')
    path.write_text(proposed)
    lock=root/"source-lock.json"
    j=json.loads(lock.read_text())
    j["localEstateAddition"]["firstReadingLink"]="Contents dialog, source book unchanged"
    lock.write_text(json.dumps(j,indent=2)+"\n")
    print("Satzfunk linked inside existing First Reading Contents, staging only")

if __name__=="__main__":
    main()
