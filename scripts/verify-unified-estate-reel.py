#!/usr/bin/env python3
"""Prove identical semantic reel on every published-state local mirror."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urljoin

IDS=['estate','book','governance','midi2','instruments',
     'teatro','satzfunk','pointer','solstice']
NAV=re.compile(r'<nav\b[^>]*class="[^"]*\bestate-nav\b[^"]*"[^>]*>.*?</nav>',re.S)
A=re.compile(r'<a\b[^>]*data-estate-id="(?P<id>[^"]+)"[^>]*>.*?</a>',re.S)
ROOT='http://192.168.8.50:8198/'
RADIO='http://192.168.8.50:8194/'

def check(root:Path,live=False):
    meta=json.loads((root/'capture-lock.json').read_text())
    assert meta['schema']=='fountain.estate.unified-reel-preview.v1'
    assert len(meta['sites'])==9
    assert meta['privateMediaCopied'] is False
    assert meta['publicationChanged'] is False
    state=[]
    for captured in meta['sites']:
        ident=captured['identity']
        source=(root/ident/'index.html').read_text()
        nav=NAV.search(source)
        assert nav,('missing reel',ident)
        matches=list(A.finditer(nav.group()))
        ids=[m.group('id') for m in matches]
        assert ids==IDS,(ident,ids)
        assert source.count('data-estate-id="satzfunk"')==1,ident
        current=[m.group('id') for m in matches if 'aria-current="page"' in m.group()]
        assert current==[ident],(ident,current)
        assert nav.group().count('aria-label="Info"')==1
        for match in matches:
            id=match.group('id')
            expected=RADIO if id=='satzfunk' else ROOT+id+'/'
            assert 'href="'+expected+'"' in match.group(),(ident,id,expected)
        for asset in captured['copiedAssets']:
            path=root/ident/asset['path']
            assert path.exists(),(ident,asset['path'])
            assert hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256']
        assert 'data-reel-preview-identity="'+ident+'"' in source
        assert 'noindex,nofollow' in source
        state.append({'site':ident,'reel':ids,'assetCount':len(captured['copiedAssets'])})
        if live:
            with urlopen(ROOT+ident+'/',timeout=8) as r:
                rendered=r.read().decode()
                assert r.status==200
                assert 'noindex' in r.headers.get('X-Robots-Tag','')
                assert 'data-estate-id="satzfunk"' in rendered
                assert 'aria-current="page"' in rendered
    if live:
        try:
            urlopen(RADIO,timeout=5)
            raise AssertionError('private radio archive became anonymously accessible')
        except HTTPError as e:
            assert e.code==403,e.code
    print(json.dumps({'PASS':True,'sites':len(state),'canonicalIds':IDS,
                      'live':live,'privateArchivePreserved':True},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',required=True,type=Path)
    ap.add_argument('--live',action='store_true')
    opts=ap.parse_args()
    check(opts.root.resolve(),opts.live)
