#!/usr/bin/env python3
"""R28 v64: make existing Press Bookshelf the entire visible Reader app surface.

Consume exact immutable v63 first Reader proof and the current source-owner
Fountain Press Bookshelf stylesheet. This is a staging-only projection of the
already source-bound Press work/collection, NOT a new renderer or admission.
Only two identical shelf entrances, First Readings shelf, and Press CSS change.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys

PREDECESSOR = "shared-shell-20261029-v63-reframe-hand-29fb917"
EXPECTED = {
    "estate/index.html":"7cc797797a2aa73dc4176036655efefcfe7a85e585d4abb71868c4b3798c4d95",
    "estate/editions/index.html":"7cc797797a2aa73dc4176036655efefcfe7a85e585d4abb71868c4b3798c4d95",
    "estate/collections/first-readings/index.html":"ea2d626ce7b516d6c3ab7864ad2bafb907b301e166cbe26bd6e2613af130f84b",
    "estate/editions/essays-continuing/index.html":"c24303fbe864f48c88c144c06f085f713208475728f8b39512fb1541221b506b",
}
CSS_ROUTE="estate/assets/linotype/bookshelf.css"
NEW_SOURCE_OWNER="Fountain-Coach/fountain-press/runtime/bookshelf.py"
NEW_CSS_OWNER="Fountain-Coach/fountain-press/runtime/bookshelf.css"

def digest(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def literal_once(source:str,old:str,new:str,label:str)->str:
    n=source.count(old)
    if n!=1:
        raise ValueError(f"{label}: expected one match, found {n}")
    return source.replace(old,new,1)

def regex_once(source:str,pattern:str,replacement:str,label:str)->str:
    out,n=re.subn(pattern,replacement,source,count=1,flags=re.DOTALL)
    if n!=1:
        raise ValueError(f"{label}: expected one match, found {n}")
    return out

def make_app_html(source:str,*,collection:bool)->str:
    html=source
    if collection:
        html=regex_once(html,
            r'<header class="fc-estate-shell"[^>]*>.*?</header>\s*',
            "","remove legacy nine-site collection header")
        html=regex_once(html,
            r'<footer class="estate-footer fc-estate-shell"[^>]*>.*?</footer>\s*',
            "","remove legacy collection footer")
        html=literal_once(html,
            '<link href="/assets/estate-shell.css" rel="stylesheet"/>',
            "","drop legacy shell CSS")
        html=literal_once(html,
            '<script defer="" src="/assets/estate-shell-state.js"></script>',
            "","drop legacy shell JS")
        html=literal_once(html,
            '<header class="bookshelf-collection-masthead"><h1>First Readings</h1></header>',
            '<h1 class="press-visually-hidden">First Readings</h1>',
            "replace collection masthead with accessible heading")
        html=literal_once(html,
            'class="book-app bookshelf-state collection-state"',
            'class="book-app bookshelf-state collection-state app-surface"',
            "source-owned collection app mode")
    else:
        html=regex_once(html,
            r'<header class="reframe-reader-heading">.*?</header>\s*<nav aria-label="Reader navigation" class="bookshelf-pathways">.*?</nav>',
            '<h1 class="press-visually-hidden">Bookshelf</h1>',
            "remove website heading and textual nav")
        html=literal_once(html,
            'class="book-app bookshelf-state"',
            'class="book-app bookshelf-state app-surface"',
            "source-owned root app mode")
        html=literal_once(html,
            'class="reframe-reader-footer"',
            'class="reframe-reader-footer press-auxiliary-navigation"',
            "retain accessible credits and rights without website footer")
        for stylesheet in (
            '<link href="/estate/assets/essay-pathways.css" rel="stylesheet"/>',
            '<link href="/estate/assets/linotype/reframe-reader-r28.css" rel="stylesheet"/>',
        ):
            html=literal_once(html,stylesheet,"","remove outdated site layer stylesheet")
    html=literal_once(html, '</head>',
        '<meta name="theme-color" content="#dfd9ce"/></head>',
        "app color matching original Press")
    if html.count('<div class="bookshelf-paper">')!=1:
        raise ValueError("Fountain Press paper grid lost")
    if html.count('class="shelf-item"')!=(1 if collection else 2):
        raise ValueError("Source cover membership changed")
    if html.count('class="bookshelf-empty"')!=20:
        raise ValueError("Fountain Press inert vacancies changed")
    if html.count('Go to Reader root — Bookshelf')!=1:
        raise ValueError("Home hand must be unique")
    if html.count('class="press-visually-hidden"')!=1:
        raise ValueError("Accessible title missing")
    if 'fc-shell-reel' in html or 'reframe-reader-heading' in html or 'bookshelf-pathways' in html or 'bookshelf-collection-masthead' in html:
        raise ValueError("Website furniture has leaked into app surface")
    if 'app-surface' not in html:
        raise ValueError("Press app mode absent")
    if 'href="/estate/editions/essays-continuing/"' not in html and not collection:
        raise ValueError("Existing source-bound Essays opening lost")
    if 'href="/estate/editions/essays/teatro-an-unfinished-composition/"' not in html and collection:
        raise ValueError("Existing First Reading work opening lost")
    return html

def prepare(args:argparse.Namespace)->dict:
    root=Path(args.stage_root).resolve(strict=True)
    current=root/"current"
    active=current.resolve(strict=True)
    if active.name!=PREDECESSOR or active.parent!=root/"releases":
        raise RuntimeError(f"Refuse changed stage predecessor: {active}")
    if not re.fullmatch(r"shared-shell-20261029-v64-reframe-app-[a-z0-9]{7}",args.release_id):
        raise ValueError("Not a bounded immutable v64 name")
    candidate=root/"releases"/args.release_id
    if candidate.exists():
        raise FileExistsError(f"Already built: {candidate}")
    original={rel:digest(active/rel) for rel in EXPECTED}
    for rel,expected in EXPECTED.items():
        if original[rel]!=expected:
            raise RuntimeError(f"Source changed at {rel}: {original[rel]}")
    if not isinstance(args.press_css_sha,str) or len(args.press_css_sha)!=64:
        raise ValueError("Press stylesheet SHA-256 must be pinned")
    press_css=Path(args.press_css).resolve(strict=True)
    if digest(press_css)!=args.press_css_sha:
        raise RuntimeError("Fountain Press source stylesheet SHA drift")
    css=press_css.read_text()
    if ".bookshelf-state.app-surface" not in css or ".press-visually-hidden" not in css:
        raise RuntimeError("No approved Fountain Press app-surface mode in stylesheet")
    if "body.bookshelf-state.app-surface" not in css:
        raise RuntimeError("Press stylesheet lacks immersive body contract")
    lock=json.loads((active/"source-lock.json").read_text())
    previous=lock.get("reframeRootHandV63",{})
    if previous.get("release")!=PREDECESSOR:
        raise RuntimeError("Predecessor source-lock hand proof unavailable")
    updates={}
    updates["estate/index.html"]=make_app_html((active/"estate/index.html").read_text(),collection=False)
    updates["estate/editions/index.html"]=make_app_html((active/"estate/editions/index.html").read_text(),collection=False)
    if updates["estate/index.html"]!=updates["estate/editions/index.html"]:
        raise RuntimeError("The two source-identical Press shelf entrances diverge")
    updates["estate/collections/first-readings/index.html"]=make_app_html(
        (active/"estate/collections/first-readings/index.html").read_text(),
        collection=True)
    unchanged_paths=[
        "estate/assets/estate-bookshelf/fountain-coach-edition.png",
        "estate/assets/estate-bookshelf/first-reading-ink.png",
        "estate/assets/fountain-coach-logo-transparent.png",
        "estate/collections/first-readings/collection.json",
        "estate/editions/essays-continuing/index.html",
        "estate/editions/essays/teatro-an-unfinished-composition/index.html",
        "estate/assets/linotype/book.js",
        "estate/assets/linotype/book.css",
        "estate/assets/linotype/identity-circle.css",
    ]
    for rel in unchanged_paths:
        if not (active/rel).is_file():
            raise FileNotFoundError(f"Required source/media missing: {rel}")
    try:
        shutil.copytree(active,candidate,symlinks=True)
        for rel,html in updates.items():
            (candidate/rel).write_text(html)
        shutil.copyfile(press_css,candidate/CSS_ROUTE)
        for rel in unchanged_paths:
            if digest(active/rel)!=digest(candidate/rel):
                raise RuntimeError(f"Unexpected authored content or media mutation: {rel}")
        output={rel:digest(candidate/rel) for rel in (*updates,CSS_ROUTE)}
        evidence={
            "schema":"fountain.reframe.press-app-surface-wlan.v1",
            "status":"private-WLAN-immutable-candidate-not-public",
            "release":candidate.name,
            "predecessor":PREDECESSOR,
            "bookRoot":"/estate/",
            "publicationSource":"Fountain-Coach/fountain.coach",
            "compositionOwner":NEW_SOURCE_OWNER,
            "stylesOwner":NEW_CSS_OWNER,
            "pressCSSInputSHA256":args.press_css_sha,
            "changedRoutes":list(updates),
            "changedAssets":[CSS_ROUTE],
            "originalRouteSHA256":{rel:original[rel] for rel in updates},
            "newRouteSHA256":output,
            "retainedCoverCount":2,
            "retainedInertVacancies":20,
            "onlyCoverTextVisibleByDefault":True,
            "readerWorksAltered":False,
            "publicDomainsChanged":False,
            "actualIPadSafariAcceptance":"not-performed",
            "browserAcceptance":"pending",
        }
        updated_lock=json.loads((candidate/"source-lock.json").read_text())
        updated_lock["reframeImmersiveReaderV64"]=evidence
        (candidate/"source-lock.json").write_text(json.dumps(updated_lock,indent=2,ensure_ascii=False)+"\n")
        return evidence
    except Exception:
        shutil.rmtree(candidate,ignore_errors=True)
        raise

def activate(args:argparse.Namespace)->dict:
    root=Path(args.stage_root).resolve(strict=True)
    active=(root/"current").resolve(strict=True)
    if active.name!=PREDECESSOR:
        raise RuntimeError("Current staging predecessor changed")
    candidate=root/"releases"/args.release_id
    if not candidate.is_dir():
        raise FileNotFoundError("Nonactive candidate not found")
    evidence=json.loads((candidate/"source-lock.json").read_text()).get("reframeImmersiveReaderV64")
    if not evidence or evidence["predecessor"]!=active.name:
        raise RuntimeError("Mismatch in candidate origin/provenance")
    for rel,expected in evidence["newRouteSHA256"].items():
        if digest(candidate/rel)!=expected:
            raise RuntimeError("Candidate bytes differ from reviewed artifact: "+rel)
    pending=root/"current.r28-app-next"
    if pending.exists() or pending.is_symlink():
        raise FileExistsError("Unexpected pending staging transition")
    pending.symlink_to(Path("releases")/candidate.name)
    os.replace(pending,root/"current")
    return {"activated":candidate.name,"previous":active.name,"restartServingService":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage-root",required=True)
    p.add_argument("--release-id",required=True)
    p.add_argument("--press-css",required=False,default="/home/benedikt/r28_press_app.css")
    p.add_argument("--press-css-sha",default="",help="Pinned exact source-owner CSS digest")
    p.add_argument("--activate",action="store_true")
    args=p.parse_args()
    print(json.dumps(activate(args) if args.activate else prepare(args),indent=2,ensure_ascii=False))

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print(f"R28_APP_REFUSED: {type(exc).__name__}: {exc}",file=sys.stderr)
        sys.exit(2)
