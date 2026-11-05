#!/usr/bin/env python3
"""Actual v140->v150 Reader provenance, candidate only. No live mutation."""
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path("/home/benedikt/estate-shell-acceptance-staging")
BASE=ROOT/"releases/shared-shell-20261103-v140-same-folio-return"
CANDIDATE=ROOT/"releases/shared-shell-20261105-v150-fluid-nested-3ba1b0e"
GUARD=ROOT/"reader_provenance_gate_v150_candidate.py"
spec=importlib.util.spec_from_file_location("reader_provenance_gate_v150_candidate",GUARD)
if spec is None or spec.loader is None:raise RuntimeError("No scoped candidate provenance guard")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
g=mod.ReaderProvenanceGate(BASE,CANDIDATE)
for path in (
 "/estate/","/estate/index.html",
 "/estate/assets/linotype/reading-first-press-engine.js",
 "/estate/assets/linotype/reading-first-press-frame.css",
 "/estate/assets/linotype/reading-first-app.js",
 "/estate/essays/what-makes-a-page-modern/assets/reader.svg",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/index.html",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-a.mp3",
 "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-b.mp3"
):
    g.check(path)
    print("ADMITTED",path)
for name in ("APPROVED_FLUID_LOCK_SHA256","APPROVED_FLUID_SOURCE_COMMIT"):
    previous=getattr(mod,name)
    setattr(mod,name,"0"*len(previous))
    try:
        mod.ReaderProvenanceGate(BASE,CANDIDATE)
    except mod.UnadmittedReaderRoute as err:
        print("REFUSED_FORGED",name,str(err)[:110])
    else:
        raise AssertionError("Forged "+name+" admitted")
    finally:setattr(mod,name,previous)
for rel in mod.APPROVED_FLUID_FILES:
    previous=mod.APPROVED_FLUID_FILES[rel]
    mod.APPROVED_FLUID_FILES[rel]="0"*len(previous)
    try:
        mod.ReaderProvenanceGate(BASE,CANDIDATE)
    except mod.UnadmittedReaderRoute as err:
        print("REFUSED_FORGED_FILE",rel,str(err)[:110])
    else:
        raise AssertionError("Forged file identity admitted: "+rel)
    finally:mod.APPROVED_FLUID_FILES[rel]=previous
print("ACCEPTED v150 only against exact source and unchanged v149 lineage; four negative probes")
