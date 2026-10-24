#!/usr/bin/env python3
"""Materialize a bounded public Satzfunk navigation correction from six pinned public releases.

Only one exact obsolete HTML token is exchanged per affected HTML page.
All other bytes, assets, editorial texts, and file names remain unchanged.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

DOMAINS = (
    "fountain.coach", "governance.fountain.coach", "midi2.fountain.coach",
    "teatro.fountain.coach", "book.fountain.coach", "instruments.fountain.coach",
)
PREDECESSOR = {
    "fountain.coach": "estate-20261023-v13-estate",
    "governance.fountain.coach": "estate-20261023-v13-governance",
    "midi2.fountain.coach": "estate-20261023-v13-midi2",
    "teatro.fountain.coach": "estate-20261023-v13-teatro",
    "book.fountain.coach": "estate-20261023-v13-book",
    "instruments.fountain.coach": "estate-20261023-v13-instruments",
}
URL = "https://satzfunk.fountain.coach/"
OLD_OPEN = (
    '<span aria-disabled="true" aria-label="Satzfunk — not yet public" '
    'class="fc-reel-link fc-reel-unavailable" '
    'data-canonical-href="https://satzfunk.fountain.coach/" '
    'data-estate-id="satzfunk" data-icon-id="satzfunk" role="link" '
    'title="Satzfunk — not yet public">'
)
MIDDLE = (
    '<svg aria-hidden="true" viewbox="0 0 24 24">'
    '<path d="M2 12h3m3-5v10m3-14v18m3-13v8m3-11v14m3-9v4"></path>'
    '</svg><span>Satzfunk</span>'
)
OLD = OLD_OPEN + MIDDLE + "</span>"
NEW = (
    '<a aria-label="Satzfunk" class="fc-reel-link" '
    'data-canonical-href="https://satzfunk.fountain.coach/" '
    'data-estate-id="satzfunk" data-icon-id="satzfunk" '
    'href="https://satzfunk.fountain.coach/">' + MIDDLE + "</a>"
)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run(source: Path, dest: Path, evidence: Path) -> None:
    assert not dest.exists(), "Do not overwrite a candidate"
    assert source.resolve() != dest.resolve()
    records = []
    counts = {}
    for domain in DOMAINS:
        left = source / domain
        right = dest / domain
        assert left.is_dir(), left
        count = 0
        file_total = 0
        for file in sorted(left.rglob("*")):
            if not file.is_file():
                continue
            assert not file.is_symlink(), file
            rel = file.relative_to(left)
            target = right / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            original = file.read_bytes()
            changed = original
            if file.suffix == ".html":
                n = original.count(OLD.encode("utf-8"))
                assert n in (0, 1), (file, n)
                if n:
                    assert original.count(b'data-estate-id="satzfunk"') == 1
                    changed = original.replace(OLD.encode("utf-8"), NEW.encode("utf-8"))
                    assert changed.count(NEW.encode("utf-8")) == 1
                    assert b'fc-reel-unavailable' not in changed or b'data-estate-id="satzfunk"' not in changed.replace(NEW.encode("utf-8"), b'')
                    assert b'data-estate-id="satzfunk"' in changed
                    records.append({"host": domain, "path": "/" + rel.as_posix(),
                        "beforeSHA256": sha(original), "afterSHA256": sha(changed)})
                    count += 1
            target.write_bytes(changed)
            target.chmod(file.stat().st_mode & 0o777)
            file_total += 1
        assert count >= 1, domain
        counts[domain] = {"totalFiles": file_total, "correctedHTMLPages": count,
                          "predecessor": PREDECESSOR[domain]}
    assert sum(x["correctedHTMLPages"] for x in counts.values()) == 171, counts
    assert len(records) == 171
    evidence.parent.mkdir(parents=True, exist_ok=True)
    assert not evidence.exists()
    evidence.write_text(json.dumps({
        "schema": "fountain.estate.satzfunk-reel-public-admission.v1",
        "asOf": "2026-10-24",
        "rootCause": "v13 estate shells retained the obsolete aria-disabled Satzfunk span after the separate media host became public",
        "change": "exact source-owned reel span -> canonical, focusable same-origin-safe HTTPS anchor",
        "canonicalURL": URL,
        "counts": counts,
        "changedHTML": records,
        "verification": "full preserved static site snapshots, per-file hashes, previous immutable releases retained"
    }, indent=2, ensure_ascii=False) + "\n")
    print("PATCH_OK",len(records),"HTML pages in",len(DOMAINS),"domains")
    for domain,c in counts.items():print(domain,c["correctedHTMLPages"],"/",c["totalFiles"])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline",required=True,type=Path)
    ap.add_argument("--candidate",required=True,type=Path)
    ap.add_argument("--evidence",required=True,type=Path)
    a=ap.parse_args()
    run(a.baseline,a.candidate,a.evidence)
