#!/usr/bin/env python3
"""R28 refinement: the source-owned open-hand always returns to Reader root.

Pin exact immutable v62 source bytes; preserve originals; derive v63 as a
private WLAN candidate without new rendering, book admission or DNS mutation.
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

PREDECESSOR = "shared-shell-20261029-v62-reframe-r28-20015e9"
EXPECTED = {
    "estate/index.html": "d63e00a2117a3760b3137cb6a8e5b89ac2dd842fbcac2aeb363e556c022119a0",
    "estate/editions/index.html": "d63e00a2117a3760b3137cb6a8e5b89ac2dd842fbcac2aeb363e556c022119a0",
    "estate/editions/essays-continuing/index.html": "dca55623d8e558b14286567b1998536bddf8d9e5585c6e2181e53e602cf2fbf5",
    "estate/collections/first-readings/index.html": "5bc208b859d524b967d4d01800ee026e1fd269a05c6485e17cc4327314d7c3d3",
    "estate/assets/linotype/reframe-reader-r28.css": "16cfe681fdf1fe4e154568022663635175547c2bcb6323df197a97a769c00aff",
}
CHILD_READER = "estate/editions/essays/teatro-an-unfinished-composition/index.html"
ROOT = "/estate/"
ART = "/estate/assets/fountain-coach-logo-transparent.png"
ACCESSIBLE = "Go to Reader root — Bookshelf"
ORIGINAL_MARK = (
    '<header class="bookshelf-brand fc-identity-circle">'
    '<img alt="Fountain Coach — open hand with spring" height="124" '
    'src="/estate/assets/fountain-coach-logo-transparent.png" width="124"/>'
    '</header>'
)
ACTION_MARK = (
    '<header class="bookshelf-brand fc-identity-circle">'
    '<a class="publisher-circle-return" href="/estate/" '
    'aria-label="Go to Reader root — Bookshelf" title="Bookshelf">'
    '<img alt="" height="124" '
    'src="/estate/assets/fountain-coach-logo-transparent.png" width="124"/>'
    '</a></header>'
)
FIRST_COLLECTION_BACK = (
    '<header class="bookshelf-collection-masthead">'
    '<a aria-label="Return to Fountain Coach bookshelf" href="/estate/">'
    '← FOUNTAIN COACH</a><h1>First Readings</h1></header>'
)
FIRST_COLLECTION_HEADING = (
    '<header class="bookshelf-collection-masthead"><h1>First Readings</h1></header>'
)
BOOK_ACTION = (
    '<a aria-label="Go to Reader root — Bookshelf" class="book-back book-root-hand" '
    'href="/estate/" title="Bookshelf">'
    '<img src="/estate/assets/fountain-coach-logo-transparent.png" width="32" height="32" alt=""/>'
    '</a>'
)
ESSAYS_BACK = (
    '<a aria-label="Return to the Bookshelf" class="book-back" href="/estate/">'
    '<span aria-hidden="true">←</span><span>Bookshelf</span></a>'
)
FIRST_READING_BACK = (
    '<a aria-label="Back to First Readings" class="book-back" '
    'href="/estate/collections/first-readings/">'
    '<span aria-hidden="true">←</span><span>First Readings</span></a>'
)
CSS_ADDITIONS = """\n/* Source-owned open hand is the sole obvious return-to-root control. */
.bookshelf-brand .publisher-circle-return{
  display:grid;place-items:center;width:100%;height:100%;
  min-width:44px;min-height:44px;border-radius:inherit;
  color:inherit;text-decoration:none;cursor:pointer;
}
.bookshelf-brand .publisher-circle-return img{pointer-events:none}
.bookshelf-brand .publisher-circle-return:focus-visible{
  outline:3px solid var(--ink);outline-offset:4px;
}
.book-toolbar .book-root-hand{
  display:grid;place-items:center;width:44px;height:44px;min-width:44px;
  max-width:44px;border:1px solid var(--book-rule);
  border-radius:50%;text-decoration:none;
}
.book-toolbar .book-root-hand img{width:32px;height:32px;object-fit:contain}
.book-toolbar .book-root-hand:focus-visible{
  outline:3px solid currentColor;outline-offset:3px;
}
@media(hover:hover){
  .bookshelf-brand .publisher-circle-return:hover{background:#2925200a}
  .book-toolbar .book-root-hand:hover{background:#2925200a}
}
"""

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def once(source: str, former: str, revised: str, what: str) -> str:
    count=source.count(former)
    if count != 1:
        raise ValueError(f"{what}: expected once, found {count}")
    return source.replace(former,revised,1)

def prepare(args: argparse.Namespace) -> dict:
    root=Path(args.stage_root).resolve(strict=True)
    active=(root/"current").resolve(strict=True)
    if active.name!=PREDECESSOR or active.parent!=(root/"releases"):
        raise RuntimeError(f"Stage predecessor changed: {active}")
    if not re.fullmatch(r"shared-shell-20261029-v63-reframe-hand-[a-z0-9]{7}",args.release_id):
        raise ValueError("Release ID is not an explicitly scoped v63")
    destination=root/"releases"/args.release_id
    if destination.exists():
        raise FileExistsError(f"Immutable candidate exists: {destination}")
    for relative,expected in EXPECTED.items():
        digest=sha(active/relative)
        if digest!=expected:
            raise RuntimeError(f"Source changed: {relative} ({digest})")
    if not (active/CHILD_READER).is_file():
        raise FileNotFoundError("First Readings child reader missing")
    if not (active/"estate/assets/fountain-coach-logo-transparent.png").is_file():
        raise FileNotFoundError("Original open-hand asset missing")
    updates={}
    for name in ["estate/index.html","estate/editions/index.html"]:
        original=(active/name).read_text()
        modified=once(original,ORIGINAL_MARK,ACTION_MARK,f"{name} root mark")
        if "fc-shell-reel" in modified or modified.count(ACCESSIBLE)!=1:
            raise ValueError(f"Root navigation not source-faithful: {name}")
        updates[name]=modified
    if updates["estate/index.html"]!=updates["estate/editions/index.html"]:
        raise ValueError("The same publication has diverging entrance bytes")
    collection_rel="estate/collections/first-readings/index.html"
    collection=(active/collection_rel).read_text()
    collection=once(collection,ORIGINAL_MARK,ACTION_MARK,"First Readings mark")
    collection=once(collection,FIRST_COLLECTION_BACK,FIRST_COLLECTION_HEADING,
                    "remove competing collection arrow")
    if collection.count(ACCESSIBLE)!=1:
        raise ValueError("First Readings needs one open-hand root link")
    updates[collection_rel]=collection
    essays_rel="estate/editions/essays-continuing/index.html"
    essays=once((active/essays_rel).read_text(),ESSAYS_BACK,BOOK_ACTION,
                "Essays toolbar root hand")
    if essays.count('data-book-chapter=')!=7 or "essays-continuing-20261029" not in essays:
        raise ValueError("Source-bound seven-essay work changed")
    updates[essays_rel]=essays
    child=(active/CHILD_READER).read_text()
    child=once(child,FIRST_READING_BACK,BOOK_ACTION,
               "First Reading book toolbar root hand")
    if child.count('id="book-viewport"')!=1:
        raise ValueError("First Reading child compositor missing")
    # The child shares the already staged book CSS and must load the
    # root-action CSS without modifying its source, artwork, or measurements.
    if 'reframe-reader-r28.css' not in child:
        child=once(child,'</head>',
                   '<link href="/estate/assets/linotype/reframe-reader-r28.css" rel="stylesheet"/></head>',
                   "child root mark CSS")
    updates[CHILD_READER]=child
    css_rel="estate/assets/linotype/reframe-reader-r28.css"
    css=(active/css_rel).read_text()+CSS_ADDITIONS
    updates[css_rel]=css
    try:
        shutil.copytree(active,destination,symlinks=True)
        for rel,content in updates.items():
            (destination/rel).write_text(content)
        results={rel:sha(destination/rel) for rel in updates}
        # Guard against side effects on media, source identity, cover artwork,
        # and the original Press collection source record.
        preserved=[
            "estate/assets/linotype/bookshelf.css",
            "estate/assets/linotype/book.css",
            "estate/assets/linotype/book.js",
            "estate/collections/first-readings/collection.json",
            "estate/assets/fountain-coach-logo-transparent.png",
            "estate/assets/estate-bookshelf/fountain-coach-edition.png",
            "estate/assets/estate-bookshelf/first-reading-ink.png",
            "source-lock.json", # compared before recording v63
        ]
        for rel in preserved:
            if sha(active/rel)!=sha(destination/rel):
                raise RuntimeError(f"Unintended source or media change: {rel}")
        lock=json.loads((destination/"source-lock.json").read_text())
        original=lock.get("reframeFirstReaderR28")
        if not original or original.get("release")!=PREDECESSOR:
            raise RuntimeError("Missing authoritative R28 predecessor evidence")
        evidence={
            "schema":"fountain.reframe.open-hand-reader-root.v1",
            "status":"immutable-WLAN-candidate-not-public",
            "release":args.release_id,
            "predecessor":PREDECESSOR,
            "rootRoute":ROOT,
            "rootHandMeaning":"Go to Reader root — Bookshelf",
            "pressCanonicalSource":"Fountain-Coach/fountain-press/runtime/bookshelf.py",
            "unchangedOriginalMark":ART,
            "changedFiles":list(updates),
            "originalSHA256":{rel:sha(active/rel) for rel in updates},
            "candidateSHA256":results,
            "originalEssayChapters":7,
            "noNewSourceAdmissions":True,
            "noPublicDomainMutation":True,
            "browserAcceptance":"pending"
        }
        lock["reframeRootHandV63"]=evidence
        (destination/"source-lock.json").write_text(json.dumps(lock,indent=2,ensure_ascii=False)+"\n")
        return evidence
    except Exception:
        shutil.rmtree(destination,ignore_errors=True)
        raise

def activate(args: argparse.Namespace) -> dict:
    root=Path(args.stage_root).resolve(strict=True)
    active=(root/"current").resolve(strict=True)
    if active.name!=PREDECESSOR:raise RuntimeError("Staging predecessor changed")
    release=root/"releases"/args.release_id
    record=json.loads((release/"source-lock.json").read_text()).get("reframeRootHandV63")
    if not record or record["predecessor"]!=active.name:
        raise RuntimeError("Candidate source identity mismatch")
    for path,digest in record["candidateSHA256"].items():
        if sha(release/path)!=digest:raise RuntimeError(f"Modified immutable artifact: {path}")
    pending=root/"current.r28-hand-next"
    if pending.exists() or pending.is_symlink():raise FileExistsError("Unexpected pending activation")
    pending.symlink_to(Path("releases")/release.name)
    os.replace(pending,root/"current")
    return {"active":release.name,"predecessor":active.name,"readbackRequired":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage-root",required=True)
    p.add_argument("--release-id",required=True)
    p.add_argument("--activate",action="store_true")
    args=p.parse_args()
    print(json.dumps(activate(args) if args.activate else prepare(args),ensure_ascii=False,indent=2))

if __name__=="__main__":
    try:main()
    except Exception as err:
        print(f"R28_HAND_REFUSED {type(err).__name__}: {err}",file=sys.stderr)
        sys.exit(2)
