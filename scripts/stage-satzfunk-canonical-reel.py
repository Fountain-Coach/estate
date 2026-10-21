#!/usr/bin/env python3
"""Project the single canonical estate reel into the ORIGINAL private Satzfunk archive.

Takes only three already-authorized HTML/CSS inputs; writes separate review
copies. Does not touch audio, scripts, video, source text, or access control.
"""
import argparse
import json
from pathlib import Path
import re
import runpy

CSS = """
/* Canonical reel: local projection of Fountain-Coach/estate navigation/canonical-reel.v1.json.
   The archive retains its own Linotype colors, gallery, playback and editorial hierarchy. */
.estate-nav.estate-local-unified-reel {
  display:flex; align-items:center; gap:8px; padding:12px 0;
  margin:14px 0 25px; overflow-x:auto; overscroll-behavior-inline:contain;
  scrollbar-width:thin; border-top:1px solid #a8aca1; border-bottom:1px solid #a8aca1;
  white-space:nowrap; max-width:100%;
}
.estate-local-unified-reel .estate-icon {
  display:flex; flex:0 0 auto; align-items:center; justify-content:center;
  width:42px; height:42px; padding:8px;
  color:#354c43; border:1px solid transparent; border-radius:8px;
  text-decoration:none;
}
.estate-local-unified-reel .estate-icon svg {
  width:22px; height:22px; fill:none; stroke:currentColor;
  stroke-width:1.35; stroke-linecap:round; stroke-linejoin:round;
}
.estate-local-unified-reel .estate-icon [aria-hidden] {pointer-events:none}
.estate-local-unified-reel .estate-icon span {position:absolute; width:1px; height:1px;
  padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0);
  white-space:nowrap; border:0}
.estate-local-unified-reel .estate-icon:hover,
.estate-local-unified-reel .estate-icon:focus-visible {background:#d9d6ca; border-color:#898b7e}
.estate-local-unified-reel .estate-icon[aria-current="page"] {
  border-color:#3f564b; background:#e5e5dc;
}
@media(max-width:720px) {
  .estate-nav.estate-local-unified-reel {gap:3px; margin:10px 0 21px}
  .estate-local-unified-reel .estate-icon {width:38px; height:40px; padding:7px}
}
"""
NAV = re.compile(r'<nav\b[^>]*class="estate-local-rail"[^>]*>.*?</nav>',re.S)
def build(source:Path,dest:Path,manifest:Path,projector:Path):
    if dest.exists():
        raise RuntimeError("Output exists; refusing overwrite")
    entries=json.loads(manifest.read_text())['entries']
    assert len(entries)==10
    make_nav=runpy.run_path(str(projector))['make_nav']
    dest.mkdir(parents=True)
    nav='<nav class="estate-nav estate-local-unified-reel" aria-label="Fountain Coach publication estate" data-reel-contract="canonical-reel.v1">'+make_nav('satzfunk',entries)+'</nav>'
    for path in ("index.html","7vst-originals.html"):
        p=source/path
        original=p.read_text()
        updated,n=NAV.subn(lambda m:nav,original)
        if n!=1:
            raise RuntimeError("Expected exact old local link bar in "+path)
        if 'id="footer"' not in updated:
            updated,n=re.subn(r'<footer\b', '<footer id="footer"',updated,count=1)
            if n!=1:
                raise RuntimeError("Missing footer in "+path)
        assert updated.count('data-estate-id="satzfunk"')==1
        assert updated.count('data-estate-id=')==10
        assert updated.count('aria-current="page"')==1
        (dest/path).write_text(updated)
    css=(source/'style.css').read_text()
    if '.estate-local-unified-reel' in css:
        raise RuntimeError("Already applied")
    (dest/'style.css').write_text(css+'\n'+CSS)
    print("PASS: canonical ten-item reel staged for private Satzfunk and 7VST; zero media touched")

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--manifest',type=Path,required=True)
    ap.add_argument('--projector',type=Path,required=True)
    a=ap.parse_args()
    build(a.source,a.output,a.manifest,a.projector)
