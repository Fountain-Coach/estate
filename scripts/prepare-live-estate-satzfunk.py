#!/usr/bin/env python3
"""Mirror the CURRENTLY PUBLISHED Fountain Coach portal to a private WLAN visual preview.

This is deliberately a public-byte fidelity study, NOT a source authority substitution
or a production publisher. It never publishes historical Satzfunk media or writes DNS.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ORIGIN = "https://fountain.coach/"
LOCAL_SATZFUNK = "http://192.168.8.50:8194/"
FILES = (
    "index.html", "assets/site.css", "assets/site.js", "assets/estate-core.css",
    "assets/estate-core.js", "assets/fountain-coach-logo-transparent.png",
    "assets/future-estate-portal.svg"
)
VOICE = """<a class="estate-icon" data-estate-id="satzfunk" href="http://192.168.8.50:8194/"
 aria-label="Satzfunk — original audiovisual radio, private local archive">
 <svg viewBox="0 0 24 24" class="estate-symbol" aria-hidden="true">
 <path d="M2 12h3m3-5v10m3-14v18m3-13v8m3-11v14m3-9v4" fill="none"
 stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
 <span>Satzfunk</span></a>"""
CARD = """<article class="estate-card" data-estate-addition="satzfunk-private-wlan">
 <div class="estate-card-head">
 <svg viewBox="0 0 24 24" aria-hidden="true">
 <path d="M2 12h3m3-5v10m3-14v18m3-13v8m3-11v14m3-9v4" fill="none"
 stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
 <small>10 · AUDIBLE WORK</small></div>
 <strong><a href="http://192.168.8.50:8194/">Satzfunk — an author's radio</a></strong>
 <span>Listen to the original audiovisual works and their historical editions. Private WLAN access; no public media release.</span>
 </article>"""

def fetch(path):
    url = ORIGIN if path == 'index.html' else ORIGIN + path
    req = urllib.request.Request(url, headers={'User-Agent':'FountainCoach-WLAN-PublishedStateAudit/1.0'})
    with urllib.request.urlopen(req, timeout=16) as response:
        if response.status != 200 or response.url != url:
            raise RuntimeError('Unexpected origin response: ' + url)
        return response.read()

def prepare(target):
    if target.exists():
        raise RuntimeError('Refusing to overwrite existing release: ' + str(target))
    if target.parent.name != 'releases' or target.parent.parent.name != 'estate-published-state-staging':
        raise RuntimeError('Refusing target outside dedicated disposable published-state preview')
    downloaded = {p: fetch(p) for p in FILES}
    raw = downloaded['index.html'].decode('utf-8')
    assert 'Author the conditions for what comes next.' in raw
    assert 'One mark. Many ways in.' in raw
    assert raw.count('data-estate-id="teatro"') == 1
    assert raw.count('<div class="estate-grid" aria-label="Estate publications">') == 1
    assert 'data-estate-id="satzfunk"' not in raw
    assert raw.count('09 · NEW ESSAY') == 1
    original_digest = hashlib.sha256(downloaded['index.html']).hexdigest()
    # Extend the exact published navigation; never rebuild its menu from Git main.
    pattern = re.compile(r'(<a\b[^>]*data-estate-id="teatro"[^>]*>.*?</a>)', re.S)
    raw, navcount = pattern.subn(lambda m:m.group(1) + VOICE, raw)
    assert navcount == 1
    # Extend the existing publication grid, after its last original essay card.
    grid = '<div class="estate-grid" aria-label="Estate publications">'
    before, after = raw.split(grid)
    end = after.index('</div></section>')
    raw = before + grid + after[:end] + CARD + after[end:]
    assert raw.count('data-estate-addition="satzfunk-private-wlan"') == 1
    # The site is a local proof of the live visual state, not a second published homepage.
    raw = raw.replace('<head>', '<head>\n<meta name="robots" content="noindex,nofollow">\n'
                      '<meta name="fountain:preview-only" content="local-published-state-satzfunk">', 1)
    target.mkdir(parents=True)
    for name, content in downloaded.items():
        output = target/name
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(raw.encode('utf-8') if name=='index.html' else content)
    digest = {name:hashlib.sha256(content).hexdigest() for name,content in downloaded.items()}
    meta = {
       'schema':'fountain.estate.published-state-satzfunk-preview.v1',
       'capturedUTC':datetime.now(timezone.utc).isoformat(),
       'originalPublicURL':ORIGIN,
       'originalPublicHomepageSHA256':original_digest,
       'originalByteSHA256':digest,
       'target':LOCAL_SATZFUNK,
       'assetOrigin':'same-published-site-bytes',
       'changes':['one nav link after Teatro','one 10 AUDIBLE WORK authority card',
                  'noindex local preview marker'],
       'existingPublicationCopiedUnchangedExceptHomeHTML':True,
       'privateArchiveMediaCopied':False,
       'publicDomainPublished':False,
       'rejectedStaticReelUsed':False,
       'sourceOwnership':'Git-owning Fountain-Coach/fountain.coach remains authoritative',
       'releaseStatus':'LOCAL_VISUAL_PREVIEW_ONLY'
    }
    (target/'capture-lock.json').write_text(json.dumps(meta,indent=2)+'\n')
    assert len(list(target.rglob('*.mp4'))) == 0
    assert b'data-estate-id="satzfunk"' in (target/'index.html').read_bytes()
    return {'release':str(target),'originSHA256':original_digest,
            'files':len(downloaded),'addedNav':1,'addedCard':1,
            'mediaCopied':False,'published':False}

if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--release',type=Path,required=True)
    args=ap.parse_args()
    print(json.dumps(prepare(args.release),indent=2))
