#!/usr/bin/env python3
"""Add the REAL protected Satzfunk archive to a disposable three-front estate stage.

Never edits Git owners, historical media, access tokens, public DNS or Caddy.
Existing 8180/8181/8182 roots remain source-identical except for local navigation,
cover assets and a documented source-lock extension.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ARCHIVE = "http://192.168.8.50:8194/"
COVER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img">
<title>Satzfunk, authored audiovisual radio</title>
<rect width="600" height="600" fill="#e8e4db"/>
<text x="42" y="82" font-family="monospace" font-size="20" fill="#5b625b">FOUNTAIN COACH</text>
<text x="38" y="202" font-family="Georgia,serif" font-size="83" fill="#263229">Satzfunk</text>
<path d="M42 251H555M42 493H555" stroke="#91988b" stroke-width="2"/>
<path d="M59 374v30m37-83v119m37-107v95m37-132v169m37-89v35m37-150v211m37-96v62m37-181v222m37-106v70m37-147v185m37-104v79m37-135v151m37-84v46" stroke="#315b54" stroke-width="6" fill="none" stroke-linecap="round"/>
<text x="43" y="543" font-family="monospace" font-size="18" fill="#5b625b">AN AUTHOR'S RADIO</text></svg>"""

NAV = re.compile(r'(<nav\b[^>]*class="[^"]*\b(?:estate-nav|edition-rail)\b[^"]*"[^>]*>)(.*?)(</nav>)', re.S)

def add_nav(source):
    def enrich(m):
        body = m.group(2)
        if 'data-estate-id="satzfunk"' in body:
            return m.group(0)
        if not all('data-estate-id="' + x + '"' in body for x in ('estate', 'first-reading', 'teatro')):
            return m.group(0)
        cls = 'estate-icon' if 'estate-nav' in m.group(1) else ''
        link = ('<a class="' + cls + '" data-estate-id="satzfunk" href="' +
                ARCHIVE + '" aria-label="Satzfunk, audiovisual radio and archive">Satzfunk</a>')
        return m.group(1) + body + link + m.group(3)
    return NAV.subn(enrich, source)

def add_book(source, art, revision):
    if 'data-linotype-state="bookshelf"' not in source:
        raise RuntimeError('not an admitted Linotype bookshelf')
    if 'data-book-id="satzfunk"' in source:
        raise RuntimeError('book already added')
    match = re.search(r'data-book-count="([0-9]+)"', source)
    if not match:
        raise RuntimeError('book count missing')
    n = int(match.group(1))
    if source.count('class="shelf-item"') != n:
        raise RuntimeError('bookshelf count mismatches original')
    slot = '<li class="bookshelf-empty" aria-hidden="true"></li>'
    if slot not in source:
        raise RuntimeError('no empty slot; do not disturb an admitted publication')
    element = (
        '<li class="shelf-item" data-book-id="satzfunk" '
        'data-release-status="wlan-private-archive" data-source-revision="' + revision + '">'
        '<a class="shelf-book" href="' + ARCHIVE + '" data-preview-host="satzfunk" '
        'aria-label="Open Satzfunk, original private audiovisual radio">'
        '<span class="shelf-cover" aria-hidden="true"><img src="' + art +
        '" alt="" loading="lazy" decoding="async"></span></a></li>'
    )
    output = source.replace(slot, element, 1)
    output = output.replace('data-book-count="' + str(n) + '"',
                            'data-book-count="' + str(n + 1) + '"', 1)
    assert output.count('class="shelf-item"') == n + 1
    return output

def process(source, target, revision):
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise RuntimeError('Satzfunk must have an exact 40-character Git revision')
    source = source.resolve()
    if not source.joinpath('source-lock.json').is_file():
        raise RuntimeError('not a pinned estate stage')
    before = source.joinpath('source-lock.json').read_bytes()
    lock = json.loads(before)
    if set(lock.get('sites', {})) != {'fountain','solstice','teatro'} or lock.get('productionPublished') is not False:
        raise RuntimeError('wrong release authority; refuse')
    if target.exists() or target.is_symlink():
        raise RuntimeError('target exists; refusing overwrite')
    if target.parent.name != 'releases' or target.parent.parent.name != 'estate-three-front-staging':
        raise RuntimeError('target is not an exact Ubuntu estate staging release')
    shutil.copytree(source, target)
    changed = []
    for site, art in [('fountain', '/assets/estate-bookshelf/satzfunk-cover.svg'),
                      ('teatro', '/assets/bookshelf/satzfunk-cover.svg')]:
        cover = target / site / art.lstrip('/')
        cover.parent.mkdir(parents=True, exist_ok=True)
        cover.write_text(COVER)
        for name in ['index.html', 'editions/index.html']:
            page = target / site / name
            page.write_text(add_book(page.read_text(), art, revision))
            changed.append(str(page.relative_to(target)))
    navs = 0
    for site in ('fountain','solstice','teatro'):
        for page in (target / site).rglob('index.html'):
            original = page.read_text()
            edited, _ = add_nav(original)
            if edited != original:
                page.write_text(edited)
                changed.append(str(page.relative_to(target)))
                navs += 1
    lock['auxiliaryServices'] = {
        'satzfunk': {
            'repository': 'Fountain-Coach/Satzfunk',
            'commit': revision,
            'address': ARCHIVE,
            'access': 'author-only LAN / existing protected service',
            'copiedMedia': False,
            'scope': 'wlan-only'
        }
    }
    lock['linkedRadioStaging'] = {
        'sourceLockSHA256': hashlib.sha256(before).hexdigest(),
        'bookshelfPages': 4, 'navigationPages': navs,
        'publicationReleased': False, 'archiveMediaCopied': False,
        'rollback': str(source),
    }
    (target / 'source-lock.json').write_text(json.dumps(lock, indent=2) + '\n')
    return {'release': str(target), 'navigationPages': navs, 'pagesChanged': sorted(set(changed)),
            'sourceLockSHA256': hashlib.sha256(before).hexdigest(),
            'archiveAuthUnchanged': True, 'productionPublished': False}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--release', type=Path, required=True)
    p.add_argument('--satzfunk-revision', required=True)
    x = p.parse_args()
    print(json.dumps(process(x.source, x.release, x.satzfunk_revision), indent=2))
