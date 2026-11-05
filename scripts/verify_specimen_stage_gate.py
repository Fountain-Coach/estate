#!/usr/bin/env python3
"""Independent read-only v147 Reader provenance acceptance on owner WLAN.

Run against the SOURCE-COPIED prospective guard, never the active guard, and
the immutable candidate. Negative cases alter only in-process constants.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path("/home/benedikt/estate-shell-acceptance-staging")
RELEASES = ROOT / "releases"
BASELINE = RELEASES / "shared-shell-20261103-v140-same-folio-return"
CANDIDATE = RELEASES / "shared-shell-20261105-v148-specimen-boundary-a9575ba"
GUARD_SOURCE = ROOT / "reader_provenance_gate_v148_candidate.py"

spec = importlib.util.spec_from_file_location("reader_provenance_gate_v147_candidate",GUARD_SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError("No scoped candidate guard file")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

g = mod.ReaderProvenanceGate(BASELINE,CANDIDATE)
for path in (
  "/estate/",
  "/estate/index.html",
  "/estate/essays/what-makes-a-page-modern/assets/reader.svg",
  "/estate/assets/linotype/reading-first-app.js",
  "/estate/assets/linotype/reading-first-press-engine.js",
  "/private-auditions/what-makes-a-page-modern-20261104-qwen3/index.html",
  "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-a.mp3",
  "/private-auditions/what-makes-a-page-modern-20261104-qwen3/vergil-b.mp3",
):
    g.check(path)
    print("ADMITTED",path)

for name in ("APPROVED_SPECIMEN_LOCK_SHA256",
             "APPROVED_SPECIMEN_SOURCE_COMMIT",
             "APPROVED_SPECIMEN_READER_SHA256"):
    original=getattr(mod,name)
    setattr(mod,name,"0"*len(original))
    try:
        mod.ReaderProvenanceGate(BASELINE,CANDIDATE)
    except mod.UnadmittedReaderRoute as error:
        print("REFUSED",name,str(error)[:105])
    else:
        raise AssertionError("Candidate admitted with forged " + name)
    finally:
        setattr(mod,name,original)
print("ACCEPTED v148 original Reader, unrelated assets preserved, 3 refusal probes")
