#!/usr/bin/env python3
"""Source-bound v152 archival stage admission and forged-identity refusal."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path("/home/benedikt/estate-shell-acceptance-staging")
BASE=ROOT/"releases/shared-shell-20261103-v140-same-folio-return"
RELEASE=ROOT/"releases/shared-shell-20261105-v152-editorial-archive-1609cb9"
GUARD=ROOT/"reader_provenance_gate_v152_candidate.py"
spec=importlib.util.spec_from_file_location("reader_provenance_gate_v152_candidate",GUARD)
if spec is None or spec.loader is None:raise RuntimeError("No pinned prospective v152 Reader guard")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
g=mod.ReaderProvenanceGate(BASE,RELEASE)
for uri in (
 "/estate/","/estate/index.html",
 "/estate/assets/linotype/reading-first-app.js",
 "/estate/assets/linotype/reading-first-press-engine.js",
 "/estate/assets/linotype/reading-first-press-frame.css",
 "/estate/essays/index.html",
 "/estate/assets/essay-share/manifest.json",
 "/estate/essays/to-read-is-not-to-remember/",
 "/estate/essays/to-read-is-not-to-remember/index.html",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/index.html",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-a.mp3",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-b.mp3"
):
    g.check(uri)
    print("ADMITTED",uri,flush=True)
for name in ("APPROVED_ARCHIVE_LOCK_SHA256","APPROVED_ARCHIVE_SOURCE_COMMIT"):
    saved=getattr(mod,name)
    setattr(mod,name,"0"*len(saved))
    try:mod.ReaderProvenanceGate(BASE,RELEASE)
    except mod.UnadmittedReaderRoute as e:print("REFUSED_FORGED",name,str(e)[:100],flush=True)
    else:raise AssertionError("Forged "+name+" was admitted")
    finally:setattr(mod,name,saved)
for rel in mod.APPROVED_ARCHIVE_FILES:
    saved=mod.APPROVED_ARCHIVE_FILES[rel]
    mod.APPROVED_ARCHIVE_FILES[rel]="0"*len(saved)
    try:mod.ReaderProvenanceGate(BASE,RELEASE)
    except mod.UnadmittedReaderRoute as e:print("REFUSED_FILE",rel,str(e)[:100],flush=True)
    else:raise AssertionError("Forged "+rel+" was admitted")
    finally:mod.APPROVED_ARCHIVE_FILES[rel]=saved
print("V152_ARCHIVE_GUARD_PASS","six adversarial variants rejected",flush=True)
