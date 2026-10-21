#!/usr/bin/env python3
"""Add reversible four-front WLAN navigation to the real Satzfunk archive UI.

The actual private video/text service and its cookie authentication are
preserved. No master media, source text, secret, public route, or API is changed.
"""
import argparse
import hashlib
import json
from pathlib import Path
from shutil import copy2

SITE = Path("/home/benedikt/services/satzfunk-private-video-browser/archive/browser")
BASE = Path("/home/benedikt/services/satzfunk-private-video-browser")
BACKUP = BASE / "integration-backups" / "20261021-four-front-v1"
ESTATE = "http://192.168.8.249:8182/"
NAV = (
    '<nav class="estate-local-rail" aria-label="Fountain Coach local estate"'
    ' data-estate-stage="four-front-v1">'
    '<a href="' + ESTATE + '" title="Return to Fountain Coach bookshelf">Estate</a>'
    '<a href="http://192.168.8.249:8180/editions/essays/">Essays</a>'
    '<a href="http://192.168.8.249:8181/editions/first-reading/">First Reading</a>'
    '<a href="http://192.168.8.249:8182/editions/first-hearing/">Teatro</a>'
    '<span aria-current="page">Satzfunk</span></nav>'
)
STYLE = """
/* Stage-only four-front navigation; the 43 original video URLs remain private. */
.estate-local-rail{display:flex;align-items:center;gap:14px;flex-wrap:wrap;border-top:1px solid #abb0a5;
  padding:12px 0 16px;margin:0 0 20px;font:11px/1.55 ui-monospace,Menlo,monospace;
  letter-spacing:.02em;color:#52645a}
.estate-local-rail a{color:#315b54;text-decoration:none}
.estate-local-rail a:hover,.estate-local-rail a:focus-visible{text-decoration:underline}
.estate-local-rail [aria-current=page]{font-weight:600;color:#27382e}
@media(max-width:720px){.estate-local-rail{flex-wrap:nowrap;overflow-x:auto;white-space:nowrap;
  padding:11px 0 15px;gap:16px;scrollbar-width:thin}}
"""
MARK = "data-estate-stage=\"four-front-v1\""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not SITE.exists() or not BASE.exists():
        raise SystemExit("Missing canonical private archive staging path")
    results = {}
    for name in ("index.html", "7vst-originals.html", "style.css"):
        path = SITE / name
        if not path.is_file():
            raise SystemExit("Missing file: " + str(path))
        original = path.read_text()
        if name.endswith(".html"):
            if MARK not in original:
                anchor = '<div class="brand">'
                first = original.find(anchor)
                end = original.find("</div>", first)
                if first < 0 or end < 0 or "SATZFUNK" not in original[first:end]:
                    raise SystemExit("Unexpected source archive branding: " + name)
                proposed = original[:end+6] + "\n" + NAV + original[end+6:]
            else:
                proposed = original
        else:
            proposed = original if "Stage-only four-front navigation" in original else original + "\n" + STYLE
        if args.check:
            if proposed != original:
                raise SystemExit(name + " needs integration")
        elif proposed != original:
            BACKUP.mkdir(parents=True, exist_ok=True)
            original_backup = BACKUP / name
            if original_backup.exists():
                raise SystemExit("Existing backup not overwritten: " + name)
            copy2(path, original_backup)
            path.write_text(proposed)
        results[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps({"integration":"four-front-v1","protectedMediaUnchanged":True,
                      "archiveURL":"http://192.168.8.50:8194/",
                      "files":results},indent=2))

if __name__ == "__main__":
    main()
