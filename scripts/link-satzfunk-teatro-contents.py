#!/usr/bin/env python3
"""Stage-only Teatro Contents link to the authenticated Satzfunk archive."""
import argparse
import json
from pathlib import Path

ROOT=Path("/home/benedikt/estate-three-front-staging")
LINK='<p class="book-contents-satzfunk">Other performances: <a data-estate-id="satzfunk" href="http://192.168.8.50:8194/" aria-label="Satzfunk, protected audiovisual radio">Satzfunk — audiovisual radio ↗</a></p>\n'
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--release",type=Path,required=True)
    x=a.parse_args()
    base=x.release.resolve()
    if base.parent!=ROOT/"releases":
        raise SystemExit("Not a disposable WLAN release")
    path=base/"teatro/editions/first-hearing/index.html"
    before=path.read_text()
    if 'data-estate-id="satzfunk"' in before:
        print("Already linked");return
    start=before.find('<dialog id="book-contents"')
    stop=before.find("</dialog>",start)
    if start<0 or stop<0 or '<nav aria-label="Chapters">' not in before[start:stop]:
        raise SystemExit("Teatro's actual Contents structure changed")
    after=before[:stop]+LINK+before[stop:]
    for tag in ('data-book-chapter=','data-press-media=','data-teatro-book-stage','id="book-media-toggle"'):
        if after.count(tag)!=before.count(tag):
            raise SystemExit("Authorial content changed: "+tag)
    path.write_text(after)
    lock=base/"source-lock.json"
    j=json.loads(lock.read_text())
    j["localEstateAddition"]["teatroLink"]="Contents dialog, score and sound unchanged"
    lock.write_text(json.dumps(j,indent=2)+"\n")
    print("Satzfunk linked in Teatro Contents; original score and audio controls unchanged")
if __name__=="__main__":
    main()
