#!/usr/bin/env python3
"""R28: deterministic private-WLAN first Reader projection.

Source: Fountain-Coach/estate/staging/r28_first_reader.py
Consumes the already-staged Fountain Press bookshelf and the already-staged
source-bound seven-essay book. Never fabricates a book, media, or public release.
Builds an immutable copy. Activation is a separate, predecessor-checked option.
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

EXPECTED_ESSAYS_SHA256 = "acc8e540360bb1798e18aa58a2896d608a51e2b1ed93fd9875c9f43eaae5e6bb"
EXPECTED_PRESS_SHELF_SHA256 = "4acb31dbca48c84e129b7677a9d05e3b36f4212aafb6ca633ff016c92a505468"
EXPECTED_COLLECTION_SHA256 = "8cbaa8cf73400602d0d61520f18d3b8f2e7885e2570981e941a6184b29d91314"
# Collection checksum is retrieved live from the v61 stage. Do not infer membership
# from the list of directories; the two source-owned Press cover records are reused.

CSS = r"""/* R28: view-layer arrangement of the existing Fountain Press Bookshelf. */
:root{color-scheme:light}
.reframe-reader-heading{padding:clamp(18px,3vw,34px) 0 clamp(20px,3vw,32px);border-bottom:1px solid var(--rule);margin-bottom:clamp(22px,3vw,34px)}
.reframe-reader-heading .reader-eyebrow{font:600 11px/1.5 ui-monospace,Menlo,monospace;letter-spacing:.11em;color:#665f56;margin:0 0 12px}
.reframe-reader-heading h1{font:400 clamp(40px,6vw,76px)/1.1 "Iowan Old Style",Georgia,serif;letter-spacing:-.045em;margin:0}
.reframe-reader-heading .reader-deck{font:400 clamp(16px,2vw,21px)/1.4 "Iowan Old Style",Georgia,serif;margin:14px 0 0;color:#5b554e}
.reframe-reader-footer{max-width:1320px;margin:0 auto;padding:26px clamp(16px,3vw,44px) 52px;color:#514b43;font:13px/1.7 "Iowan Old Style",Georgia,serif;border-top:1px solid var(--rule)}
.reframe-reader-footer .reader-identities{display:flex;flex-wrap:wrap;gap:6px 24px}
.reframe-reader-footer p{margin:0 0 8px}
.reframe-reader-footer a{color:inherit;text-underline-offset:3px}
.reframe-reader-footer a:focus-visible{outline:2px solid #292520;outline-offset:3px}
.reframe-reader-footer nav{display:flex;gap:6px 18px;flex-wrap:wrap;margin-top:14px}
.bookshelf-main{min-height:0;padding-bottom:clamp(30px,7vw,85px)}
.bookshelf-pathways{font-size:12px}
@media(max-width:720px){.reframe-reader-heading{padding-top:12px}.reframe-reader-footer{padding-bottom:35px}}
@media(prefers-reduced-motion:reduce){.shelf-cover{transition:none!important}}
"""

FOOTER = """<footer class="reframe-reader-footer" aria-label="Publisher and references">
  <div class="reader-identities" id="about">
    <p><strong>Benedikt Eickhoff</strong> · Author</p>
    <p><strong>Fountain Coach</strong> · Publisher of Reframe</p>
  </div>
  <nav aria-label="References and legal notices">
    <a href="https://governance.fountain.coach/">Governance</a>
    <a href="https://midi2.fountain.coach/">MIDI2</a>
    <a href="https://instruments.fountain.coach/">Instruments</a>
    <a href="https://status.fountain.coach/">Status</a>
    <a href="https://governance.fountain.coach/legal/">Legal</a>
    <a href="https://governance.fountain.coach/privacy/">Privacy</a>
    <a href="https://governance.fountain.coach/accessibility/">Accessibility</a>
  </nav>
</footer>"""

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def replace_once(source: str, old: str, new: str, name: str) -> str:
    n = source.count(old)
    if n != 1:
        raise ValueError(f"{name}: expected exactly 1 original, found {n}")
    return source.replace(old, new, 1)

def strip_staged_shell(source: str, *, name: str) -> str:
    html, n = re.subn(r'<header class="fc-estate-shell"\b[^>]*>.*?</header>\s*', '', source, count=1, flags=re.S)
    if n != 1:
        raise ValueError(f"{name}: no uniquely identified legacy shell header")
    html, n = re.subn(r'<footer class="estate-footer fc-estate-shell"\b[^>]*>.*?</footer>\s*', '', html, count=1, flags=re.S)
    if n != 1:
        raise ValueError(f"{name}: no uniquely identified legacy shell footer")
    for asset in (
        r'<link href="/assets/estate-shell.css" rel="stylesheet"\s*/>',
        r'<script defer="" src="/assets/estate-shell-state.js"></script>',
        r'<link href="/estate/assets/estate-core.css" rel="stylesheet"\s*/>',
        r'<script defer="" src="/estate/assets/estate-core.js"></script>',
    ):
        html = re.sub(asset, '', html)
    if '<header class="fc-estate-shell"' in html or '<footer class="estate-footer fc-estate-shell"' in html:
        raise ValueError(f"{name}: legacy global shell survived")
    return html

def make_book(src: str) -> str:
    html = strip_staged_shell(src, name="essays")
    html = replace_once(html,
        '<a aria-label="The complete Essays publication collection" class="book-back" href="/estate/essays/"><span aria-hidden="true">←</span><span>Essays</span></a>',
        '<a aria-label="Return to the Bookshelf" class="book-back" href="/estate/"><span aria-hidden="true">←</span><span>Bookshelf</span></a>',
        "Press book return")
    html = replace_once(html, '<option value="systems">Reframe &amp; estate</option>',
                        '<option value="systems">Reframe &amp; publishing</option>',
                        "semantic sequence label")
    html = html.replace('href="/estate/editions/">Fountain Press editions</a>',
                        'href="/estate/">Bookshelf</a>')
    html = replace_once(html, '<link href="https://fountain.coach/" rel="canonical"/>',
                        '<link href="https://fountain.coach/editions/essays-continuing/" rel="canonical"/>',
                        "future canonical reader identity")
    html = replace_once(html, '</head>',
                        '<link href="/estate/assets/linotype/reframe-reader-r28.css" rel="stylesheet"/></head>',
                        "book CSS")
    if html.count('id="work-the-door-is-a-score"') != 1 or html.count('data-book-chapter=') != 7:
        raise ValueError("Seven original Press essay identities not retained")
    if html.count('class="book-viewport"') != 1 or 'data-edition-id="essays-continuing-20261029"' not in html:
        raise ValueError("Original Linotype engine or edition identity absent")
    if 'aria-label="Estate"' in html or '>Estate</span>' in html:
        raise ValueError("Human-facing retired name remains in book shell")
    return html

def make_shelf(press_html: str, essay_source_revision: str, essay_artifact_sha: str) -> str:
    html = strip_staged_shell(press_html, name="bookshelf")
    html = replace_once(html, "<title>Fountain Coach · Fountain Coach</title>",
                        "<title>Bookshelf · Reframe Reader · Fountain Coach</title>",
                        "Bookshelf title")
    html = replace_once(html, '</head>',
                        '<meta name="author" content="Benedikt Eickhoff"/>'
                        '<meta name="description" content="The Reframe Reader Bookshelf. Books, editions and original works published by Fountain Coach."/>'
                        '<link rel="canonical" href="https://fountain.coach/"/>'
                        '<link href="/estate/assets/linotype/reframe-reader-r28.css" rel="stylesheet"/></head>',
                        "Bookshelf metadata")
    previous_nav = ('<nav aria-label="Writing and instruments" class="bookshelf-pathways">'
                    '<a href="/estate/essays/">Essays</a>'
                    '<a href="/estate/essays/the-ear-that-learns/">The Ear That Learns</a>'
                    '<a href="https://instruments.fountain.coach/">Instruments · Ear &amp; Sing</a></nav>')
    new_head = ( '<header class="reframe-reader-heading">'
        '<p class="reader-eyebrow">FOUNTAIN COACH · REFRAME READER</p>'
        '<h1>Bookshelf</h1>'
        '<p class="reader-deck">Books and editions. Open a work to read.</p>'
        '</header>'
        '<nav aria-label="Reader navigation" class="bookshelf-pathways">'
        '<a href="/estate/" aria-current="page">Bookshelf</a>'
        '<a href="#about">Author</a>'
        '</nav>')
    html = replace_once(html, previous_nav, new_head, "source Press shelf nav")
    html = replace_once(html, 'href="/estate/editions/essays/"',
                        'href="/estate/editions/essays-continuing/"',
                        "Essay cover destination")
    html = replace_once(html, 'data-canonical-href="https://fountain.coach/editions/essays/"',
                        'data-canonical-href="https://fountain.coach/editions/essays-continuing/"',
                        "Essay candidate canonical path")
    html = replace_once(html,
        'aria-label="Open FOUNTAIN COACH · ESSAYS — Fountain Coach; WLAN proofreading"',
        'aria-label="Open Essays — A Book Continually Written; seven source-authored chapters, WLAN candidate"',
        "Essay cover accessibility")
    html, count = re.subn(r'(data-book-id="fountain-coach"[^>]*data-source-revision=")[^"]+"',
                           lambda match: match.group(1)+essay_source_revision+'"',
                           html, count=1)
    if count != 1:
        raise ValueError("First Press cover source revision missing")
    html = replace_once(html, 'id="work-fountain-coach"',
                        f'id="work-fountain-coach" data-reader-artifact-sha256="{essay_artifact_sha}"',
                        "proof binding")
    html = replace_once(html, '</main>', '</main>'+FOOTER, "Bookshelf footer")
    if html.count('class="shelf-item"') != 2:
        raise ValueError("Changed original number of admitted Press covers")
    if 'href="/estate/collections/first-readings/"' not in html:
        raise ValueError("Original First Readings Press collection missing")
    if '>Estate</' in html or 'aria-label="Estate"' in html or '>Editorial</' in html:
        raise ValueError("Retired site categories remain in new Bookshelf")
    return html

def build(args: argparse.Namespace) -> dict:
    stage_root = Path(args.stage_root).resolve()
    current = stage_root / "current"
    active = current.resolve(strict=True)
    if active.name != args.expected_active or active.parent != stage_root / "releases":
        raise RuntimeError(f"Refusing stale/different canonical stage: {active}")
    if "/" in args.release_id or not args.release_id.startswith("shared-shell-20261029-v62-reframe-r28-"):
        raise ValueError("Invalid bounded R28 release ID")
    out = stage_root / "releases" / args.release_id
    if out.exists():
        raise FileExistsError(f"Candidate already exists: {out}")
    old_book = active / "estate" / "index.html"
    old_shelf = active / "estate" / "editions" / "index.html"
    old_collection = active / "estate" / "collections" / "first-readings" / "collection.json"
    originals = {
        "essays": digest(old_book),
        "pressBookshelf": digest(old_shelf),
        "firstReadingsCollection": digest(old_collection),
    }
    if originals["essays"] != EXPECTED_ESSAYS_SHA256 or originals["pressBookshelf"] != EXPECTED_PRESS_SHELF_SHA256:
        raise RuntimeError(f"Changed source artifacts, do not overwrite: {originals}")
    lock = json.loads((active / "source-lock.json").read_text())
    source_record = lock.get("readerFirstStageV59", {})
    if source_record.get("chapterCount") != 7 or source_record.get("sourceOwner") != "Fountain-Coach/fountain.coach":
        raise RuntimeError("Original seven-essay source plan not grounded")
    source_revision = source_record.get("sourceRevision")
    if not isinstance(source_revision, str) or len(source_revision) != 40:
        raise RuntimeError("Unpinned original essay source identity")
    book_html = make_book(old_book.read_text())
    book_sha = hashlib.sha256(book_html.encode()).hexdigest()
    shelf_html = make_shelf(old_shelf.read_text(), source_revision, book_sha)
    try:
        shutil.copytree(active, out, symlinks=True)
        book_target = out / "estate" / "editions" / "essays-continuing" / "index.html"
        book_target.parent.mkdir(parents=True, exist_ok=False)
        book_target.write_text(book_html)
        root_target = out / "estate" / "index.html"
        root_target.write_text(shelf_html)
        # The already published editions address remains an exact alternative
        # entrance to the *same source-compiled* Press Bookshelf, not a second app.
        (out / "estate" / "editions" / "index.html").write_text(shelf_html)
        (out / "estate" / "assets" / "linotype" / "reframe-reader-r28.css").write_text(CSS)
        # Verify all earlier staged routes/media remain byte-for-byte unchanged,
        # except the two explicitly replaced Reader entrances.
        for path in (
            "estate/collections/first-readings/collection.json",
            "estate/assets/linotype/bookshelf.css",
            "estate/assets/linotype/book.js",
            "estate/assets/linotype/living-essays.js",
            "estate/essays/index.html",
            "teatro/index.html",
            "pointer/index.html",
        ):
            old = active / path
            new = out / path
            if old.exists() and digest(old) != digest(new):
                raise RuntimeError(f"Unexpected route/media change: {path}")
        record = {
            "schema": "fountain.reframe.r28.first-wlan-bookshelf.v1",
            "state": "built-private-WLAN-candidate-not-public-not-Store-admitted",
            "predecessor": active.name,
            "release": out.name,
            "sourceOwner": "Fountain-Coach/fountain.coach",
            "pressExistingMarkupSource": "estate/editions/index.html",
            "originalSevenEssayRoute": "estate/index.html",
            "originalEssaySourceRevision": source_revision,
            "originalSHA256": originals,
            "outputSHA256": {
                "bookshelf": digest(root_target),
                "essaysContinuing": digest(book_target),
                "pressBookshelfAlternative": digest(out/"estate"/"editions"/"index.html"),
                "readerCSS": digest(out/"estate"/"assets"/"linotype"/"reframe-reader-r28.css"),
            },
            "changedRoutes": ["estate/index.html", "estate/editions/index.html"],
            "addedRoutes": ["estate/editions/essays-continuing/index.html"],
            "addedAssets": ["estate/assets/linotype/reframe-reader-r28.css"],
            "allOtherRoutesPreserved": True,
            "sameReaderTwoPublicDomains": "product-direction-only-no-DNS-change",
            "publicPublication": False,
            "iPadSafariAcceptance": "not-performed",
        }
        lock["reframeFirstReaderR28"] = record
        (out / "source-lock.json").write_text(json.dumps(lock, indent=2, ensure_ascii=False)+"\n")
    except Exception:
        shutil.rmtree(out, ignore_errors=True)
        raise
    return record

def activate(args: argparse.Namespace) -> dict:
    root = Path(args.stage_root).resolve()
    current = root / "current"
    active = current.resolve(strict=True)
    if active.name != args.expected_active:
        raise RuntimeError("Stage predecessor changed; refusing activation")
    candidate = root / "releases" / args.release_id
    if not candidate.is_dir():
        raise FileNotFoundError("No prebuilt candidate")
    record = json.loads((candidate/"source-lock.json").read_text()).get("reframeFirstReaderR28")
    if not record or record["predecessor"] != active.name:
        raise RuntimeError("Candidate provenance mismatch")
    for path, sha in (
       ("estate/index.html",record["outputSHA256"]["bookshelf"]),
       ("estate/editions/essays-continuing/index.html",record["outputSHA256"]["essaysContinuing"]),
    ):
        if digest(candidate/path) != sha:
            raise RuntimeError("Candidate changed since build: "+path)
    replacement = root / "current.r28-next"
    if replacement.exists() or replacement.is_symlink():
        raise FileExistsError("Unexpected pending stage activation")
    replacement.symlink_to(Path("releases") / candidate.name)
    os.replace(replacement,current)
    return {"activated": candidate.name, "previous": active.name, "readbackNeeded": True}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage-root", required=True)
    parser.add_argument("--expected-active", required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args()
    result = activate(args) if args.activate else build(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"R28_STAGE_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
