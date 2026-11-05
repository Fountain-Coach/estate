#!/usr/bin/env python3
"""Fail-closed v151 source admission against the actual immutable MacMini candidate."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path("/home/benedikt/estate-shell-acceptance-staging")
BASE=ROOT/"releases/shared-shell-20261103-v140-same-folio-return"
CANDIDATE=ROOT/"releases/shared-shell-20261105-v151-semantic-spread-17e32af"
GUARD=ROOT/"reader_provenance_gate_v151_candidate.py"
spec=importlib.util.spec_from_file_location("reader_provenance_gate_v151_candidate",GUARD)
if spec is None or spec.loader is None:raise RuntimeError("Cannot read prospective stage provenance guard")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
gate=mod.ReaderProvenanceGate(BASE,CANDIDATE)
for uri in (
 "/estate/","/estate/index.html",
 "/estate/assets/linotype/reading-first-press-engine.js",
 "/estate/assets/linotype/reading-first-press-frame.css",
 "/estate/assets/linotype/reading-first-app.js",
 "/estate/essays/what-makes-a-page-modern/assets/reader.svg",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/index.html",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-a.mp3",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-b.mp3"
):
    gate.check(uri)
    print("ADMITTED",uri,flush=True)
for name in ("APPROVED_SPREAD_LOCK_SHA256","APPROVED_SPREAD_SOURCE_COMMIT"):
    saved=getattr(mod,name)
    setattr(mod,name,"0"*len(saved))
    try:
        mod.ReaderProvenanceGate(BASE,CANDIDATE)
    except mod.UnadmittedReaderRoute as e:
        print("REJECTED_TAMPER",name,str(e)[:130],flush=True)
    else:
        raise AssertionError("Forbidden source mismatch admitted: "+name)
    finally:setattr(mod,name,saved)
for rel in mod.APPROVED_SPREAD_FILES:
    saved=mod.APPROVED_SPREAD_FILES[rel]
    mod.APPROVED_SPREAD_FILES[rel]="0"*len(saved)
    try:
        mod.ReaderProvenanceGate(BASE,CANDIDATE)
    except mod.UnadmittedReaderRoute as e:
        print("REJECTED_TAMPER",rel,str(e)[:130],flush=True)
    else:
        raise AssertionError("Forbidden Press file mismatch admitted: "+rel)
    finally:mod.APPROVED_SPREAD_FILES[rel]=saved
print("V151_ADMISSION_PASS",str(CANDIDATE),"three forged source/file identities rejected",flush=True)
