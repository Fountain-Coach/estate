#!/usr/bin/env python3
"""Integrate Satzfunk into the already verified four-front local estate preview.

Changes ONLY a disposable, pinned Ubuntu estate release. Never writes the
GitHub-owned source site trees or bypasses the separately protected archive.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

STAGING = Path("/home/benedikt/estate-three-front-staging")
SATZFUNK = "http://192.168.8.50:8194/"
COVER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img" aria-labelledby="t d">
<title id="t">Satzfunk — the audiovisual archive</title>
<desc id="d">Warm archive-paper artwork with a restrained sound trace</desc>
<rect width="600" height="600" fill="#e8e4db"/>
<g fill="#26342c"><text x="48" y="80" font-family="monospace" font-size="19" letter-spacing="3">FOUNTAIN COACH</text>
<text x="44" y="192" font-family="Georgia,serif" font-size="72">Satzfunk</text></g>
<g fill="none" stroke="#315b54" stroke-linecap="round"><path d="M48 231H552M48 491H552" stroke-width="2"/>
<path d="M65 367v18m28-36v54m28-82v111m28-50v35m28-95v117m28-132v153m28-88v62m28-111v160m28-90v93m28-137v183m28-105v77m28-134v167m28-94v83m28-113v119m28-66v34m28-54v54" stroke-width="5"/></g>
<text x="48" y="543" fill="#5c675e" font-family="monospace" font-size="15" letter-spacing="2">AUTHOR'S AUDIOVISUAL RADIO</text>
</svg>"""

def read(path):
    return path.read_text(encoding="utf-8")

def put(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and read(path) == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True

def nav_projection(page):
    html = read(page)
    pattern = re.compile(r'(<nav\b[^>]*class="[^"]*\b(edition-rail|estate-nav)\b[^"]*"[^>]*>)(.*?)(</nav>)', re.S)
    found = [0]
    def make(match):
        kind = match.group(2)
        body = match.group(3)
        if 'data-estate-id="satzfunk"' in body:
            return match.group(0)
        if 'data-estate-id="teatro"' not in body:
            return match.group(0)
        if kind == "edition-rail":
            link = '<a data-estate-id="satzfunk" href="' + SATZFUNK + '" title="Satzfunk audiovisual archive">Satzfunk</a>'
        else:
            link = ('<a class="estate-icon" data-estate-id="satzfunk" href="' + SATZFUNK + '" aria-label="Satzfunk archive">'
                    '<svg viewBox="0 0 24 24" class="estate-symbol" aria-hidden="true"><path d="M3 12h3m2-5v10m3-14v18m3-12v6m3-10v14m3-7h1"/></svg><span>Satzfunk</span></a>')
        found[0] += 1
        if kind == "estate-nav" and '<a class="estate-icon estate-info"' in body:
            body = body.replace('<a class="estate-icon estate-info"', link + '<a class="estate-icon estate-info"', 1)
        else:
            body += link
        return match.group(1) + body + match.group(4)
    modified = pattern.sub(make, html)
    if found[0]:
        put(page, modified)
    return found[0]

def shelf_projection(page, asset):
    html = read(page)
    if 'data-linotype-state="bookshelf"' not in html:
        raise ValueError("Not a bookshelf: " + str(page))
    if 'data-book-id="satzfunk"' in html:
        return False
    before = re.search(r'data-book-count="(\d+)"', html)
    if before is None:
        raise ValueError("Missing count: " + str(page))
    old_count = int(before.group(1))
    if html.count('class="shelf-book"') != old_count:
        raise ValueError("Existing cover count drift: " + str(page))
    if '<li class="bookshelf-empty"' not in html:
        raise ValueError("Cannot find retained blank slot: " + str(page))
    item = ('<li class="shelf-item" data-book-id="satzfunk" data-release-status="wlan-private"'
            ' data-owning-repository="Fountain-Coach/Satzfunk">'
            '<a class="shelf-book" href="' + SATZFUNK + '" data-preview-host="satzfunk"'
            ' aria-label="Open SATZFUNK — original audiovisual archive; private local listening">'
            '<span class="shelf-cover" aria-hidden="true"><img src="' + asset +
            '" alt="" loading="lazy" decoding="async"></span></a></li>')
    html = html.replace('<li class="bookshelf-empty"', item + '<li class="bookshelf-empty"', 1)
    html = html.replace('data-book-count="' + str(old_count) + '"',
                        'data-book-count="' + str(old_count + 1) + '"', 1)
    if html.count('class="shelf-book"') != old_count + 1:
        raise ValueError("Post-projection cover count mismatch")
    put(page, html)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--satzfunk-commit", required=True)
    args = parser.parse_args()
    release = args.release.resolve()
    if release.parent != STAGING / "releases" or release == (STAGING / "current").resolve():
        raise SystemExit("Refuse unsafe staging target: " + str(release))
    if not re.fullmatch(r"[a-f0-9]{40}", args.satzfunk_commit):
        raise SystemExit("Invalid SHA")
    lock_path = release / "source-lock.json"
    metadata = json.loads(read(lock_path))
    if set(metadata["sites"]) != {"fountain", "solstice", "teatro"}:
        raise SystemExit("Existing estate source lock has unexpected owners")
    changes = {}
    for s in ("fountain", "solstice", "teatro"):
        root = release / s
        changed = 0
        for page in sorted(root.rglob("*.html")):
            changed += nav_projection(page)
        changes[s] = changed
    for s, asset in (("fountain", "/assets/estate-bookshelf/satzfunk-archive.svg"),
                     ("teatro", "/assets/bookshelf/satzfunk-archive.svg")):
        for entry in ("index.html", "editions/index.html"):
            shelf_projection(release / s / entry, asset)
        cover_path = release / s / asset.lstrip("/")
        put(cover_path, COVER + "\n")
        changes[s + "CoverSHA256"] = hashlib.sha256(cover_path.read_bytes()).hexdigest()
    metadata["localEstateAddition"] = {
        "site": "satzfunk", "repository": "Fountain-Coach/Satzfunk",
        "commit": args.satzfunk_commit, "url": SATZFUNK,
        "access": "existing private cookie-protected archive",
        "playerOwner": "Satzfunk archive/browser, not a copied server",
        "reel": "accepted real Bandcamp/Linotype archive, NOT rejected public-reel",
        "productionPublished": False, "navigationPages": changes,
    }
    metadata["scope"] = "Four-way WLAN estate: Essays, First Reading, Teatro, authentic Satzfunk"
    metadata["authorAcceptance"] = "pending actual iPad Safari viewing"
    put(lock_path, json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(metadata["localEstateAddition"], indent=2))

if __name__ == "__main__":
    main()
